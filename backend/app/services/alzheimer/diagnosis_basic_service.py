from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas.alzheimer.diagnosis_basic import (
    AlzheimerDiagnosisBasicInput,
    AlzheimerDiagnosisBasicOutput,
)
from app.clinical.alzheimer.ml_models.diagnosis_basic import (
    predict_cognitive_status_basic,
)
from app.db.models.assessments import AssessmentType
from app.services.assessment_pipeline import run_assessment_pipeline


def predict_diag_basic(
    input_schema: AlzheimerDiagnosisBasicInput,
    db: Session,
    user_id: UUID,  # ✅ STRING (Supabase-compatible)
) -> AlzheimerDiagnosisBasicOutput:
    """
    Full pipeline for predicting cognitive status using the basic Alzheimer model.
    """
    return run_assessment_pipeline(
        input_schema=input_schema,
        db=db,
        user_id=user_id,  # ✅ FIXED
        model_function=predict_cognitive_status_basic,
        assessment_type=AssessmentType.ALZHEIMER_DIAGNOSIS_BASIC,
        model_name="alz-diagnosis-basic-v1",
        model_version="1.0.0",
        use_cache=True,
    )
