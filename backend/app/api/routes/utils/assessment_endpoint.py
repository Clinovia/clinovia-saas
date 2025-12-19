"""
Generic assessment endpoint factory.
Creates standardized REST endpoints for clinical assessments
WITHOUT requiring patient_id.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Type, Callable

from app.api.deps import get_current_user, get_db
from app.db.models.users import User
from app.db.models.assessments import AssessmentType
from app.db.repositories.assessment_repository import AssessmentRepository
from app.schemas.base import AssessmentInputSchema, AssessmentOutputSchema


def create_assessment_endpoint(
    *,
    path: str,
    input_schema: Type[AssessmentInputSchema],
    output_schema: Type[AssessmentOutputSchema],
    service_function: Callable,
    assessment_type: AssessmentType,
    router: APIRouter,
):
    """
    Generic endpoint generator for clinician-owned assessments.

    Characteristics
    ---------------------------
    ✔ Authenticated clinician required
    ✔ No patient_id required
    ✔ No patient lookup
    ✔ Runs assessment service
    ✔ Persists assessment with:
        - clinician_id = current_user.id
        - patient_id = None
    ✔ Returns structured response
    """

    @router.post(
        path,
        response_model=output_schema,
        status_code=status.HTTP_200_OK,
    )
    async def assessment_endpoint(
        input_data: input_schema,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        try:
            # ================================================================
            # 1. Run Assessment Service
            # ================================================================
            result = service_function(
                input_data=input_data,
                db=db,
                clinician_id=current_user.id,
            )

            # ================================================================
            # 2. Normalize result to JSON-safe dict
            # ================================================================
            if isinstance(result, dict):
                result_dict = result
            elif hasattr(result, "model_dump"):
                result_dict = result.model_dump(mode="json")
            elif hasattr(result, "dict"):
                result_dict = result.dict()
            else:
                result_dict = dict(result)

            # ================================================================
            # 3. Persist Assessment (patient_id = None)
            # ================================================================
            AssessmentRepository(db).create(
                assessment_type=assessment_type,
                clinician_id=current_user.id,
                patient_id=None,
                input_data=input_data.model_dump(mode="json"),
                result=result_dict,
                algorithm_version="v1.0",
            )

            return result

        except HTTPException:
            raise
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"{assessment_type.value} assessment failed: {str(e)}",
            )

    assessment_endpoint.__name__ = (
        f"{assessment_type.value.replace('-', '_')}_endpoint"
    )

    return assessment_endpoint
