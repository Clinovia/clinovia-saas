"""
Cardiology assessment routes
----------------------------
Defines endpoints for cardiology-related assessments:
- ASCVD Risk
- Blood Pressure Category
- CHA₂DS₂-VASc Score
- ECG Interpretation
- Ejection Fraction
"""

from fastapi import UploadFile, File, HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any

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
from app.api.deps import get_db, get_current_user

router = APIRouter(tags=["Cardiology"])


@router.get("/test")
async def test_route():
    return {"ok": True}


# ================================================================
# 🫀 Stateless Assessment Endpoints (no patient_id)
# ================================================================

create_assessment_endpoint(
    path="/ascvd",
    input_schema=ASCVDRiskInput,
    output_schema=ASCVDRiskOutput,
    service_function=ascvd_service.run_ascvd_prediction,
    assessment_type=AssessmentType.CARDIOLOGY_ASCVD,
    router=router,
)

create_assessment_endpoint(
    path="/bp-category",
    input_schema=BPCategoryInput,
    output_schema=BPCategoryOutput,
    service_function=bp_service.run_bp_category_prediction,
    assessment_type=AssessmentType.CARDIOLOGY_BP,
    router=router,
)

create_assessment_endpoint(
    path="/cha2ds2vasc",
    input_schema=CHA2DS2VAScInput,
    output_schema=CHA2DS2VAScOutput,
    service_function=cha2ds2vasc_service.run_cha2ds2vasc_prediction,
    assessment_type=AssessmentType.CARDIOLOGY_CHA2DS2VASC,
    router=router,
)

create_assessment_endpoint(
    path="/ecg-interpreter",
    input_schema=ECGInterpretationInput,
    output_schema=ECGInterpretationOutput,
    service_function=ecg_service.run_ecg_interpretation,
    assessment_type=AssessmentType.CARDIOLOGY_ECG,
    router=router,
)


# ================================================================
# 🫀 Ejection Fraction (async, optional patient_id)
# ================================================================

@router.post(
    "/ejection-fraction",
    response_model=EchonetEFOutput,
    summary="Predict ejection fraction from echocardiogram video",
)
async def predict_ejection_fraction(
    video: UploadFile = File(...),
    patient_id: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Analyze echocardiogram video and predict ejection fraction.
    Optionally associates the result with a patient.
    """
    try:
        return await ef_service.run_ef_prediction(
            video=video,
            db=db,
            clinician_id=current_user.id,
            patient_id=patient_id,
        )

    except ef_service.EFServiceError as e:
        raise HTTPException(status_code=503, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process echocardiogram: {str(e)}",
        )
