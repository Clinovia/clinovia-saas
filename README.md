# Clinovia SaaS

**Enterprise AI Platform for Cardiovascular & Neurodegenerative Risk Assessment**  
Trusted by hospitals, CROs, and academic centers for clinical decision support.

![Clinovia Architecture](docs/architecture/system-diagram.png)

## 🌟 Key Features
- **Two Clinical Domains**:  
  - 🫀 **Cardiology**: ASCVD, BP Category, CHA₂DS₂-VASc, ECG Interpreter  
  - 🧠 **Neurology**: Alzheimer’s Cognitive Status Classifier (CN/MCI/AD)
- **Enterprise-Ready**:  
  - HIPAA-compliant (BAA with AWS, Clerk, Vercel)  
  - Organization-based isolation  
  - Audit-safe prediction logging  
- **Flexible Engagement**:  
  - Paid Pilot Program (quick validation)  
  - Precision Insights Consulting (deep analysis)

## 🛠️ Tech Stack
| Layer | Technology |
|-------|------------|
| **Frontend** | Next.js 14 (App Router), TypeScript, Tailwind CSS |
| **Backend** | FastAPI, Python 3.11, PostgreSQL |
| **AI/ML** | XGBoost, Clinical Rules Engine |
| **Auth** | Clerk (HIPAA BAA, SSO, MFA) |
| **Infra** | AWS (ECS Fargate, RDS, S3), Docker |
| **Compliance** | HIPAA, GDPR-ready |

## 🚀 Getting Started

### Prerequisites
- Docker 24+
- Node.js 18+
- Python 3.11+

### Local Development
1. **Clone repo**
   ```bash
   git clone https://github.com/your-org/clinovia-saas.git
   cd clinovia-saas```