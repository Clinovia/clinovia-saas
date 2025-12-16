from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.api.deps import get_db, get_current_user
from app.db.models.users import User
from app.schemas.assessments import AssessmentResponse, AssessmentList
from app.services.assessments.patient_history_service import PatientHistoryService

router = APIRouter()


@router.get("/assessments/history", response_model=AssessmentList)
async def get_assessment_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    assessment_type: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List past assessments for the current user."""
    service = PatientHistoryService(db)
    assessments = service.get_history(
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        assessment_type=assessment_type,
        start_date=start_date,
        end_date=end_date
    )
    total = service.count_history(
        user_id=current_user.id,
        assessment_type=assessment_type,
        start_date=start_date,
        end_date=end_date
    )
    return {"assessments": assessments, "total": total}


@router.get("/assessments/{id}", response_model=AssessmentResponse)
async def get_assessment_by_id(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific assessment by ID."""
    service = PatientHistoryService(db)
    assessment = service.get_history_by_id(id)
    
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Verify ownership - user must be either the patient or the clinician
    is_patient = assessment.patient_id == current_user.id
    is_clinician = assessment.user_id == current_user.id if assessment.user_id else False
    
    if not (is_patient or is_clinician):
        raise HTTPException(status_code=403, detail="Not authorized to access this assessment")
    
    return assessment


@router.delete("/assessments/{id}", status_code=204)
async def delete_assessment(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete an assessment."""
    service = PatientHistoryService(db)
    assessment = service.get_history_by_id(id)
    
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Verify ownership - user must be either the patient or the clinician
    is_patient = assessment.patient_id == current_user.id
    is_clinician = assessment.user_id == current_user.id if assessment.user_id else False
    
    if not (is_patient or is_clinician):
        raise HTTPException(status_code=403, detail="Not authorized to delete this assessment")
    
    service.delete_history(id)
    return None