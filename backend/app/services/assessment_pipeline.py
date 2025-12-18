from typing import Optional, Type
from sqlalchemy.orm import Session
from pydantic import BaseModel
from uuid import UUID

from app.db.repositories.assessment_repository import AssessmentRepository
from app.db.models.assessments import AssessmentType
from app.services.alzheimer.cache import cache_result


def run_assessment_pipeline(
    input_schema: BaseModel,
    db: Session,
    clinician_id: UUID,
    model_function,
    assessment_type: AssessmentType,
    model_name: str,
    patient_id: Optional[UUID] = None,  # <-- patient_id is optional
    model_version: str = "1.0.0",
    use_cache: bool = True,
) -> BaseModel:
    """
    Generic assessment pipeline for any clinical model:
    - Runs prediction using the provided model_function
    - Persists the assessment to the database
    - Returns typed Pydantic output
    
    Args:
        input_schema: Pydantic schema containing input data (may include patient_id)
        db: SQLAlchemy session
        clinician_id: Clinician performing the assessment
        model_function: Function that generates the prediction
        assessment_type: Type of assessment (Enum)
        model_name: Name of the model (used for specialty)
        patient_id: Optional patient UUID
        model_version: Version of the algorithm/model
        use_cache: Whether to wrap the model function with caching
    
    Returns:
        Pydantic schema of the prediction result
    """
    # Wrap model_function with caching if requested
    if use_cache:
        model_function = cache_result(model_function)

    # Run model prediction
    prediction_schema: BaseModel = model_function(input_schema)

    # Determine patient_id: prefer explicit argument, else fallback to input_schema
    final_patient_id: Optional[UUID] = patient_id or getattr(input_schema, "patient_id", None)

    # Persist assessment to DB
    AssessmentRepository(db).create(
        specialty=model_name.split("_")[0],  # e.g., 'alzheimer' or 'cardiology'
        assessment_type=assessment_type,
        patient_id=final_patient_id,  # can be None
        clinician_id=clinician_id,
        input_data=input_schema.model_dump(mode="json"),
        result=prediction_schema.model_dump(mode="json"),
        algorithm_version=model_version,
        status="completed",
    )

    return prediction_schema
