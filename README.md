curl -X 'POST' \
  'http://localhost:8000/v1/blur' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "input_video_path": "./demo_assets/test_video.mp4",
  "output_video_path": "./output/test_video_output.avi",
  "face_model_path": "./models/ego_blur_face/ego_blur_face.jit",
  "lp_model_path": "./models/ego_blur_lp/ego_blur_lp.jit",
  "face_model_score_threshold": 0.9,
  "lp_model_score_threshold": 0.9,
  "nms_iou_threshold": 0.3,
  "scale_factor_detections": 1,
  "output_video_fps": 30
}'