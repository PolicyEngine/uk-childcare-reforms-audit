import type { Metadata, Viewport } from 'next';
import './globals.css';

const SITE_URL = 'https://uk-childcare-reforms-audit.vercel.app';
const TITLE = 'UK Childcare Reforms Benchmark | PolicyEngine';
const DESCRIPTION =
  'Benchmark of PolicyEngine modelling against external sources for UK childcare reforms — extended entitlement, tax-free childcare, and Universal Credit work allowances.';

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: TITLE,
  description: DESCRIPTION,
  keywords: [
    'UK childcare',
    'extended entitlement',
    'tax-free childcare',
    'PolicyEngine',
    'reforms',
    'benchmark',
  ],
  authors: [{ name: 'PolicyEngine' }],
  alternates: { canonical: SITE_URL },
  openGraph: {
    type: 'website',
    title: TITLE,
    description: DESCRIPTION,
    url: SITE_URL,
    siteName: 'PolicyEngine',
  },
  twitter: {
    card: 'summary_large_image',
    title: TITLE,
    description: DESCRIPTION,
    site: '@ThePolicyEngine',
  },
};

export const viewport: Viewport = {
  themeColor: '#2C6496',
  width: 'device-width',
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
