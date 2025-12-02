/**
 * Application Routes Configuration
 * Centralized route definitions for type-safe navigation
 */

/**
 * Public routes (accessible without authentication)
 */
export const PUBLIC_ROUTES = {
  HOME: '/',
  MODULES: '/modules',
  ABOUT: '/about',
  CONTACT: '/contact',
  PRIVACY: '/privacy',
  TERMS: '/terms',
} as const;

/**
 * Authentication routes
 */
export const AUTH_ROUTES = {
  LOGIN: '/login',
  SIGNUP: '/signup',
  FORGOT_PASSWORD: '/forgot-password',
  RESET_PASSWORD: '/reset-password',
  VERIFY_EMAIL: '/verify-email',
} as const;

/**
 * Dashboard routes (protected)
 */
export const DASHBOARD_ROUTES = {
  DASHBOARD: '/dashboard',
  PROFILE: '/profile',
  SETTINGS: '/settings',
  REPORTS: '/reports',
} as const;

/**
 * Alzheimer's module routes (protected)
 */
export const ALZHEIMER_ROUTES = {
  BASE: '/alzheimer',
  OVERVIEW: '/alzheimer',
  
  // Diagnosis routes
  DIAGNOSIS_SCREENING: '/alzheimer/diagnosis-screening',
  DIAGNOSIS_BASIC: '/alzheimer/diagnosis-basic',
  DIAGNOSIS_EXTENDED: '/alzheimer/diagnosis-extended',
  
  // Prognosis routes
  PROGNOSIS_2YR_BASIC: '/alzheimer/prognosis-2yr-basic',
  PROGNOSIS_2YR_EXTENDED: '/alzheimer/prognosis-2yr-extended',
  
  // Risk assessment
  RISK_SCREENER: '/alzheimer/risk-screener',
} as const;

/**
 * Cardiology module routes (protected)
 */
export const CARDIOLOGY_ROUTES = {
  BASE: '/cardiology',
  OVERVIEW: '/cardiology',
  
  // Assessment routes
  ASCVD: '/cardiology/ascvd',
  BP_CATEGORY: '/cardiology/bp-category',
  CHA2DS2_VASC: '/cardiology/cha2ds2vasc',
  ECG_INTERPRETER: '/cardiology/ecg-interpreter',
  EF_PREDICTION: '/cardiology/ef-prediction',
} as const;

/**
 * All routes grouped
 */
export const ROUTES = {
  PUBLIC: PUBLIC_ROUTES,
  AUTH: AUTH_ROUTES,
  DASHBOARD: DASHBOARD_ROUTES,
  ALZHEIMER: ALZHEIMER_ROUTES,
  CARDIOLOGY: CARDIOLOGY_ROUTES,
} as const;

/**
 * Route metadata for navigation menus
 */
