from pydantic import BaseModel, Field, model_validator
from typing import Optional, Dict, List, Literal
from datetime import date, datetime
from enum import Enum


# ===============================
# Shared Types
# ===============================

ResponseStatus = Literal["success"]  # Extend to ["success", "error"] if needed later


# ===============================
# Enums
# ===============================

class ReportType(str, Enum):
    """Valid report types"""
    USAGE = "usage"
    REVENUE = "revenue"
    COMBINED = "combined"


# ===============================
# Usage Tracking
# ===============================

class UsageEventCreate(BaseModel):
    """Schema for creating a usage event"""
    endpoint: str = Field(
        ..., 
        min_length=1, 
        max_length=500, 
        description="API endpoint path (must start with /)"
    )
    status: str = Field(
        ..., 
        min_length=1, 
        max_length=50, 
        description="Request status (e.g., success, error)"
    )
    
    @model_validator(mode='before')
    @classmethod
    def normalize_status(cls, data):
        if isinstance(data, dict) and 'status' in data:
            data['status'] = data['status'].lower()
        return data

    @model_validator(mode='after')
    def validate_endpoint_starts_with_slash(self):
        if not self.endpoint.startswith('/'):
            raise ValueError("Endpoint must start with '/'")
        return self

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "endpoint": "/api/generate",
                    "status": "success"
                }
            ]
        }
    }


# ===============================
# Usage Summary
# ===============================

class UsageSummaryData(BaseModel):
    """Structured usage summary data"""
    total_requests: int = Field(..., ge=0)
    success_count: int = Field(..., ge=0)
    failure_count: int = Field(..., ge=0)
    endpoint_breakdown: Dict[str, int] = Field(default_factory=dict)
    status_breakdown: Dict[str, int] = Field(default_factory=dict)

class UsageSummaryResponse(BaseModel):
    """Schema for usage summary response"""
    status: ResponseStatus = "success"
    summary: UsageSummaryData

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "success",
                    "summary": {
                        "total_requests": 150,
                        "success_count": 145,
                        "failure_count": 5,
                        "endpoint_breakdown": {
                            "/api/generate": 100,
                            "/api/analyze": 50
                        },
                        "status_breakdown": {
                            "success": 145,
                            "error": 5
                        }
                    }
                }
            ]
        }
    }


# ===============================
# Reporting Requests & Metadata
# ===============================

class ReportRequest(BaseModel):
    """Schema for requesting a report"""
    start_date: Optional[date] = Field(
        None, 
        description="Start date for the report (YYYY-MM-DD)"
    )
    end_date: Optional[date] = Field(
        None, 
        description="End date for the report (YYYY-MM-DD)"
    )
    report_type: ReportType = Field(
        default=ReportType.COMBINED,
        description="Type of report: usage, revenue, or combined"
    )

    @model_validator(mode='after')
    def validate_dates(self):
        today = date.today()
        if self.start_date and self.start_date > today:
            raise ValueError("start_date cannot be in the future")
        if self.end_date and self.end_date > today:
            raise ValueError("end_date cannot be in the future")
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError("end_date must be after or equal to start_date")
        return self

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "start_date": "2025-01-01",
                    "end_date": "2025-01-31",
                    "report_type": "combined"
                }
            ]
        }
    }


# ===============================
# Report Data Structures
# ===============================

class UsageReportData(BaseModel):
    total_requests: int
    by_endpoint: Dict[str, int]
    by_status: Dict[str, int]

class RevenueReportData(BaseModel):
    total_usd: float
    by_tier: Dict[str, float]

class CombinedReportData(BaseModel):
    usage: UsageReportData
    revenue: RevenueReportData

class ReportContent(BaseModel):
    """Union-like container for report content (discriminated by report_type in practice)"""
    report_id: str
    generated_at: str  # ISO 8601 string
    type: ReportType
    period: Dict[str, str]  # e.g., {"start": "2025-01-01", "end": "2025-01-31"}
    usage: Optional[UsageReportData] = None
    revenue: Optional[RevenueReportData] = None

