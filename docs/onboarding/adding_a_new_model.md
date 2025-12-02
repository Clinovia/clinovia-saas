# Adding a New AI Model

Follow this checklist to add a new clinical AI model to Clinovia SaaS.

## Step 1: Clinical Validation
- [ ] Model validated on external dataset
- [ ] Performance metrics documented (AUC, PPV, etc.)
- [ ] Regulatory path confirmed (research-use vs. diagnostic)

## Step 2: Backend Implementation
1. **Add model artifacts**  
   `backend/app/clinical/alzheimer/{new_model}/`
   - `model.pkl` or `.joblib`
   - `inference.py` (pure function)
   - `utils.py` (preprocessing)

2. **Create schema**  
   `backend/app/schemas/{new_model}.py`
   - Input/Output models
   - Validation rules

3. **Add service**  
   `backend/app/services/{new_model}_service.py`
   - Call inference
   - Log audit trail

4. **Add API route**  
   `backend/app/api/routes/{new_model}.py`
   - POST endpoint
   - Error handling

## Step 3: Frontend Implementation
1. **Add TypeScript types**  
   `frontend/types/{new_model}.ts`

2. **Create dashboard component**  
   `frontend/app/dashboard/components/{NewModel}Results.tsx`

3. **Update dashboard page**  
   Add to `frontend/app/dashboard/page.tsx`

## Step 4: Documentation
- [ ] Update `docs/data-schema.md`
- [ ] Add to `docs/api-reference.md`
- [ ] Create model-specific validation guide

## Example PR Structure