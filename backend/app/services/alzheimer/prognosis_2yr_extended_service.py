from uuid import UUID
from sqlalchemy.orm import Session
from app.schemas.alzheimer.prognosis_2yr_extended import AlzheimerPrognosis2yrExtendedInput, AlzheimerPrognosis2yrExtendedOutput
from app.clinical.alzheimer.ml_models.prognosis_2yr_extended import predict_prognosis_2yr_extended
from app.db.models.assessments import AssessmentType
from app.services.assessment_pipeline import run_assessment_pipeline

def predict_prog_2yr_extended(
    input_schema: AlzheimerPrognosis2yrExtendedInput,
    db: Session,
    user_id: UUID,
) -> AlzheimerPrognosis2yrExtendedOutput:
    """
    Pipeline for predicting 2-year progression (extended model) and persisting assessment.
    """
    return run_assessment_pipeline(
        input_schema=input_schema,
        db=db,
        user_id=user_id,
        model_function=predict_prognosis_2yr_extended,
        assessment_type=AssessmentType.ALZHEIMER_PROGNOSIS_2YR_EXTENDED,
        model_name="prognosis-2yr-extended-v1",
        model_version="1.0.0",
        use_cache=True,
    )
