/**
 * Application Configuration
 * General app settings and constants
 */

/**
 * Application metadata
 */
export const APP_CONFIG = {
  NAME: 'MedAI Platform',
  DESCRIPTION: 'AI-powered medical diagnosis and prognosis platform',
  VERSION: '1.0.0',
  AUTHOR: 'Your Organization',
  SUPPORT_EMAIL: 'support@medai.com',
  CONTACT_EMAIL: 'contact@medai.com',
} as const;

/**
 * Feature flags
 * Enable/disable features across the app
 */
export const FEATURE_FLAGS = {
  ENABLE_ALZHEIMER_MODULE: true,
  ENABLE_CARDIOLOGY_MODULE: true,
  ENABLE_REPORTS: true,
  ENABLE_DASHBOARD: true,
  ENABLE_ANALYTICS: true,
  ENABLE_NOTIFICATIONS: false, // Coming soon
  ENABLE_DARK_MODE: true,
  ENABLE_EXPORT_PDF: true,
  ENABLE_MULTI_LANGUAGE: false, // Coming soon
} as const;

/**
 * Authentication configuration
 */
export const AUTH_CONFIG = {
  // Token expiration times (in seconds)
  ACCESS_TOKEN_EXPIRY: 7 * 24 * 60 * 60, // 7 days
  REFRESH_TOKEN_EXPIRY: 30 * 24 * 60 * 60, // 30 days
  
  // Session settings
  SESSION_TIMEOUT: 24 * 60 * 60 * 1000, // 24 hours in milliseconds
  REMEMBER_ME_DURATION: 30 * 24 * 60 * 60 * 1000, // 30 days
  
  // Password requirements
  PASSWORD_MIN_LENGTH: 8,
  PASSWORD_REQUIRE_UPPERCASE: true,
  PASSWORD_REQUIRE_LOWERCASE: true,
  PASSWORD_REQUIRE_NUMBER: true,
  PASSWORD_REQUIRE_SPECIAL: true,
  
  // Login attempts
  MAX_LOGIN_ATTEMPTS: 5,
  LOCKOUT_DURATION: 15 * 60 * 1000, // 15 minutes
} as const;

/**
 * UI/UX Configuration
 */
export const UI_CONFIG = {
  // Theme
  DEFAULT_THEME: 'light' as 'light' | 'dark',
  
  // Pagination
  DEFAULT_PAGE_SIZE: 10,
  PAGE_SIZE_OPTIONS: [10, 20, 50, 100],
  
  // Sidebar
  SIDEBAR_WIDTH: 280,
  SIDEBAR_COLLAPSED_WIDTH: 80,
  
  // Toast/Notification duration
  TOAST_DURATION: 5000, // 5 seconds
  
  // Loading states
  DEBOUNCE_DELAY: 500, // milliseconds
  LOADING_SPINNER_DELAY: 300, // milliseconds
  
  // File upload
  MAX_FILE_SIZE: 10 * 1024 * 1024, // 10MB
  ALLOWED_FILE_TYPES: ['.pdf', '.jpg', '.jpeg', '.png', '.dcm'],
} as const;

/**
 * Validation rules
 */
export const VALIDATION_RULES = {
  // Email
  EMAIL_REGEX: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  
  // Age ranges
  MIN_AGE: 18,
  MAX_AGE: 120,
  
  // Vital signs ranges (for validation)
  BLOOD_PRESSURE: {
    SYSTOLIC: { MIN: 70, MAX: 250 },
    DIASTOLIC: { MIN: 40, MAX: 150 },
  },
  HEART_RATE: { MIN: 30, MAX: 250 },
  TEMPERATURE: { MIN: 35, MAX: 42 }, // Celsius
  
  // Lab values
  CHOLESTEROL: { MIN: 100, MAX: 400 }, // mg/dL
  HDL: { MIN: 20, MAX: 100 }, // mg/dL
  LDL: { MIN: 50, MAX: 300 }, // mg/dL
} as const;

/**
 * Medical module configuration
 */
export const MODULE_CONFIG = {
  ALZHEIMER: {
    NAME: "Alzheimer's Disease",
    DESCRIPTION: 'AI-powered diagnosis and prognosis tools',
    ICON: '🧠',
    COLOR: '#8B5CF6', // Purple
    AVAILABLE_TOOLS: [
      'diagnosis-screening',
      'diagnosis-basic',
      'diagnosis-extended',
      'prognosis-2yr-basic',
      'prognosis-2yr-extended',
      'risk-screener',
    ],
  },
  CARDIOLOGY: {
    NAME: 'Cardiology',
    DESCRIPTION: 'Cardiovascular risk assessment tools',
    ICON: '❤️',
    COLOR: '#EF4444', // Red
    AVAILABLE_TOOLS: [
      'ascvd',
      'bp-category',
      'cha2ds2vasc',
      'ecg-interpreter',
      'ef-prediction',
    ],
  },
} as const;

/**
 * Error messages
 */
export const ERROR_MESSAGES = {
  GENERIC: 'An unexpected error occurred. Please try again.',
  NETWORK: 'Network error. Please check your connection.',
  TIMEOUT: 'Request timed out. Please try again.',
  UNAUTHORIZED: 'You are not authorized. Please log in.',
  FORBIDDEN: 'You do not have permission to access this resource.',
  NOT_FOUND: 'The requested resource was not found.',
  VALIDATION: 'Please check your input and try again.',
  SERVER: 'Server error. Please try again later.',
} as const;

/**
 * Success messages
 */
export const SUCCESS_MESSAGES = {
  LOGIN: 'Successfully logged in!',
  SIGNUP: 'Account created successfully!',
  LOGOUT: 'Successfully logged out.',
  PROFILE_UPDATED: 'Profile updated successfully.',
  PASSWORD_CHANGED: 'Password changed successfully.',
  REPORT_GENERATED: 'Report generated successfully.',
  DATA_SAVED: 'Data saved successfully.',
} as const;

/**
 * Local storage keys
 */
export const STORAGE_KEYS = {
  THEME: 'medai_theme',
  LANGUAGE: 'medai_language',
  SIDEBAR_COLLAPSED: 'medai_sidebar_collapsed',
  RECENT_SEARCHES: 'medai_recent_searches',
  PREFERENCES: 'medai_user_preferences',
} as const;

/**
 * Environment check
 */
export const IS_PRODUCTION = process.env.NODE_ENV === 'production';
export const IS_DEVELOPMENT = process.env.NODE_ENV === 'development';
export const IS_TEST = process.env.NODE_ENV === 'test';

/**
 * External links
 */
export const EXTERNAL_LINKS = {
  DOCUMENTATION: 'https://docs.medai.com',
  SUPPORT: 'https://support.medai.com',
  PRIVACY_POLICY: 'https://medai.com/privacy',
  TERMS_OF_SERVICE: 'https://medai.com/terms',
  FAQ: 'https://medai.com/faq',
  GITHUB: 'https://github.com/yourorg/medai',
} as const;