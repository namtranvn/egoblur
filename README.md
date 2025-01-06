curl -X 'POST' \
  'http://localhost:8000/v1/blur' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "input_video_path": "test_video.mp4",
  "face_model_score_threshold": 0.9,
  "lp_model_score_threshold": 0.9,
  "nms_iou_threshold": 0.3,
  "scale_factor_detections": 1,
  "output_video_fps": 30
}'