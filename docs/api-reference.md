# API Reference

Base URL: `https://api.clinovia.com`

## Authentication
- All requests require a **valid Clerk session cookie**
- No API keys needed

## Cardiology Endpoints

### POST /cardiology/predict/ascvd
**Request**
```json
{
  "age": 55,
  "sex": "male",
  "race": "white",
  "total_cholesterol": 210,
  "hdl_cholesterol": 50,
  "systolic_bp": 125,
  "on_hypertension_treatment": false,
  "smoker": true,
  "diabetic": false
}