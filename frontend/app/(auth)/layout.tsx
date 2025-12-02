import type { Metadata } from 'next';
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Clinovia - Clinical AI Platform',
  description: 'AI-powered clinical assessments for cardiology and neurology',
  keywords: ['clinical AI', 'cardiology', 'neurology', 'medical AI', 'ASCVD', 'Alzheimer'],
};

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return <div className={inter.className}>{children}</div>;
}
