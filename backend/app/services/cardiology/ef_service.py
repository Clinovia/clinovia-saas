# app/services/cardiology/ef_service.py
from sqlalchemy.orm import Session
from fastapi import UploadFile 
from app.schemas.cardiology import EchonetEFInput, EchonetEFOutput
from app.clinical.cardiology.echonet_ef import predict_ejection_fraction_from_bytes
from app.db.models.assessments import AssessmentType
from app.services.assessment_pipeline import run_assessment_pipeline

async def run_ef_prediction(
    video: UploadFile,
    db: Session,
    clinician_id: int,
) -> EchonetEFOutput:
    """
    Full ejection fraction (EF) prediction from uploaded video.
    """
    video_bytes = await video.read()
    
    result = predict_ejection_fraction_from_bytes(
        video_bytes=video_bytes,
        patient_id=None,  # Or extract from metadata if needed
        filename=video.filename
    )
    
    # TODO: Save to database using assessment_pipeline if needed
    
    return result