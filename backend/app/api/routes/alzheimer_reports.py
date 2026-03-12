from datetime import datetime
from typing import Optional, List, Dict

from fastapi import APIRouter, Depends, Query

from app.services.alzheimer.reports_service import AlzheimerReportsService
from app.api.deps import CurrentUser


router = APIRouter(
    prefix="/alzheimer/reports",
    tags=["Alzheimer Reports"]
)


@router.get("/", response_model=List[Dict])
def get_reports(
    current_user: CurrentUser,
    start_date: Optional[datetime] = Query(default=None),
    end_date: Optional[datetime] = Query(default=None),
    service: AlzheimerReportsService = Depends(),
) -> List[Dict]:
    """
    Retrieve Alzheimer clinical reports for the authenticated clinician.
    """

    return service.get_reports(
        clinician_id=current_user.id,
        start_date=start_date,
        end_date=end_date,
    )