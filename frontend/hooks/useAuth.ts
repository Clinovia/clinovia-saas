/**
 * Central export file for all custom hooks
 * Import hooks from this file for cleaner imports
 * 
 * @example
 * import { useAuth, useDebounce, useMediaQuery } from '@/hooks';
 */

export { useAuth } from './useAuth';
export { useLocalStorage } from './useLocalStorage';
export { useDebounce, useDebouncedCallback } from './useDebounce';
export { useMediaQuery, useBreakpoint } from './useMediaQuery';
export { useForm } from './useForm';
export { useAsync, useAsyncCallback } from './useAsync';

// Re-export types
export type { UseAuthReturn, SignupData } from './useAuth';
export type { UseFormOptions, UseFormReturn } from './useForm';
export type { UseAsyncState, UseAsyncReturn } from './useAsync';