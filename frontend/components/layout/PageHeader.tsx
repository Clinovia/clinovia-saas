import Link from 'next/link';
import { ChevronRight, Home } from 'lucide-react';
import type { ReactNode } from 'react';

interface Breadcrumb {
  label: string;
  href?: string;
}

interface PageHeaderProps {
  title: string;
  description?: string;
  breadcrumbs?: Breadcrumb[];
  icon?: ReactNode;
  actions?: ReactNode;
  badge?: {
    text: string;
    variant?: 'default' | 'success' | 'warning' | 'danger' | 'info';
  };
}

/**
 * PageHeader Component
 * Reusable header for dashboard pages with breadcrumbs, title, description, and actions
 * 
 * @example
 * <PageHeader
 *   title="Alzheimer's Diagnosis"
 *   description="AI-powered diagnostic assessment tools"
 *   icon={<Brain className="h-6 w-6" />}
 *   breadcrumbs={[
 *     { label: 'Dashboard', href: '/dashboard' },
 *     { label: 'Alzheimer', href: '/alzheimer' },
 *     { label: 'Diagnosis' }
 *   ]}
 *   actions={
 *     <button>Export Results</button>
 *   }
 *   badge={{ text: 'Beta', variant: 'info' }}
 * />
 */
export default function PageHeader({
  title,
  description,
  breadcrumbs,
  icon,
  actions,
  badge,
}: PageHeaderProps) {
  return (
    <div className="mb-6 border-b border-gray-200 bg-white px-6 py-4">
      {/* Breadcrumbs */}
      {breadcrumbs && breadcrumbs.length > 0 && (
        <nav className="mb-4 flex" aria-label="Breadcrumb">
          <ol className="flex items-center space-x-2 text-sm">
            {/* Home Icon */}
            <li>
              <Link
                href="/"
                className="text-gray-500 transition-colors hover:text-gray-700"
                aria-label="Home"
              >
                <Home className="h-4 w-4" />
              </Link>
            </li>

            {/* Breadcrumb Items */}
            {breadcrumbs.map((crumb, index) => (
              <li key={index} className="flex items-center">
                <ChevronRight className="h-4 w-4 text-gray-400" />
                {crumb.href ? (
                  <Link
                    href={crumb.href}
                    className="ml-2 text-gray-500 transition-colors hover:text-gray-700"
                  >
                    {crumb.label}
                  </Link>
                ) : (
                  <span className="ml-2 font-medium text-gray-900">{crumb.label}</span>
                )}
              </li>
            ))}
          </ol>
        </nav>
      )}

      {/* Header Content */}
      <div className="flex items-start justify-between">
        {/* Title Section */}
        <div className="flex items-start gap-4">
          {/* Icon */}
          {icon && (
            <div className="flex-shrink-0 rounded-lg bg-blue-50 p-3 text-blue-600">
              {icon}
            </div>
          )}

          {/* Title and Description */}
          <div>
            <div className="flex items-center gap-3">
              <h1 className="text-2xl font-bold text-gray-900 sm:text-3xl">{title}</h1>
              
              {/* Badge */}
              {badge && (
                <span
                  className={`rounded-full px-3 py-1 text-xs font-semibold ${getBadgeClasses(
                    badge.variant || 'default'
                  )}`}
                >
                  {badge.text}
                </span>
              )}
            </div>

            {/* Description */}
            {description && <p className="mt-1 text-gray-600">{description}</p>}
          </div>
        </div>

        {/* Actions */}
        {actions && <div className="flex items-center gap-2">{actions}</div>}
      </div>
    </div>
  );
}

/**
 * Get badge color classes based on variant
 */
function getBadgeClasses(variant: string): string {
  const variants = {
    default: 'bg-gray-100 text-gray-700',
    success: 'bg-green-100 text-green-700',
    warning: 'bg-yellow-100 text-yellow-700',
    danger: 'bg-red-100 text-red-700',
    info: 'bg-blue-100 text-blue-700',
  };

  return variants[variant as keyof typeof variants] || variants.default;
}

/**
 * Simplified PageHeader for simple pages
 */
export function SimplePageHeader({
  title,
  description,
}: {
  title: string;
  description?: string;
}) {
  return (
    <div className="mb-6">
      <h1 className="text-3xl font-bold text-gray-900">{title}</h1>
      {description && <p className="mt-1 text-gray-600">{description}</p>}
    </div>
  );
}

/**
 * PageHeader with back button
 */
export function PageHeaderWithBack({
  title,
  description,
  onBack,
  backLabel = 'Back',
}: {
  title: string;
  description?: string;
  onBack: () => void;
  backLabel?: string;
}) {
  return (
    <div className="mb-6">
      <button
        onClick={onBack}
        className="mb-3 flex items-center gap-2 text-sm text-gray-600 transition-colors hover:text-gray-900"
      >
        <ChevronRight className="h-4 w-4 rotate-180" />
        {backLabel}
      </button>
      <h1 className="text-3xl font-bold text-gray-900">{title}</h1>
      {description && <p className="mt-1 text-gray-600">{description}</p>}
    </div>
  );
}