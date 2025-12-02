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
    additional_dependencies: list = None,
):
    """
    Generic endpoint generator for clinical assessments WITHOUT patient_id.
    
    Functionality:
    ---------------------------
    ✔ No patient_id required
    ✔ No patient lookup
    ✔ No owner/clinician authorization check
    ✔ Runs assessment service function
    ✔ Persists results with patient_id=None
    ✔ Returns structured output
    """

    @router.post(path, response_model=output_schema, status_code=status.HTTP_200_OK)
    async def assessment_endpoint(
        input_data: input_schema,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        try:
            # ================================================================
            # 1. Execute Assessment Service
            # ================================================================
            result = service_function(
                input_data=input_data,
                current_user=current_user,
                db=db,
            )

            # ================================================================
            # 2. Normalize response to dictionary with JSON serialization
            # ================================================================
            if isinstance(result, dict):
                result_dict = result
            elif hasattr(result, "model_dump"):
                result_dict = result.model_dump(mode='json')  # ✅ Added mode='json'
            elif hasattr(result, "dict"):
                result_dict = result.dict()
            else:
                result_dict = dict(result)

            # ================================================================
            # 3. Persist to Database (patient_id = None)
            # ================================================================
            AssessmentRepository(db).create(
                assessment_type=assessment_type,
                patient_id=None,
                clinician_id=current_user.id,
                input_data=input_data.model_dump(mode='json') if hasattr(input_data, "model_dump") else dict(input_data),  # ✅ Added mode='json'
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

    assessment_endpoint.__name__ = f"{assessment_type.value.replace('-', '_')}_endpoint"
    return assessment_endpoint