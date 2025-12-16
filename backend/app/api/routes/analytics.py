from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from app.api.deps import (
    CurrentUser,
    ReportingServiceDep,
    UsageAnalyticsServiceDep,
)
from app.schemas.analytics import (
    UsageEventCreate,
    UsageSummaryResponse,
    ReportRequest,
    ReportResponse,
    ReportListResponse,
    StandardResponse,
)

router = APIRouter(tags=["Analytics"])

# ===============================
# Usage Tracking
# ===============================

@router.post("/track", status_code=status.HTTP_201_CREATED, response_model=StandardResponse)
async def track_usage(
    event: UsageEventCreate,
    current_user: CurrentUser,
    usage_service: UsageAnalyticsServiceDep,
):
    """Record an API usage event for the current user."""
    try:
        usage_service.record_event(
            user_id=current_user.id,
            endpoint=event.endpoint,
            status=event.status,
        )
        return StandardResponse(message="Event recorded successfully")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to record event: {str(e)}"
        )


@router.get("/summary", response_model=UsageSummaryResponse)
async def get_my_usage_summary(
    current_user: CurrentUser,
    usage_service: UsageAnalyticsServiceDep,
):
    """Retrieve usage summary for the current user."""
    summary = usage_service.get_usage_summary(user_id=current_user.id)
    return UsageSummaryResponse(summary=summary)


@router.get("/summary/{user_id}", response_model=UsageSummaryResponse)
async def get_user_usage_summary(
    user_id: UUID,
    current_user: CurrentUser,
    usage_service: UsageAnalyticsServiceDep,
):
    """Retrieve usage summary for any user (no admin check yet)."""
    summary = usage_service.get_usage_summary(user_id=user_id)
    return UsageSummaryResponse(summary=summary)


# ===============================
# Reporting (Admin Only placeholder)
# ===============================

@router.post("/report", response_model=ReportResponse)
async def generate_report(
    report_request: ReportRequest,
    current_user: CurrentUser,
    usage_service: UsageAnalyticsServiceDep,
    reporting_service: ReportingServiceDep,
):
    """Generate a usage and revenue report (no admin check yet)."""
    try:
        usage_data = usage_service.get_all_usage_data(
            start_date=report_request.start_date,
            end_date=report_request.end_date
        )
        revenue_data = reporting_service.get_revenue_data(
            start_date=report_request.start_date,
            end_date=report_request.end_date
        )
        report = reporting_service.generate_report(
            usage_data=usage_data,
            revenue_data=revenue_data,
            start_date=report_request.start_date,
            end_date=report_request.end_date,
            report_type=report_request.report_type
        )
        return ReportResponse(report=report)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/reports", response_model=ReportListResponse)
async def list_reports(
    current_user: CurrentUser,
    reporting_service: ReportingServiceDep,
):
    """List all previously generated reports (no admin check yet)."""
    reports = reporting_service.list_reports()
    return ReportListResponse(reports=reports, total=len(reports))


@router.get("/reports/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: str,
    current_user: CurrentUser,
    reporting_service: ReportingServiceDep,
):
    """Retrieve a specific report by ID (no admin check yet)."""
    report = reporting_service.get_report_by_id(report_id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report with ID {report_id} not found"
        )
    return ReportResponse(report=report)


@router.delete("/reports/{report_id}", response_model=StandardResponse)
async def delete_report(
    report_id: str,
    current_user: CurrentUser,
    reporting_service: ReportingServiceDep,
):
    """Delete a specific report by ID (no admin check yet)."""
    success = reporting_service.delete_report(report_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report with ID {report_id} not found"
        )
    return StandardResponse(message=f"Report {report_id} deleted successfully")
