# Data Handling Policy

## 1. Data Collection
- Only **de-identified clinical data** is accepted
- Required fields: age, sex, biomarkers (no names, MRNs, SSNs)
- Users must confirm data is de-identified before submission

## 2. Data Storage
| Data Type | Location | Retention | Encryption |
|-----------|----------|-----------|------------|
| Prediction Logs | AWS RDS | 7 years | AES-256 |
| Input/Output Files | AWS S3 | 30 days | AES-256 |
| User Accounts | Clerk | Until deletion | AES-256 |

## 3. Data Deletion
- Users can request deletion via `DELETE /account`
- Data purged from S3 within 24 hours
- Audit logs retained per legal requirements

## 4. Third Parties
- **Clerk**: Auth only (BAA signed)
- **AWS**: Infrastructure (BAA signed)
- **No other third parties** receive data