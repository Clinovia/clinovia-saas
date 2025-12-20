# app/services/cardiology/bp_service.py
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas.cardiology import BPCategoryInput, BPCategoryOutput
from app.clinical.cardiology.bp_category import categorize_blood_pressure
from app.db.models.assessments import AssessmentType
from app.services.assessment_pipeline import run_assessment_pipeline


def run_bp_category_prediction(
    *,
    input_schema: BPCategoryInput,
    db: Session,
    clinician_id: UUID,
) -> BPCategoryOutput:
    """
    Full blood pressure categorization pipeline.

    This wraps the generic assessment pipeline for BP categorization.
    """
    # Run the generic assessment pipeline
    prediction_schema: BPCategoryOutput = run_assessment_pipeline(
        input_schema=input_schema,
        db=db,
        clinician_id=clinician_id,
        model_function=categorize_blood_pressure,
        assessment_type=AssessmentType.CARDIOLOGY_BP,
        specialty="cardiology",
        model_name="bp-category-v1",
        model_version="1.0.0",
        use_cache=True,
    )

    return prediction_schema
