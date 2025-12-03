// frontend/features/alzheimer/types.ts

// ==========================================================
// Shared Types
// ==========================================================
export type Gender = "male" | "female";
export type Race = 1 | 2 | 3 | 4 | 5 | 6 | 7;
export type AlzheimerClass = "CN" | "MCI" | "AD";
export type RiskCategory = "low" | "moderate" | "high";

// ==========================================================
// Alzheimer Diagnosis (Screening)
// ==========================================================
export interface AlzheimerDiagnosisScreeningInput {
  patient_id?: string | number | null;
  age: number; // 55 - 95
  education_years: number; // 0 - 30
  moca_score: number; // 0 - 30
  adas13_score: number; // 0 - 85
  cdr_sum: number; // 0 - 18
  faq_total: number; // 0 - 30
  gender: Gender;
  race: Race;
}

export interface AlzheimerDiagnosisScreeningOutput {
  patient_id?: string | number | null;
  model_name: string; // e.g., "alz-diagnosis-xgboost-adni.joblib"
  model_version: string; // e.g., "1.0.0"
  predicted_class: AlzheimerClass;
  confidence: number; // 0 - 1
  probabilities: Record<AlzheimerClass, number>;
  top_features?: string[] | null;
}

// ==========================================================
// Alzheimer Risk Screener
// ==========================================================
export interface AlzheimerRiskScreenerInput {
  patient_id?: string | number | null;
  age: number;
  gender: Gender;
  education_years: number;
  apoe4_status: boolean;
  memory_score: number; // MoCA-like
  hippocampal_volume?: number | null;
}

export interface AlzheimerRiskScreenerOutput {
  patient_id?: string | number | null;
  model_name: string;
  model_version: string;
  risk_category: RiskCategory;
  recommendation: string;
}

// ==========================================================
// Alzheimer Diagnosis Basic
// ==========================================================
export interface AlzheimerDiagnosisBasicInput {
  patient_id?: string | number | null;
  AGE: number;
  MMSE_bl: number;
  CDRSB_bl: number;
  FAQ_bl: number;
  PTEDUCAT: number;
  PTGENDER: string; // "male" | "female"
  APOE4: number; // -1, 0, 1, or 2
  RAVLT_immediate_bl: number;
  MOCA_bl: number;
  ADAS13_bl: number;
}

export interface AlzheimerDiagnosisBasicOutput {
  patient_id?: string | number | null;
  model_name: string;
  model_version: string;
  predicted_class: AlzheimerClass;
  confidence: number;
  probabilities: Record<AlzheimerClass, number>;
  top_features?: string[] | null;
}

// ==========================================================
// Alzheimer Diagnosis Extended
// ==========================================================
export interface AlzheimerDiagnosisExtendedInput
  extends AlzheimerDiagnosisBasicInput {
  Hippocampus_bl?: number | null;
  Ventricles_bl?: number | null;
  WholeBrain_bl?: number | null;
  Entorhinal_bl?: number | null;
  FDG_bl?: number | null;
  AV45_bl?: number | null;
  PIB_bl?: number | null;
  FBB_bl?: number | null;
  ABETA_bl?: number | null;
  TAU_bl?: number | null;
  PTAU_bl?: number | null;
  mPACCdigit_bl?: number | null;
  mPACCtrailsB_bl?: number | null;
}

export interface AlzheimerDiagnosisExtendedOutput
  extends AlzheimerDiagnosisBasicOutput {}

// ==========================================================
// 2-Year Prognosis Models (Refactored + Organized)
// ==========================================================

// -----------------------------
// Common 8 shared features
// -----------------------------
interface AlzheimerPrognosis2yrCommonFeatures {
  patient_id?: string | number | null;
  AGE: number;
  PTGENDER: Gender;
  PTEDUCAT: number;

  ADAS13: number;
  CDRSB: number;
  FAQ: number;

  APOE4_count: 0 | 1 | 2;
  GDTOTAL: number;
}

// ==========================================================
// 2-Year Prognosis BASIC (includes MOCA, no biomarkers)
// ==========================================================
export interface AlzheimerPrognosis2yrBasicInput
  extends AlzheimerPrognosis2yrCommonFeatures {
  MOCA: number; // **Basic-only**
}

export interface AlzheimerPrognosis2yrBasicOutput {
  patient_id?: string | number | null;
  model_name?: string;
  model_version?: string;

  // Expressive probability fields
  probability_progression_to_AD_within_2yrs: number; // 0–1
  probability_stable_within_2yrs: number; // 0–1

  // Risk category: "low" | "moderate" | "high"
  risk_level: string;

  // Human-readable summary
  summary_text: string;

  // Feature importance (optional)
  top_features?: string[] | null;

  // Error handling
  error?: string | null;
}

// ==========================================================
// 2-Year Prognosis EXTENDED (biomarkers, no MOCA)
// ==========================================================
export interface AlzheimerPrognosis2yrExtendedInput
  extends AlzheimerPrognosis2yrCommonFeatures {
  ABETA: number | null; // **Extended-only**
  TAU: number | null;   // **Extended-only**
  PTAU: number | null;  // **Extended-only**
}

export interface AlzheimerPrognosis2yrExtendedOutput
  extends AlzheimerPrognosis2yrBasicOutput {}
