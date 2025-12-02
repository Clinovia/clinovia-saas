from sqlalchemy.orm import Session
from sqlalchemy import func, cast, String
from datetime import datetime, timedelta
from app.db.models.assessments import Assessment
from app.schemas.analytics import (
    ModelPerformanceResponse,
    AssessmentStatsResponse,
    UserActivityResponse
)


class ReportingService:
    def __init__(self, db: Session):
        self.db = db

    def get_model_performance(self) -> ModelPerformanceResponse:
        """Get model performance statistics"""
        # Query all assessments (filter in Python for compatibility)
        assessments = self.db.query(Assessment).all()
        
        # Filter completed assessments in Python
        completed_assessments = [
            a for a in assessments 
            if isinstance(a.result, dict) and a.result.get("status") == "complete"
        ]

        total_completed = len(completed_assessments)
        by_model = {}
        confidence_scores = []

        for assessment in completed_assessments:
            # Use algorithm_version instead of model_name (based on your Assessment model)
            model = assessment.algorithm_version or "unknown"
            by_model[model] = by_model.get(model, 0) + 1

            # Extract confidence from result JSON
            if assessment.result and isinstance(assessment.result, dict):
                confidence = assessment.result.get("confidence")
                if confidence is not None:
                    confidence_scores.append(confidence)

        average_confidence = (
            sum(confidence_scores) / len(confidence_scores)
            if confidence_scores
            else 0.0
        )

        return ModelPerformanceResponse(
            total_completed=total_completed,
            by_model=by_model,
            average_confidence=average_confidence
        )

    def get_assessment_stats(self, days: int = 30) -> AssessmentStatsResponse:
        """Get assessment statistics for a given time period"""
        start_date = datetime.utcnow() - timedelta(days=days)

        assessments = self.db.query(Assessment).filter(
            Assessment.created_at >= start_date
        ).all()

        total_assessments = len(assessments)
        by_type = {}

        for assessment in assessments:
            assessment_type = str(assessment.type.value) if hasattr(assessment.type, 'value') else str(assessment.type)
            by_type[assessment_type] = by_type.get(assessment_type, 0) + 1

        return AssessmentStatsResponse(
            total_assessments=total_assessments,
            by_type=by_type,
            date_range_days=days
        )

    def get_user_activity(self, days: int = 30) -> UserActivityResponse:
        """Get user activity statistics"""
        start_date = datetime.utcnow() - timedelta(days=days)

        # Get unique active users (patients who completed assessments)
        active_assessments = self.db.query(Assessment).filter(
            Assessment.created_at >= start_date
        ).all()

        unique_users = set()
        for assessment in active_assessments:
            if assessment.patient_id:
                unique_users.add(assessment.patient_id)

        total_users = len(unique_users)
        active_users = total_users  # For now, all users with assessments are considered active

        return UserActivityResponse(
            total_users=total_users,
            active_users=active_users,
            date_range_days=days
        )