export const ROUTE_METADATA = {
  // Alzheimer's tools
  ALZHEIMER_TOOLS: [
    {
      path: ALZHEIMER_ROUTES.DIAGNOSIS_SCREENING,
      title: 'Diagnosis Screening',
      description: 'Quick screening for Alzheimer\'s disease',
      icon: '🔍',
    },
    {
      path: ALZHEIMER_ROUTES.DIAGNOSIS_BASIC,
      title: 'Basic Diagnosis',
      description: 'Basic diagnostic assessment',
      icon: '📋',
    },
    {
      path: ALZHEIMER_ROUTES.DIAGNOSIS_EXTENDED,
      title: 'Extended Diagnosis',
      description: 'Comprehensive diagnostic evaluation',
      icon: '📊',
    },
    {
      path: ALZHEIMER_ROUTES.PROGNOSIS_2YR_BASIC,
      title: '2-Year Prognosis (Basic)',
      description: 'Basic 2-year prognosis prediction',
      icon: '📈',
    },
    {
      path: ALZHEIMER_ROUTES.PROGNOSIS_2YR_EXTENDED,
      title: '2-Year Prognosis (Extended)',
      description: 'Extended 2-year prognosis prediction',
      icon: '📉',
    },
    {
      path: ALZHEIMER_ROUTES.RISK_SCREENER,
      title: 'Risk Screener',
      description: 'Assess risk factors for Alzheimer\'s',
      icon: '⚠️',
    },
  ],
  
  // Cardiology tools
  CARDIOLOGY_TOOLS: [
    {
      path: CARDIOLOGY_ROUTES.ASCVD,
      title: 'ASCVD Calculator',
      description: 'Atherosclerotic cardiovascular disease risk',
      icon: '💓',
    },
    {
      path: CARDIOLOGY_ROUTES.BP_CATEGORY,
      title: 'Blood Pressure Category',
      description: 'Categorize blood pressure readings',
      icon: '🩺',
    },
    {
      path: CARDIOLOGY_ROUTES.CHA2DS2_VASC,
      title: 'CHA₂DS₂-VASc Score',
      description: 'Stroke risk in atrial fibrillation',
      icon: '🫀',
    },
    {
      path: CARDIOLOGY_ROUTES.ECG_INTERPRETER,
      title: 'ECG Interpreter',
      description: 'AI-powered ECG analysis',
      icon: '📈',
    },
    {
      path: CARDIOLOGY_ROUTES.EF_PREDICTION,
      title: 'Ejection Fraction',
      description: 'Predict cardiac ejection fraction',
      icon: '💗',
    },
  ],
  
  // Main navigation
  MAIN_NAV: [
    {
      path: PUBLIC_ROUTES.HOME,
      title: 'Home',
      icon: '🏠',
    },
    {
      path: PUBLIC_ROUTES.MODULES,
      title: 'Modules',
      icon: '📦',
    },
    {
      path: DASHBOARD_ROUTES.DASHBOARD,
      title: 'Dashboard',
      icon: '📊',
      protected: true,
    },
  ],
} as const;

/**
 * Helper function to check if a route is protected
 */
export function isProtectedRoute(pathname: string): boolean {
  const protectedPrefixes = [
    ALZHEIMER_ROUTES.BASE,
    CARDIOLOGY_ROUTES.BASE,
    DASHBOARD_ROUTES.DASHBOARD,
    DASHBOARD_ROUTES.PROFILE,
    DASHBOARD_ROUTES.SETTINGS,
    DASHBOARD_ROUTES.REPORTS,
  ];
  
  return protectedPrefixes.some(prefix => pathname.startsWith(prefix));
}

/**
 * Helper function to check if a route is public
 */
export function isPublicRoute(pathname: string): boolean {
  return Object.values(PUBLIC_ROUTES).includes(pathname as any);
}

/**
 * Helper function to check if a route is an auth route
 */
export function isAuthRoute(pathname: string): boolean {
  return Object.values(AUTH_ROUTES).some(route => pathname.startsWith(route));
}

/**
 * Get default redirect based on user role
 */
export function getDefaultRedirect(userRole?: string): string {
  // Can customize based on user role
  switch (userRole) {
    case 'admin':
      return DASHBOARD_ROUTES.DASHBOARD;
    case 'doctor':
      return ALZHEIMER_ROUTES.BASE;
    default:
      return DASHBOARD_ROUTES.DASHBOARD;
  }
}

/**
 * Breadcrumb configuration
 */
export function getBreadcrumbs(pathname: string): Array<{ label: string; href: string }> {
  const segments = pathname.split('/').filter(Boolean);
  const breadcrumbs = [{ label: 'Home', href: '/' }];
  
  let currentPath = '';
  segments.forEach((segment, index) => {
    currentPath += `/${segment}`;
    
    // Format segment name
    const label = segment
      .split('-')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
    
    breadcrumbs.push({
      label,
      href: currentPath,
    });
  });
  
  return breadcrumbs;
}