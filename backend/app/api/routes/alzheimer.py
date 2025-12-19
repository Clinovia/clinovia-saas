"""
Alzheimer assessment routes
---------------------------
Defines endpoints for Alzheimer's-related assessments:
- Screening diagnosis
- Basic diagnosis
- Extended diagnosis
- 2-year prognosis (basic & extended)
- Risk screener
"""

from fastapi import APIRouter

from app.api.routes.utils.assessment_endpoint import create_assessment_endpoint
from app.schemas.alzheimer.diagnosis_screening import (
    AlzheimerDiagnosisInput,
    AlzheimerDiagnosisOutput,
)
from app.schemas.alzheimer.diagnosis_basic import (
    AlzheimerDiagnosisBasicInput,
    AlzheimerDiagnosisBasicOutput,
)
from app.schemas.alzheimer.diagnosis_extended import (
    AlzheimerDiagnosisExtendedInput,
    AlzheimerDiagnosisExtendedOutput,
)
from app.schemas.alzheimer.prognosis_2yr_basic import (
    AlzheimerPrognosis2yrBasicInput,
    AlzheimerPrognosis2yrBasicOutput,
)
from app.schemas.alzheimer.prognosis_2yr_extended import (
    AlzheimerPrognosis2yrExtendedInput,
    AlzheimerPrognosis2yrExtendedOutput,
)
from app.schemas.alzheimer.risk_screener import (
    AlzheimerRiskScreenerInput,
    AlzheimerRiskScreenerOutput,
)

from app.services.alzheimer.diagnosis_screening_service import predict_diag_screen
from app.services.alzheimer.diagnosis_basic_service import predict_diag_basic
from app.services.alzheimer.diagnosis_extended_service import predict_diag_extended
from app.services.alzheimer.prognosis_2yr_basic_service import predict_prog_2yr_basic
from app.services.alzheimer.prognosis_2yr_extended_service import predict_prog_2yr_extended
from app.services.alzheimer.risk_screener_service import assess_alzheimer_risk

from app.db.models.assessments import AssessmentType

router = APIRouter(tags=["Alzheimer Assessments"])


# ================================================================
# 🧠 Stateless Alzheimer Assessments
# ================================================================

create_assessment_endpoint(
    path="/diagnosis-screening",
    input_schema=AlzheimerDiagnosisInput,
    output_schema=AlzheimerDiagnosisOutput,
    service_function=predict_diag_screen,
    assessment_type=AssessmentType.ALZHEIMER_DIAGNOSIS_SCREENING,
    router=router,
)

create_assessment_endpoint(
    path="/diagnosis-basic",
    input_schema=AlzheimerDiagnosisBasicInput,
    output_schema=AlzheimerDiagnosisBasicOutput,
    service_function=predict_diag_basic,
    assessment_type=AssessmentType.ALZHEIMER_DIAGNOSIS_BASIC,
    router=router,
)

create_assessment_endpoint(
    path="/diagnosis-extended",
    input_schema=AlzheimerDiagnosisExtendedInput,
    output_schema=AlzheimerDiagnosisExtendedOutput,
    service_function=predict_diag_extended,
    assessment_type=AssessmentType.ALZHEIMER_DIAGNOSIS_EXTENDED,
    router=router,
)

create_assessment_endpoint(
    path="/prognosis-2yr-basic",
    input_schema=AlzheimerPrognosis2yrBasicInput,
    output_schema=AlzheimerPrognosis2yrBasicOutput,
    service_function=predict_prog_2yr_basic,
    assessment_type=AssessmentType.ALZHEIMER_PROGNOSIS_2YR_BASIC,
    router=router,
)

create_assessment_endpoint(
    path="/prognosis-2yr-extended",
    input_schema=AlzheimerPrognosis2yrExtendedInput,
    output_schema=AlzheimerPrognosis2yrExtendedOutput,
    service_function=predict_prog_2yr_extended,
    assessment_type=AssessmentType.ALZHEIMER_PROGNOSIS_2YR_EXTENDED,
    router=router,
)

create_assessment_endpoint(
    path="/risk-screener",
    input_schema=AlzheimerRiskScreenerInput,
    output_schema=AlzheimerRiskScreenerOutput,
    service_function=assess_alzheimer_risk,
    assessment_type=AssessmentType.ALZHEIMER_RISK,
    router=router,
)
