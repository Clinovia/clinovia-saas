/**
 * API Endpoints Configuration
 * Centralized API endpoint definitions
 */

const API_VERSION = 'v1';
const BASE_PATH = `/api/${API_VERSION}`;

/**
 * Authentication endpoints
 */
export const AUTH_ENDPOINTS = {
  LOGIN: '/api/auth/login',
  SIGNUP: '/api/auth/signup',
  LOGOUT: '/api/auth/logout',
  REFRESH: '/api/auth/refresh',
  FORGOT_PASSWORD: '/api/auth/forgot-password',
  RESET_PASSWORD: '/api/auth/reset-password',
  VERIFY_EMAIL: '/api/auth/verify-email',
} as const;

/**
 * Alzheimer's module endpoints
 */
export const ALZHEIMER_ENDPOINTS = {
  // Diagnosis
  DIAGNOSIS_SCREENING: `${BASE_PATH}/alzheimer/diagnosis-screening`,
  DIAGNOSIS_BASIC: `${BASE_PATH}/alzheimer/diagnosis-basic`,
  DIAGNOSIS_EXTENDED: `${BASE_PATH}/alzheimer/diagnosis-extended`,
  
  // Prognosis
  PROGNOSIS_2YR_BASIC: `${BASE_PATH}/alzheimer/prognosis-2yr-basic`,
  PROGNOSIS_2YR_EXTENDED: `${BASE_PATH}/alzheimer/prognosis-2yr-extended`,
  
  // Risk Assessment
  RISK_SCREENER: `${BASE_PATH}/alzheimer/risk-screener`,
} as const;

/**
 * Cardiology module endpoints
 */
export const CARDIOLOGY_ENDPOINTS = {
  ASCVD: `${BASE_PATH}/cardiology/ascvd`,
  BP_CATEGORY: `${BASE_PATH}/cardiology/bp-category`,
  CHA2DS2_VASC: `${BASE_PATH}/cardiology/cha2ds2vasc`,
  ECG_INTERPRETER: `${BASE_PATH}/cardiology/ecg-interpreter`,
  EF_PREDICTION: `${BASE_PATH}/cardiology/ef-prediction`,
} as const;

/**
 * User/Profile endpoints
 */
export const USER_ENDPOINTS = {
  PROFILE: `${BASE_PATH}/user/profile`,
  UPDATE_PROFILE: `${BASE_PATH}/user/profile`,
  CHANGE_PASSWORD: `${BASE_PATH}/user/change-password`,
  DELETE_ACCOUNT: `${BASE_PATH}/user/delete`,
} as const;

/**
 * Dashboard/Analytics endpoints
 */
export const DASHBOARD_ENDPOINTS = {
  STATS: `${BASE_PATH}/dashboard/stats`,
  RECENT_ASSESSMENTS: `${BASE_PATH}/dashboard/recent`,
  CHARTS: `${BASE_PATH}/dashboard/charts`,
} as const;

/**
 * Report endpoints
 */
export const REPORT_ENDPOINTS = {
  GENERATE: `${BASE_PATH}/reports/generate`,
  LIST: `${BASE_PATH}/reports/list`,
  GET_BY_ID: (id: string) => `${BASE_PATH}/reports/${id}`,
  DOWNLOAD: (id: string) => `${BASE_PATH}/reports/${id}/download`,
  DELETE: (id: string) => `${BASE_PATH}/reports/${id}`,
} as const;

/**
 * All API endpoints grouped
 */
export const API_ENDPOINTS = {
  AUTH: AUTH_ENDPOINTS,
  ALZHEIMER: ALZHEIMER_ENDPOINTS,
  CARDIOLOGY: CARDIOLOGY_ENDPOINTS,
  USER: USER_ENDPOINTS,
  DASHBOARD: DASHBOARD_ENDPOINTS,
  REPORT: REPORT_ENDPOINTS,
} as const;

/**
 * Backend API base URL
 * Falls back to localhost in development
 */
export const BACKEND_API_URL = 
  process.env.NEXT_PUBLIC_API_URL || 
  process.env.NEXT_PUBLIC_BACKEND_URL || 
  'http://localhost:8000';

/**
 * API request timeout (in milliseconds)
 */
export const API_TIMEOUT = 30000; // 30 seconds

/**
 * API retry configuration
 */
export const API_RETRY_CONFIG = {
  MAX_RETRIES: 3,
  RETRY_DELAY: 1000, // 1 second
  RETRY_STATUS_CODES: [408, 429, 500, 502, 503, 504],
} as const;