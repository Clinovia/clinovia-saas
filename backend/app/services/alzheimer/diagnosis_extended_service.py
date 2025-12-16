from uuid import UUID
from sqlalchemy.orm import Session
from app.schemas.alzheimer.diagnosis_extended import (
    AlzheimerDiagnosisExtendedInput,
    AlzheimerDiagnosisExtendedOutput,
)
from app.clinical.alzheimer.ml_models.diagnosis_extended import predict_cognitive_status_extended
from app.db.models.assessments import AssessmentType
from app.services.assessment_pipeline import run_assessment_pipeline

def predict_diag_extended(
    input_schema: AlzheimerDiagnosisExtendedInput,
    db: Session,
    user_id: UUID,
) -> AlzheimerDiagnosisExtendedOutput:
    """
    Full pipeline for predicting cognitive status using the extended Alzheimer model.
    """
    return run_assessment_pipeline(
        input_schema=input_schema,
        db=db,
        user_id=user_id,
        model_function=predict_cognitive_status_extended,
        assessment_type=AssessmentType.ALZHEIMER_DIAGNOSIS_EXTENDED,
        model_name="alz-diagnosis-extended-v1",
        model_version="1.0.0",
        use_cache=True,
    )
