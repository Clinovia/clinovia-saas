from datetime import datetime
from typing import Optional, List, Dict, Callable

from app.repositories.assessments_repository import AssessmentsRepository


class BaseReportsService:
    """
    Base service for building clinical reports.
    """

    SPECIALTY: str = ""
    SUMMARY_BUILDERS: Dict[str, Callable[[Dict], Dict]] = {}

    def __init__(self):
        self.repository = AssessmentsRepository()

    # -----------------------------------------------------
    # Public API
    # -----------------------------------------------------

    def get_reports(
        self,
        clinician_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Dict]:

        rows = self.repository.get_by_specialty(
            clinician_id=clinician_id,
            specialty=self.SPECIALTY,
            start_date=start_date,
            end_date=end_date,
        )

        return [self._build_report(row) for row in rows]

    # -----------------------------------------------------
    # Internal
    # -----------------------------------------------------

    def _build_report(self, row: Dict) -> Dict:

        assessment_type = row.get("assessment_type")
        output_data = row.get("output_data") or {}

        summary_builder = self.SUMMARY_BUILDERS.get(assessment_type)

        summary = summary_builder(output_data) if summary_builder else {}

        return {
            "assessment_id": row.get("id"),
            "assessment_type": assessment_type,
            "patient_id": row.get("patient_id"),
            "model_version": row.get("model_version"),
            "created_at": row.get("created_at"),
            "summary": summary,
        }