"""
Cardiology assessment routes
----------------------------
This module defines endpoints for cardiology-related assessments:
- ASCVD Risk
- Blood Pressure Category
- CHA₂DS₂-VASc Score
- ECG Interpretation
- Ejection Fraction

All endpoints use a generic _make_wrapper() factory for minimal boilerplate.
"""
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.api.routes.utils.assessment_endpoint import create_assessment_endpoint
from app.schemas.cardiology import (
    ASCVDRiskInput,
    ASCVDRiskOutput,
    BPCategoryInput,
    BPCategoryOutput,
    CHA2DS2VAScInput,
    CHA2DS2VAScOutput,
    ECGInterpretationInput,
    ECGInterpretationOutput,
    EchonetEFOutput,
)
from app.services.cardiology import (
    ascvd_service,
    bp_service,
    cha2ds2vasc_service,
    ecg_service,
    ef_service,
)
from app.db.models.assessments import AssessmentType
from app.db.models.users import User
from app.api.deps import get_db, get_current_active_user

router = APIRouter(tags=["Cardiology"])


# ================================================================
# 🔧 Generic wrapper factory (SYNC version)
# ================================================================
def _make_wrapper(service_func):
    """
    Factory that generates a standardized service wrapper with automatic
    injection of `db` and `current_user` via FastAPI Depends.
    This version is synchronous.
    """
    def wrapper(
        *, 
        input_data, 
        db: Session = Depends(get_db), 
        current_user: User = Depends(get_current_active_user)
    ):
        return service_func(input_data, db=db, clinician_id=current_user.id)
    
    wrapper.__name__ = f"{service_func.__name__}_wrapper"
    return wrapper


# ================================================================
# 🫀 Endpoints
# ================================================================

# 1️⃣ ASCVD Risk
create_assessment_endpoint(
    path="/ascvd",
    input_schema=ASCVDRiskInput,
    output_schema=ASCVDRiskOutput,
    service_function=_make_wrapper(ascvd_service.run_ascvd_prediction),
    assessment_type=AssessmentType.CARDIOLOGY_ASCVD,
    router=router,
)

# 2️⃣ Blood Pressure Category
create_assessment_endpoint(
    path="/bp-category",
    input_schema=BPCategoryInput,
    output_schema=BPCategoryOutput,
    service_function=_make_wrapper(bp_service.run_bp_category_prediction),
    assessment_type=AssessmentType.CARDIOLOGY_BP,
    router=router,
)

# 3️⃣ CHA₂DS₂-VASc Score
create_assessment_endpoint(
    path="/cha2ds2vasc",
    input_schema=CHA2DS2VAScInput,
    output_schema=CHA2DS2VAScOutput,
    service_function=_make_wrapper(cha2ds2vasc_service.run_cha2ds2vasc_prediction),
    assessment_type=AssessmentType.CARDIOLOGY_CHA2DS2VASC,
    router=router,
)

# 4️⃣ ECG Interpretation
create_assessment_endpoint(
    path="/ecg-interpreter",
    input_schema=ECGInterpretationInput,
    output_schema=ECGInterpretationOutput,
    service_function=_make_wrapper(ecg_service.run_ecg_interpretation),
    assessment_type=AssessmentType.CARDIOLOGY_ECG,
    router=router,
)

# 5️⃣ Ejection Fraction Prediction
@router.post("/ejection-fraction", response_model=EchonetEFOutput)
async def ef_endpoint(
    video: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)  # ← Changed: User object, not dict
):
    return await ef_service.run_ef_prediction(
        video=video,
        db=db,
        clinician_id=current_user.id  # ← Changed: .id instead of ["id"]
    )