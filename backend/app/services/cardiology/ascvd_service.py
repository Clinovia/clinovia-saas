# app/services/cardiology/ascvd_service.py
from sqlalchemy.orm import Session
from app.schemas.cardiology import ASCVDRiskInput, ASCVDRiskOutput
from app.clinical.cardiology.ascvd import calculate_ascvd
from app.db.models.assessments import AssessmentType
from app.services.assessment_pipeline import run_assessment_pipeline

def run_ascvd_prediction(
    input_schema: ASCVDRiskInput,
    db: Session,
    clinician_id: int,
) -> ASCVDRiskOutput:
    """
    Full ASCVD risk calculation pipeline using schema validation.
    """
    return run_assessment_pipeline(
        input_schema=input_schema,
        db=db,
        clinician_id=clinician_id,
        model_function=calculate_ascvd,
        assessment_type=AssessmentType.CARDIOLOGY_ASCVD,
        model_name="ascvd-rule-v1",
        model_version="1.0.0",
        use_cache=True,
    )
