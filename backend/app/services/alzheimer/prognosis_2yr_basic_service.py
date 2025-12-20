from uuid import UUID
from sqlalchemy.orm import Session
from app.schemas.alzheimer.prognosis_2yr_basic import AlzheimerPrognosis2yrBasicInput, AlzheimerPrognosis2yrBasicOutput
from app.clinical.alzheimer.ml_models.prognosis_2yr_basic import predict_prognosis_2yr_basic
from app.db.models.assessments import AssessmentType
from app.services.assessment_pipeline import run_assessment_pipeline

def predict_prog_2yr_basic(
    input_schema: AlzheimerPrognosis2yrBasicInput,
    db: Session,
    clinician_id: UUID,
) -> AlzheimerPrognosis2yrBasicOutput:
    """
    Pipeline for predicting 2-year progression (basic model) and persisting assessment.
    """
    return run_assessment_pipeline(
        input_schema=input_schema,
        db=db,
        clinician_id=clinician_id, 
        model_function=predict_prognosis_2yr_basic,
        assessment_type=AssessmentType.ALZHEIMER_PROGNOSIS_2YR_BASIC,
        specialty="alzheimer",
        model_name="prognosis-2yr-basic-v1",
        model_version="1.0.0",
        use_cache=True,
    )
