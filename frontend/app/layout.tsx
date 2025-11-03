import './globals.css';
import type { Metadata } from 'next';
import { Inter, Playfair_Display } from 'next/font/google';
import Navigation from '@/components/Navigation';
import ConditionalFooter from '../components/ConditionalFooter';
import DynamicFavicon from '@/components/DynamicFavicon';
import ClientOnlyAssistantWidget from '../components/ClientOnlyAssistantWidget';

const inter = Inter({ subsets: ['latin'] });
const playfair = Playfair_Display({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'ListAcrossEU - European Business Directory',
  description: 'Find businesses across Europe organized by category and location',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="scroll-smooth">
      <body className={`${inter.className} bg-white min-h-screen`}>
        <DynamicFavicon />

        {/* Content */}
        <div className="flex flex-col min-h-screen">
          <Navigation />
          <main className="flex-1">
            {children}
          </main>
          
          <ConditionalFooter playfair={playfair} />
        </div>
        
        {/* Public Assistant Widget */}
        <ClientOnlyAssistantWidget initialLang="en" isLoggedIn={false} />
      </body>
    </html>
  );
}