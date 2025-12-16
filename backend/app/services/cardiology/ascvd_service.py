# app/services/cardiology/ascvd_service.py
from uuid import UUID
from sqlalchemy.orm import Session
from app.schemas.cardiology import ASCVDRiskInput, ASCVDRiskOutput
from app.clinical.cardiology.ascvd import calculate_ascvd
from app.db.models.assessments import AssessmentType
from app.services.assessment_pipeline import run_assessment_pipeline

def run_ascvd_prediction(
    input_schema: ASCVDRiskInput,
    db: Session,
    user_id: UUID,
) -> ASCVDRiskOutput:
    """
    Full ASCVD risk calculation pipeline using schema validation.
    """
    return run_assessment_pipeline(
        input_schema=input_schema,
        db=db,
        user_id=user_id,
        model_function=calculate_ascvd,
        assessment_type=AssessmentType.CARDIOLOGY_ASCVD,
        model_name="ascvd-rule-v1",
        model_version="1.0.0",
        use_cache=True,
    )
