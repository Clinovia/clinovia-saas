# backend/app/services/pdf_engine/clinical_sections.py
def build_metadata_section(assessment: dict):
    """
    Convert assessment metadata into a table.
    """

    return [
        ["Assessment ID", assessment.get("id", "—")],
        ["Specialty", assessment.get("specialty", "—")],
        ["Assessment Type", assessment.get("assessment_type", "—")],
        ["Model", assessment.get("model_name", "—")],
        ["Model Version", assessment.get("model_version", "—")],
        ["Status", assessment.get("status", "—")],
        ["Clinician ID", assessment.get("clinician_id", "—")],
        ["Patient ID", assessment.get("patient_id", "—")],
    ]


def build_clinical_interpretation(assessment_type: str, output_data: dict):

    if not assessment_type:
        return None

    assessment_type = assessment_type.upper()

    # --------------------------------------------------
    # Alzheimer Diagnosis
    # --------------------------------------------------

    if "ALZHEIMER_DIAGNOSIS" in assessment_type:

        prediction = output_data.get("prediction")
        probability = output_data.get("probability")

        if prediction is None:
            return None

        text = f"The model predicts <b>{prediction}</b>."

        if probability is not None:
            text += f" Estimated probability: {round(probability * 100, 1)}%."

        text += (
            " This estimate reflects patterns learned from clinical datasets "
            "and should be interpreted in conjunction with full clinical "
            "assessment and diagnostic workup."
        )

        return text

    # --------------------------------------------------
    # Alzheimer Prognosis
    # --------------------------------------------------

    if "PROGNOSIS" in assessment_type:

        risk = output_data.get("risk_group")

        if risk:

            return (
                f"The patient falls into the <b>{risk}</b> progression risk category. "
                "This estimate reflects predicted cognitive decline risk "
                "within the modeled time horizon."
            )

    return None