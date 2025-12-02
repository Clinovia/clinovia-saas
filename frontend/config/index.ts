/**
 * Central configuration export
 * Import all config from this file for cleaner imports
 * 
 * @example
 * import { API_ENDPOINTS, ROUTES, APP_CONFIG } from '@/config';
 */

// API Configuration
export {
  API_ENDPOINTS,
  AUTH_ENDPOINTS,
  ALZHEIMER_ENDPOINTS,
  CARDIOLOGY_ENDPOINTS,
  USER_ENDPOINTS,
  DASHBOARD_ENDPOINTS,
  REPORT_ENDPOINTS,
  BACKEND_API_URL,
  API_TIMEOUT,
  API_RETRY_CONFIG,
} from './api';

// Application Configuration
export {
  APP_CONFIG,
  FEATURE_FLAGS,
  AUTH_CONFIG,
  UI_CONFIG,
  VALIDATION_RULES,
  MODULE_CONFIG,
  ERROR_MESSAGES,
  SUCCESS_MESSAGES,
  STORAGE_KEYS,
  IS_PRODUCTION,
  IS_DEVELOPMENT,
  IS_TEST,
  EXTERNAL_LINKS,
} from './app';

// Routes Configuration
export {
  ROUTES,
  PUBLIC_ROUTES,
  AUTH_ROUTES,
  DASHBOARD_ROUTES,
  ALZHEIMER_ROUTES,
  CARDIOLOGY_ROUTES,
  ROUTE_METADATA,
  isProtectedRoute,
  isPublicRoute,
  isAuthRoute,
  getDefaultRedirect,
  getBreadcrumbs,
} from './routes';