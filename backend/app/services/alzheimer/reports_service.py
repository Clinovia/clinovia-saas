from typing import Dict

from app.services.reports.base_reports_service import BaseReportsService


# -----------------------------------------------------
# Summary Builders
# -----------------------------------------------------

def diagnosis_summary(output: Dict) -> Dict:
    return {
        "diagnosis": (
            output.get("risk_category")
            or output.get("diagnosis")
            or output.get("classification")
        )
    }


def prognosis_summary(output: Dict) -> Dict:
    return {
        "risk_category": output.get("risk_category"),
        "progression_probability": output.get("progression_probability"),
    }


def screening_summary(output: Dict) -> Dict:
    return {
        "risk_flag": output.get("risk_flag"),
        "risk_score": output.get("risk_score"),
    }


# -----------------------------------------------------
# Service
# -----------------------------------------------------

class AlzheimerReportsService(BaseReportsService):

    SPECIALTY = "alzheimer"

    SUMMARY_BUILDERS = {
        "ALZHEIMER_DIAGNOSIS_BASIC": diagnosis_summary,
        "ALZHEIMER_DIAGNOSIS_EXTENDED": diagnosis_summary,
        "ALZHEIMER_DIAGNOSIS_SCREENING": screening_summary,
        "ALZHEIMER_PROGNOSIS_2YR_BASIC": prognosis_summary,
        "ALZHEIMER_PROGNOSIS_2YR_EXTENDED": prognosis_summary,
    }