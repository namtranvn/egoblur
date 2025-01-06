from fastapi import APIRouter, HTTPException
from typing import Dict, Optional
import os
from celery.result import AsyncResult
from celery import Celery
from models.blur import BlurRequest, TaskResponse, TaskStatusResponse

router = APIRouter(
    prefix="/blur",
    tags=["blur"],
    responses={404: {"description": "Not found"}},
)

# Initialize Celery client
celery_app = Celery('tasks',
                    broker='amqp://guest:guest@rabbitmq:5672//',
                    backend='redis://redis:6379/0')

@router.get("/health")
async def check_processor_health() -> Dict:
    """
    Check the health of Celery workers
    """
    try:
        i = celery_app.control.inspect()
        if not i.active():
            return {
                "status": "degraded",
                "message": "No Celery workers available"
            }
        return {
            "status": "healthy",
            "message": "Service is running"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@router.post("", response_model=TaskResponse)
async def blur_video(request: BlurRequest) -> TaskResponse:
    """
    Submit a video for processing with EgoBlur
    """
    try:
        # Submit task to Celery
        task = celery_app.send_task(
            'process_video',
            args=[request.dict()],
            kwargs={}
        )
        
        return TaskResponse(
            task_id=task.id,
            status="submitted",
            message="Task submitted successfully"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error submitting task: {str(e)}"
        )

@router.get("/status/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str) -> TaskStatusResponse:
    """
    Get the status of a submitted task
    """
    try:
        task_result = AsyncResult(task_id, app=celery_app)
        
        if task_result.failed():
            return TaskStatusResponse(
                task_id=task_id,
                status="failed",
                error=str(task_result.result)
            )
            
        if task_result.ready():
            return TaskStatusResponse(
                task_id=task_id,
                status="completed",
                result=task_result.result
            )
            
        return TaskStatusResponse(
            task_id=task_id,
            status=task_result.status.lower()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error checking task status: {str(e)}"
        )