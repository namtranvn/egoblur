from pydantic import BaseModel
from typing import Optional, Dict

class BlurRequest(BaseModel):
    input_video_path: str
    output_video_path: str
    face_model_path: str = "./models/ego_blur_face/ego_blur_face.jit"
    lp_model_path: str = "./models/ego_blur_lp/ego_blur_lp.jit"
    face_model_score_threshold: float = 0.9
    lp_model_score_threshold: float = 0.9
    nms_iou_threshold: float = 0.3
    scale_factor_detections: float = 1.0
    output_video_fps: int = 30

    class Config:
        schema_extra = {
            "example": {
                "input_video_path": "./demo_assets/test_video.mp4",
                "output_video_path": "./output/test_video_output.mp4",
                "face_model_score_threshold": 0.9,
                "output_video_fps": 30
            }
        }

class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str

class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Dict] = None
    error: Optional[str] = None