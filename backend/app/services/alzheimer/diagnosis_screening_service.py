from uuid import UUID
from sqlalchemy.orm import Session
from app.schemas.alzheimer.diagnosis_screening import AlzheimerDiagnosisInput, AlzheimerDiagnosisOutput
from app.clinical.alzheimer.ml_models.diagnosis_screening import predict_cognitive_status
from app.db.models.assessments import AssessmentType
from app.services.assessment_pipeline import run_assessment_pipeline

def predict_diag_screen(
    input_schema: AlzheimerDiagnosisInput,
    db: Session,
    clinician_id: UUID,
) -> AlzheimerDiagnosisOutput:
    """
    Pipeline for predicting cognitive status (screening model) and persisting assessment.
    """
    return run_assessment_pipeline(
        input_schema=input_schema,
        db=db,
        clinician_id=clinician_id, 
        model_function=predict_cognitive_status,
        assessment_type=AssessmentType.ALZHEIMER_DIAGNOSIS_SCREENING,
        model_name="alz-diagnosis-screening-v1",
        model_version="1.0.0",
        use_cache=True,
    )
