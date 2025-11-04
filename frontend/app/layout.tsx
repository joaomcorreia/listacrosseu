import './globals.css';
import type { Metadata } from 'next';
import { Inter, Playfair_Display } from 'next/font/google';
import Navigation from '@/components/Navigation';
import ConditionalFooter from '../components/ConditionalFooter';
import DynamicFavicon from '@/components/DynamicFavicon';
import ClientOnlyAssistantWidget from '../components/ClientOnlyAssistantWidget';
import ChunkErrorBoundary from '@/components/ChunkErrorBoundary';
import ChunkErrorHandler from '@/components/ChunkErrorHandler';
import ChunkRetryHandler from '@/components/ChunkRetryHandler';
import DevNotifications from '@/components/DevNotifications';

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
                <ChunkErrorHandler />
                <ChunkRetryHandler maxRetries={2} retryDelay={500} />

                {/* Content */}
                <ChunkErrorBoundary>
                    <div className="flex flex-col min-h-screen">
                        <Navigation />
                        <main className="flex-1">
                            {children}
                        </main>

                        <ConditionalFooter playfair={playfair} />
                    </div>
                </ChunkErrorBoundary>

                {/* Public Assistant Widget */}
                <ClientOnlyAssistantWidget initialLang="en" isLoggedIn={false} />
                
                {/* Development notifications for chunk loading */}
                <DevNotifications />
            </body>
        </html>
    );
}