class ReportResponse(BaseModel):
    """Schema for report response"""
    status: ResponseStatus = "success"
    report: ReportContent

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "success",
                    "report": {
                        "report_id": "report_123",
                        "generated_at": "2025-01-15T10:30:00Z",
                        "period": {
                            "start": "2025-01-01",
                            "end": "2025-01-31"
                        },
                        "type": "combined",
                        "usage": {
                            "total_requests": 1000,
                            "by_endpoint": {
                                "/api/generate": 600,
                                "/api/analyze": 400
                            },
                            "by_status": {
                                "success": 950,
                                "error": 50
                            }
                        },
                        "revenue": {
                            "total_usd": 5000.00,
                            "by_tier": {
                                "free": 0.0,
                                "pro": 3000.0,
                                "enterprise": 2000.0
                            }
                        }
                    }
                }
            ]
        }
    }


# ===============================
# Report Listing
# ===============================

class ReportListItem(BaseModel):
    """Schema for a single report in the list"""
    report_id: str = Field(..., description="Unique report identifier")
    generated_at: datetime = Field(..., description="When the report was generated")
    report_type: ReportType = Field(..., description="Type of report")
    period_start: Optional[date] = Field(None, description="Report start date")
    period_end: Optional[date] = Field(None, description="Report end date")
    generated_by: str = Field(..., description="User ID who generated the report")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "report_id": "report_123",
                    "generated_at": "2025-01-15T10:30:00Z",
                    "report_type": "combined",
                    "period_start": "2025-01-01",
                    "period_end": "2025-01-31",
                    "generated_by": "admin_user_id"
                }
            ]
        }
    }


class ReportListResponse(BaseModel):
    """Schema for listing reports response"""
    status: ResponseStatus = "success"
    reports: List[ReportListItem] = Field(default_factory=list)
    total: int = Field(..., ge=0)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "success",
                    "reports": [
                        {
                            "report_id": "report_123",
                            "generated_at": "2025-01-15T10:30:00Z",
                            "report_type": "combined",
                            "period_start": "2025-01-01",
                            "period_end": "2025-01-31",
                            "generated_by": "admin_user_id"
                        }
                    ],
                    "total": 1
                }
            ]
        }
    }


# ===============================
# Standard Responses
# ===============================

class StandardResponse(BaseModel):
    """Standard response schema for simple operations"""
    status: ResponseStatus = "success"
    message: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "success",
                    "message": "Event recorded successfully"
                }
            ]
        }
    }


# ===============================
# Advanced Analytics (Model & User Stats)
# ===============================

class ModelPerformanceResponse(BaseModel):
    """Schema for model performance statistics"""
    total_completed: int = Field(..., ge=0)
    by_model: Dict[str, int] = Field(default_factory=dict)
    average_confidence: float = Field(..., ge=0.0, le=1.0)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "total_completed": 150,
                    "by_model": {
                        "gpt-4": 90,
                        "claude-3": 60
                    },
                    "average_confidence": 0.87
                }
            ]
        }
    }


class AssessmentStatsResponse(BaseModel):
    """Schema for assessment statistics"""
    total_assessments: int = Field(..., ge=0)
    by_type: Dict[str, int] = Field(default_factory=dict)
    date_range_days: int = Field(default=30, ge=1)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "total_assessments": 250,
                    "by_type": {
                        "alzheimer_diagnosis": 100,
                        "alzheimer_risk_screener": 50,
                        "cardiology_ascvd": 60,
                        "cardiology_bp_categories": 40
                    },
                    "date_range_days": 30
                }
            ]
        }
    }


class UserActivityResponse(BaseModel):
    """Schema for user activity statistics"""
    total_users: int = Field(..., ge=0)
    active_users: int = Field(..., ge=0)
    date_range_days: int = Field(default=30, ge=1)
    assessments_per_user: Optional[float] = Field(None, ge=0.0)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "total_users": 45,
                    "active_users": 38,
                    "date_range_days": 30,
                    "assessments_per_user": 5.6
                }
            ]
        }
    }