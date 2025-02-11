# processor/tasks.py
from celery import Celery
import torch
# NEW: Added SoftTimeLimitExceeded exception
from celery.exceptions import TaskError, SoftTimeLimitExceeded
import os

app = Celery('tasks',
             broker='amqp://guest:guest@rabbitmq:5672//',
             backend='redis://redis:6379/0')

# NEW: Updated Celery configuration
app.conf.update(
    broker_connection_retry_on_startup=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour
    task_soft_time_limit=3600,
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    # NEW: Added broker settings
    broker_heartbeat=0,
    broker_connection_timeout=30,
    result_expires=3600,
    # NEW: Added worker settings
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_queue_max_priority=10
)

# NEW: Added task settings
@app.task(name="process_video", 
          bind=True, 
          throws=(RuntimeError,), 
          time_limit=3600, 
          soft_time_limit=3600,
          acks_late=True)
def process_video(self, params):
    try:
        # NEW: Added GPU memory management
        if torch.cuda.is_available():
            device = torch.device('cuda')
            torch.cuda.empty_cache()
            torch.cuda.set_device(0)
        else:
            device = torch.device('cpu')

        # Load models
        if os.path.exists(params["face_model_path"]):
            face_detector = torch.jit.load(params["face_model_path"], map_location=device)
            face_detector.eval()
        
        # Process video
        result = ego_blur.visualize_video(
            input_video_path=params["input_video_path"],
            face_detector=face_detector,
            lp_detector=None,  # Simplified to use only face detection
            face_model_score_threshold=params["face_model_score_threshold"],
            lp_model_score_threshold=params["lp_model_score_threshold"],
            nms_iou_threshold=params["nms_iou_threshold"],
            output_video_path=params["output_video_path"],
            scale_factor_detections=params["scale_factor_detections"],
            output_video_fps=params["output_video_fps"]
        )
        
        return {
            "status": "success",
            "message": "Video processed successfully",
            "output_path": params["output_video_path"]
        }
        
    # NEW: Added exception handling
    except SoftTimeLimitExceeded:
        raise SoftTimeLimitExceeded("Task took too long to complete")
    except Exception as e:
        raise RuntimeError(str(e))
    finally:
        # NEW: Added cleanup
        if torch.cuda.is_available():
            torch.cuda.empty_cache()