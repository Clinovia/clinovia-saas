
---

### ✅ 3. `docs/compliance/hipaa-checklist.md`
```md
# HIPAA Compliance Checklist

## ✅ Implemented
| Requirement | Status | Details |
|-------------|--------|---------|
| **BAAs Signed** | ✅ | Clerk, AWS, Vercel |
| **Data Encryption** | ✅ | AES-256 at rest (S3/RDS), TLS 1.3 in transit |
| **Access Controls** | ✅ | Org-based isolation, RBAC |
| **Audit Logs** | ✅ | All predictions logged (user, org, model) |
| **Data Minimization** | ✅ | No PHI stored; only de-identified inputs |
| **Secure Auth** | ✅ | Clerk (MFA, SSO, session management) |
| **Vulnerability Scans** | ✅ | AWS Inspector, Snyk for deps |

## 🚧 In Progress
| Requirement | Target Date |
|-------------|-------------|
| Penetration Testing | Q3 2024 |
| Annual Risk Assessment | Q4 2024 |

## 📌 Notes
- **All AWS services** used are [HIPAA-eligible](https://aws.amazon.com/compliance/hipaa-eligible-services-reference/)
- **Clerk** provides signed BAA for auth
- **Vercel** provides BAA for frontend hosting