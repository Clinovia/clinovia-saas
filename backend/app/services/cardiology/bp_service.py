# app/services/cardiology/bp_service.py
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas.cardiology import BPCategoryInput, BPCategoryOutput
from app.clinical.cardiology.bp_category import categorize_blood_pressure
from app.db.models.assessments import AssessmentType
from app.services.assessment_pipeline import run_assessment_pipeline

def run_bp_category_prediction(
    input_schema: BPCategoryInput,
    db: Session,
    user_id: UUID,
) -> BPCategoryOutput:
    """
    Full blood pressure categorization pipeline.
    """
    return run_assessment_pipeline(
        input_schema=input_schema,
        db=db,
        user_id=user_id,
        model_function=categorize_blood_pressure,
        assessment_type=AssessmentType.CARDIOLOGY_BP,
        model_name="bp-category-v1",
        model_version="1.0.0",
        use_cache=True,
    )
