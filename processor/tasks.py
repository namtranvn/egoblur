# processor/tasks.py
import os
import boto3
import torch
from celery import Celery
from celery.signals import worker_process_init
from script import demo_ego_blur as ego_blur

# Initialize Celery
app = Celery('tasks',
             broker='amqp://guest:guest@rabbitmq:5672//',
             backend='redis://redis:6379/0')

app.conf.update(
    broker_connection_retry_on_startup=True,
    task_track_started=True,
    task_time_limit=3600,
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    worker_max_tasks_per_child=1
)

# Global variables for models
face_detector = None
lp_detector = None

def load_models():
    device = ego_blur.get_device()
    
    face_model_path = "./models/ego_blur_face/ego_blur_face.jit"
    lp_model_path = "./models/ego_blur_lp/ego_blur_lp.jit"
    
    if os.path.exists(face_model_path):
        face_detector = torch.jit.load(face_model_path, map_location="cpu").to(device)
        face_detector.eval()
        
    if os.path.exists(lp_model_path):
        lp_detector = torch.jit.load(lp_model_path, map_location="cpu").to(device)
        lp_detector.eval()

    print("Models loaded")
    return face_detector, lp_detector

@worker_process_init.connect
def init_worker_process(**kwargs):
    """
    Load models once when the worker process initializes
    """
    global face_detector, lp_detector
    face_detector, lp_detector = load_models()


def upload_to_s3(file_path, s3_key):
    """
    Upload a file to S3 bucket
    """
    try:
        s3 = boto3.client('s3')
        s3.upload_file(file_path, 'ego-blur', s3_key)
        return True
    except Exception as e:
        print(f"Failed to upload to S3: {str(e)}")
        return False

def cleanup_files(input_path, output_path):
    """
    Clean up temporary files after processing
    """
    try:
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)
    except Exception as e:
        print(f"Failed to cleanup files: {str(e)}")

def on_success(self, retval, task_id, args, kwargs):
    """
    Success callback handler
    """
    try:
        output_path = retval.get('output_path')
        if output_path and os.path.exists(output_path):
            # Upload to S3
            filename = os.path.basename(output_path)
            s3_key = f"output_data/{filename}"
            
            if upload_to_s3(output_path, s3_key):
                print(f"Successfully uploaded {filename} to S3")
                # Update return value with S3 path
                retval['s3_path'] = s3_key
            else:
                print(f"Failed to upload {filename} to S3")
            
            # Cleanup local files
            input_path = f"./demo_assets/{args[0]['input_video_path']}"
            cleanup_files(input_path, output_path)
            
        return retval
    except Exception as e:
        print(f"Error in success callback: {str(e)}")
        return retval

def on_failure(self, exc, task_id, args, kwargs, einfo):
    """
    Failure callback handler
    """
    try:
        # Cleanup any temporary files
        input_path = f"./demo_assets/{args[0]['input_video_path']}"
        output_path = f"./output/output_{args[0]['input_video_path']}"
        cleanup_files(input_path, output_path)
        
        # Log the error
        print(f"Task {task_id} failed: {str(exc)}")
        
    except Exception as e:
        print(f"Error in failure callback: {str(e)}")

@app.task(name="process_video", bind=True, on_success=on_success, on_failure=on_failure)
def process_video(self, params):
    try:
        # Validate input paths
        input_path = f"./demo_assets/{params['input_video_path']}"
        print(input_path)
        if os.path.exists(input_path):
            os.remove(input_path)
        
        # print(f"input_data/{params['input_video_path']}")
        file_key = f"input_data/{params['input_video_path']}"
        print(file_key)

        s3 = boto3.client('s3')
        s3.download_file('ego-blur', file_key, input_path)

        # Create output directory if it doesn't exist
        output_dir = "./output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_path = f"{output_dir}/output_{params['input_video_path']}"

        # Update task state
        self.update_state(state='PROCESSING',
                         meta={'status': 'Processing video'})

        print("Start Processing")
        # Process video using globally loaded models
        ego_blur.visualize_video(
            input_video_path=input_path,
            face_detector=face_detector,
            lp_detector=lp_detector,
            face_model_score_threshold=params["face_model_score_threshold"],
            lp_model_score_threshold=params["lp_model_score_threshold"],
            nms_iou_threshold=params["nms_iou_threshold"],
            output_video_path=output_path,
            scale_factor_detections=params["scale_factor_detections"],
            output_video_fps=params["output_video_fps"]
        )

        return {
            "status": "success",
            "output_path": output_path,
            "message": "Video processed successfully"
        }

    except Exception as e:
        # Update task state on failure
        self.update_state(state='FAILURE',
                         meta={'status': 'Failed',
                               'error': str(e)})
        raise