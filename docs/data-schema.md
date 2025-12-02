
---

### ✅ 6. `docs/data-schema.md`
```md
# Data Schema

## Cardiology

### ASCVD Input
| Field | Type | Range | Required |
|-------|------|-------|----------|
| age | integer | 40-79 | ✅ |
| sex | string | "male", "female" | ✅ |
| race | string | "white", "black", "hispanic", "asian", "other" | ✅ |
| total_cholesterol | number | 130-320 | ✅ |
| hdl_cholesterol | number | 20-100 | ✅ |
| systolic_bp | number | 90-200 | ✅ |
| on_hypertension_treatment | boolean | - | ✅ |
| smoker | boolean | - | ✅ |
| diabetic | boolean | - | ✅ |

### ASCVD Output
| Field | Type | Description |
|-------|------|-------------|
| risk_percentage | number | 0.0-100.0 |
| risk_category | string | "low", "intermediate", "high" |

## Alzheimer

### Input
| Field | Type | Range | Required |
|-------|------|-------|----------|
| age | integer | 50-95 | ✅ |
| education_years | integer | 6-20 | ✅ |
| moca_score | number | 0-30 | ✅ |
| adas13_score | number | 0-70 | ✅ |
| cdr_sum | number | 0-18 | ✅ |
| faq_total | integer | 0-30 | ✅ |
| sex | string | "male", "female" | ✅ |
| ethnicity | string | "hispanic", "not_hispanic" | ✅ |
| race | string | See schema | ✅ |

### Output
| Field | Type | Description |
|-------|------|-------------|
| predicted_class | string | "CN", "MCI", "AD" |
| confidence | number | 0.0-1.0 |
| probabilities | object | {CN: 0.1, MCI: 0.8, AD: 0.1} |