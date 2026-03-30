import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Almatti AI Workforce',
  description: 'Multi-Agent AI System — Web Builder, Content, Communication, File Manager',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
