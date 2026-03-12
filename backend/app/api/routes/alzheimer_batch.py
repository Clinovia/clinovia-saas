# backend/app/api/routes/alzheimer_batch.py
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends
from app.services.alzheimer.batch_service import AlzheimerBatchService

router = APIRouter(prefix="/alzheimer/batch", tags=["Alzheimer Batch"])

@router.post("/upload")
async def upload_batch(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    service: AlzheimerBatchService = Depends()
):
    """Upload batch CSV/JSON and process asynchronously"""
    result = await service.process_batch(file, background_tasks)
    return {"status": "submitted", "details": result}

@router.get("/status/{batch_id}")
async def batch_status(batch_id: str, service: AlzheimerBatchService = Depends()):
    """Check status of a batch processing job"""
    return service.get_status(batch_id)
