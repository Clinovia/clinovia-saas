# Data Flow

## Overview
All data flows are **de-identified** and **encrypted in transit/at rest**. No PHI is stored.

## User → System
1. User authenticates via **Clerk** (SSO supported)
2. Frontend sends de-identified clinical data to backend
3. Backend validates → runs prediction → logs audit trail
4. Result returned to frontend

## Prediction Workflow
```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant Model
    participant DB

    User->>Frontend: Enters de-identified data
    Frontend->>Backend: POST /predict (with auth token)
    Backend->>Backend: Validate input
    Backend->>Model: Run inference
    Model-->>Backend: Return prediction
    Backend->>DB: Log audit trail (org_id, prediction_id, model)
    Backend-->>Frontend: Return result
    Frontend-->>User: Display risk score