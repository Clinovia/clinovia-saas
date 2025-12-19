# app/services/cardiology/ecg_service.py
from uuid import UUID
from typing import Union, Dict, Any
from sqlalchemy.orm import Session
from app.schemas.cardiology import ECGInterpretationInput, ECGInterpretationOutput
from app.clinical.cardiology.ecg_interpret import interpret_ecg
from app.db.models.assessments import AssessmentType
from app.services.assessment_pipeline import run_assessment_pipeline

def run_ecg_interpretation(
    input_schema: Union[ECGInterpretationInput, Dict[str, Any]],
    db: Session,
    clinician_id: UUID,
) -> ECGInterpretationOutput:
    """
    Full ECG interpretation pipeline using generic assessment pipeline.
    """
    return run_assessment_pipeline(
        input_schema=input_schema,
        db=db,
        clinician_id=clinician_id, 
        model_function=interpret_ecg,
        assessment_type=AssessmentType.CARDIOLOGY_ECG,
        model_name="ecg-interpretation-v1",
        model_version="1.0.0",
        use_cache=True,
    )
