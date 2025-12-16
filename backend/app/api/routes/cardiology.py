# backend/app/api/routes/cardiology.py
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

import httpx
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
from app.api.deps import get_db, get_current_user

router = APIRouter(tags=["Cardiology"])

@router.get("/test")
async def test_route():
    return {"ok": True}


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
        current_user: User = Depends(get_current_user)
    ):
        return service_func(input_data, db=db, user_id=current_user.id)
    
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
@router.post("/ejection-fraction", response_model=Dict[str, Any])
async def predict_ejection_fraction(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    video: UploadFile = File(...),
    patient_id: str | None = None,
):
    """
    Analyze echocardiogram video and predict ejection fraction.
    
    - Accepts .avi, .mp4, or .mov video files
    - Returns EF percentage and clinical severity classification
    - Optionally saves to patient record if patient_id provided
    """
    try:
        # Call the microservice
        result = await ef_service.predict_ejection_fraction(video)
        
        # Save to database if patient_id provided
        if patient_id:
            from app.db.repositories.cardiology_repository import CardiologyRepository
            cardio_repo = CardiologyRepository(db)
            
            assessment = cardio_repo.create_ef_assessment(
                patient_id=patient_id,
                user_id=current_user.id,
                ef_value=result["ef_value"],
                severity=result["severity"],
                confidence=result.get("confidence"),
                model_version=result.get("model_version"),
                metadata={
                    "filename": result.get("filename"),
                    "file_size_mb": result.get("file_size_mb")
                }
            )
            
            result["assessment_id"] = assessment.id
            result["saved_to_patient"] = True
        
        return result
        
    except ef_service.EFServiceError as e:
        raise HTTPException(status_code=503, detail=str(e))
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process echocardiogram: {str(e)}"
        )


@router.get("/ejection-fraction/health")
async def check_ef_service():
    """
    Check the health status of the EF prediction microservice.
    """
    try:
        health = await ef_service.check_ef_service_health()
        return health
    except Exception as e:
        return {
            "status": "error",
            "model_loaded": False,
            "error": str(e)
        }


@router.get("/ejection-fraction/model-info")
async def get_ef_model_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get information about the EF prediction model.
    Requires authentication.
    """
    try:
        info = await ef_service.get_ef_model_info()
        return info
    except ef_service.EFServiceError as e:
        raise HTTPException(status_code=503, detail=str(e))
