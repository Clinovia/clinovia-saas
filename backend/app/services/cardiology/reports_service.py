from typing import Dict

from app.services.reports.base_reports_service import BaseReportsService


# -----------------------------------------------------
# Summary Builders
# -----------------------------------------------------

def ascvd_summary(output: Dict) -> Dict:
    return {
        "risk_score": output.get("risk_score"),
        "risk_level": output.get("risk_level"),
    }


def bp_summary(output: Dict) -> Dict:
    return {
        "bp_category": output.get("category"),
    }


def cha2ds2vasc_summary(output: Dict) -> Dict:
    return {
        "score": output.get("score"),
        "stroke_risk": output.get("risk_level"),
    }


def ecg_summary(output: Dict) -> Dict:
    return {
        "prediction": output.get("prediction"),
        "confidence": output.get("confidence"),
    }


# -----------------------------------------------------
# Service
# -----------------------------------------------------

class CardioReportsService(BaseReportsService):

    SPECIALTY = "cardiology"

    SUMMARY_BUILDERS = {
        "CARDIOLOGY_ASCVD": ascvd_summary,
        "CARDIOLOGY_BP": bp_summary,
        "CARDIOLOGY_CHA2DS2VASc": cha2ds2vasc_summary,
        "CARDIOLOGY_ECG": ecg_summary,
    }