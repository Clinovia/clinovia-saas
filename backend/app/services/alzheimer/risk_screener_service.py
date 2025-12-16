from uuid import UUID
from sqlalchemy.orm import Session
from app.schemas.alzheimer.risk_screener import AlzheimerRiskScreenerInput, AlzheimerRiskScreenerOutput
from app.clinical.alzheimer.risk_screener.risk_screener import calculate_risk_score
from app.db.models.assessments import AssessmentType
from app.services.assessment_pipeline import run_assessment_pipeline

def assess_alzheimer_risk(
    input_schema: AlzheimerRiskScreenerInput,
    db: Session,
    user_id: UUID,
) -> AlzheimerRiskScreenerOutput:
    """
    Pipeline for calculating Alzheimer's risk score and persisting assessment.
    """
    return run_assessment_pipeline(
        input_schema=input_schema,
        db=db,
        user_id=user_id,
        model_function=calculate_risk_score,
        assessment_type=AssessmentType.ALZHEIMER_RISK,
        model_name="alz-risk-screener-v1",
        model_version="1.0.0",
        use_cache=True,
    )
