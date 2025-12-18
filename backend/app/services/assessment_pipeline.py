from typing import Type
from sqlalchemy.orm import Session
from pydantic import BaseModel
from uuid import UUID
from app.db.repositories.assessment_repository import AssessmentRepository
from app.db.models.assessments import AssessmentType
from app.services.alzheimer.cache import cache_result


def run_assessment_pipeline(
    input_schema: BaseModel,
    db: Session,
    user_id: int,
    model_function,
    assessment_type: AssessmentType,
    model_name: str,
    model_version: str = "1.0.0",
    use_cache: bool = True,
) -> BaseModel:
    """
    Generic assessment pipeline for any clinical model:
    - Runs prediction using the provided model_function
    - Persists the assessment to the database
    - Returns typed Pydantic output
    """
    # Wrap model_function with caching if requested
    if use_cache:
        model_function = cache_result(model_function)

    # Run model prediction
    prediction_schema: BaseModel = model_function(input_schema)

    # Persist assessment to DB
    AssessmentRepository(db).create(
        specialty=model_name.split("_")[0],  # e.g., 'alzheimer' or 'cardiology'
        assessment_type=assessment_type,
        patient_id=getattr(input_schema, "patient_id", None),
        clinician_id=user_id,  # updated field
        input_data=input_schema.model_dump(mode="json"),
        result=prediction_schema.model_dump(mode="json"),
        algorithm_version=model_version,
        status="completed",
    )

    return prediction_schema
