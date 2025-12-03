// frontend/types/cardiology.ts

// ======================
// 1. ASCVD Risk
// ======================
export interface ASCVDInput {
  patient_id?: string | number | null;
  age: number; // 40-79
  gender: "male" | "female";
  race: "white" | "black" | "hispanic" | "asian" | "other";
  total_cholesterol: number; // 130-320
  hdl_cholesterol: number; // 20-100
  systolic_bp: number; // 90-200
  on_hypertension_treatment: boolean;
  smoker: boolean;
  diabetes: boolean;
}

export interface ASCVDOutput {
  patient_id?: string | number | null;
  risk_percentage: number; // 0-100
  risk_category: "low" | "borderline" | "intermediate" | "high";
  model_name: string; // default: "ascvd_rule_v1"
}

// ======================
// 2. Blood Pressure Category
// ======================
export interface BPCategoryInput {
  patient_id?: string | number | null;
  systolic_bp: number; // 70-250
  diastolic_bp: number; // 40-150
}

export interface BPCategoryOutput {
  patient_id?: string | number | null;
  category:
    | "normal"
    | "elevated"
    | "hypertension_stage_1"
    | "hypertension_stage_2"
    | "hypertensive_crisis";
  model_name: string; // default: "bp_category_rule_v1"
}

// ======================
// 3. CHA₂DS₂-VASc Score
// ======================
export interface CHA2DS2VAScInput {
  patient_id?: string | number | null;
  age: number; // 18-120
  gender: "male" | "female";
  congestive_heart_failure: boolean;
  hypertension: boolean;
  diabetes: boolean;
  stroke_tia_thromboembolism: boolean;
  vascular_disease: boolean;
}

export interface CHA2DS2VAScOutput {
  patient_id?: string | number | null;
  score: number; // 0-9
  risk_category: "low" | "moderate" | "high";
  model_name: string; // default: "cha2ds2vasc_rule_v1"
}

// ======================
// 4. ECG Interpreter
// ======================
export interface ECGInterpreterInput {
  patient_id?: string | number | null;
  heart_rate: number; // 20-300
  qrs_duration: number; // 50-200
  qt_interval?: number; // 300-600
  pr_interval?: number; // 80-400
  rhythm: "sinus" | "afib" | "flutter" | "other";
  st_elevation?: boolean; // default false
  t_wave_inversion?: boolean; // default false
}

export interface ECGInterpreterOutput {
  patient_id?: string | number | null;
  findings: Array<
    | "normal"
    | "sinus_tachycardia"
    | "sinus_bradycardia"
    | "afib"
    | "lvh"
    | "st_elevation"
    | "t_wave_abnormality"
    | "prolonged_qt"
  >;
  rhythm: string;
  overall_risk: "routine" | "urgent" | "emergent";
  model_name: string; // default: "ecg_interpreter_rule_v1"
  model_version: string;
}

// ======================
// 5. Echonet EF Prediction
// ======================
export interface EchonetEFInput {
  video_file: File; // file path or base64 depending on uploader
}

export interface EchonetEFOutput {
  ef_percent?: number; // 0–100
  category: string; // "Normal", "Mildly Reduced", etc.
  model_name: string; // "echonet_ef_model"
  model_version: string; // "1.0.0"
}
