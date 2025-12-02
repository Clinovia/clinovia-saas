"""
Alzheimer assessment routes
---------------------------
Defines endpoints for Alzheimer's-related assessments:
- Screening diagnosis
- Basic diagnosis
- Extended diagnosis
- 2-year prognosis (basic & extended)
- Risk screener

All endpoints use a generic _make_wrapper() factory for minimal boilerplate.
All assessments require a patient_id in the URL path.
"""

from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.api.routes.utils.assessment_endpoint import create_assessment_endpoint
from app.schemas.alzheimer.diagnosis_screening import AlzheimerDiagnosisInput, AlzheimerDiagnosisOutput
from app.schemas.alzheimer.diagnosis_basic import AlzheimerDiagnosisBasicInput, AlzheimerDiagnosisBasicOutput
from app.schemas.alzheimer.diagnosis_extended import AlzheimerDiagnosisExtendedInput, AlzheimerDiagnosisExtendedOutput
from app.schemas.alzheimer.prognosis_2yr_basic import AlzheimerPrognosis2yrBasicInput, AlzheimerPrognosis2yrBasicOutput
from app.schemas.alzheimer.prognosis_2yr_extended import AlzheimerPrognosis2yrExtendedInput, AlzheimerPrognosis2yrExtendedOutput
from app.schemas.alzheimer.risk_screener import AlzheimerRiskScreenerInput, AlzheimerRiskScreenerOutput

from app.services.alzheimer.diagnosis_screening_service import predict_diag_screen
from app.services.alzheimer.diagnosis_basic_service import predict_diag_basic
from app.services.alzheimer.diagnosis_extended_service import predict_diag_extended
from app.services.alzheimer.prognosis_2yr_basic_service import predict_prog_2yr_basic
from app.services.alzheimer.prognosis_2yr_extended_service import predict_prog_2yr_extended
from app.services.alzheimer.risk_screener_service import assess_alzheimer_risk

from app.db.models.assessments import AssessmentType
from app.db.models.users import User

router = APIRouter(tags=["Alzheimer Assessments"])


# ================================================================
# 🔧 Generic wrapper factory
# ================================================================
def _make_wrapper(service_func):
    """
    Factory that generates a standardized service wrapper for FastAPI endpoints.
    Signature: (*, input_data, current_user, db) -> output
    """
    def wrapper(*, input_data, current_user: User, db: Session):
        return service_func(input_data, db=db, clinician_id=current_user.id)
    
    wrapper.__name__ = f"{service_func.__name__}_wrapper"
    return wrapper


# ================================================================
# 🧠 Endpoints - All require patient_id in URL
# ================================================================

create_assessment_endpoint(
    path="/diagnosisScreening",
    input_schema=AlzheimerDiagnosisInput,
    output_schema=AlzheimerDiagnosisOutput,
    service_function=_make_wrapper(predict_diag_screen),
    assessment_type=AssessmentType.ALZHEIMER_DIAGNOSIS_SCREENING,
    router=router,
)

create_assessment_endpoint(
    path="/diagnosisBasic",
    input_schema=AlzheimerDiagnosisBasicInput,
    output_schema=AlzheimerDiagnosisBasicOutput,
    service_function=_make_wrapper(predict_diag_basic),
    assessment_type=AssessmentType.ALZHEIMER_DIAGNOSIS_BASIC,
    router=router,
)

create_assessment_endpoint(
    path="/diagnosisExtended",
    input_schema=AlzheimerDiagnosisExtendedInput,
    output_schema=AlzheimerDiagnosisExtendedOutput,
    service_function=_make_wrapper(predict_diag_extended),
    assessment_type=AssessmentType.ALZHEIMER_DIAGNOSIS_EXTENDED,
    router=router,
)

create_assessment_endpoint(
    path="/prognosis2yrBasic",
    input_schema=AlzheimerPrognosis2yrBasicInput,
    output_schema=AlzheimerPrognosis2yrBasicOutput,
    service_function=_make_wrapper(predict_prog_2yr_basic),
    assessment_type=AssessmentType.ALZHEIMER_PROGNOSIS_2YR_BASIC,
    router=router,
)

create_assessment_endpoint(
    path="/prognosis2yrExtended",
    input_schema=AlzheimerPrognosis2yrExtendedInput,
    output_schema=AlzheimerPrognosis2yrExtendedOutput,
    service_function=_make_wrapper(predict_prog_2yr_extended),
    assessment_type=AssessmentType.ALZHEIMER_PROGNOSIS_2YR_EXTENDED,
    router=router,
)

create_assessment_endpoint(
    path="/riskScreener",
    input_schema=AlzheimerRiskScreenerInput,
    output_schema=AlzheimerRiskScreenerOutput,
    service_function=_make_wrapper(assess_alzheimer_risk),
    assessment_type=AssessmentType.ALZHEIMER_RISK,
    router=router,
)