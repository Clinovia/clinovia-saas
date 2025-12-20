# app/services/cardiology/cha2ds2vasc_service.py
from uuid import UUID
from typing import Union, Dict, Any
from sqlalchemy.orm import Session
from app.schemas.cardiology import CHA2DS2VAScInput, CHA2DS2VAScOutput
from app.clinical.cardiology.cha2ds2vasc import calculate_cha2ds2vasc
from app.db.models.assessments import AssessmentType
from app.services.assessment_pipeline import run_assessment_pipeline

def run_cha2ds2vasc_prediction(
    input_schema: Union[CHA2DS2VAScInput, Dict[str, Any]],
    db: Session,
    clinician_id: UUID,
) -> CHA2DS2VAScOutput:
    """
    Full stroke risk assessment pipeline.
    """
    return run_assessment_pipeline(
        input_schema=input_schema,
        db=db,
        clinician_id=clinician_id, 
        model_function=calculate_cha2ds2vasc,
        assessment_type=AssessmentType.CARDIOLOGY_CHA2DS2VASC,
        specialty="cardiology",
        model_name="cha2ds2vasc-v1",
        model_version="1.0.0",
        use_cache=True,
    )
