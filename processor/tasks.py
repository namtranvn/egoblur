# processor/tasks.py
from celery import Celery
from celery.signals import worker_process_init
import torch
import os
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

    return face_detector, lp_detector

@worker_process_init.connect
def init_worker_process(**kwargs):
    """
    Load models once when the worker process initializes
    """
    print("Load Model")
    global face_detector, lp_detector
    face_detector, lp_detector = load_models()

@app.task(name="process_video", bind=True)
def process_video(self, params):
    try:
        # Validate input paths
        if not os.path.exists(params["input_video_path"]):
            raise FileNotFoundError(f"Input video not found: {params['input_video_path']}")

        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(params["output_video_path"])
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Update task state
        self.update_state(state='PROCESSING',
                         meta={'status': 'Processing video'})

        print("Start Processing")
        # Process video using globally loaded models
        ego_blur.visualize_video(
            input_video_path=params["input_video_path"],
            face_detector=face_detector,
            lp_detector=lp_detector,
            face_model_score_threshold=params["face_model_score_threshold"],
            lp_model_score_threshold=params["lp_model_score_threshold"],
            nms_iou_threshold=params["nms_iou_threshold"],
            output_video_path=params["output_video_path"],
            scale_factor_detections=params["scale_factor_detections"],
            output_video_fps=params["output_video_fps"]
        )

        return {
            "status": "success",
            "output_path": params["output_video_path"],
            "message": "Video processed successfully"
        }

    except Exception as e:
        # Update task state on failure
        self.update_state(state='FAILURE',
                         meta={'status': 'Failed',
                               'error': str(e)})
        raise