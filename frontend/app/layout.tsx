import './globals.css';
import type { Metadata } from 'next';
import { Inter, Playfair_Display } from 'next/font/google';
import Navigation from '@/components/Navigation';

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
      <body className={`${inter.className} bg-gradient-to-br from-slate-50 via-blue-50 to-amber-50 min-h-screen`}>
        {/* Background Pattern */}
        <div className="fixed inset-0 z-0">
          <div className="absolute inset-0 opacity-40 bg-slate-100"></div>
          <div className="absolute inset-0 bg-gradient-to-br from-blue-600/5 via-transparent to-amber-500/5"></div>
        </div>

        {/* Content */}
        <div className="relative z-10">
          <Navigation />
          <main className="min-h-screen">
            {children}
          </main>
          
          {/* Enhanced Footer */}
          <footer className="relative bg-gradient-to-r from-slate-900 via-blue-900 to-slate-900 text-white overflow-hidden">
            {/* Footer Background Pattern */}
            <div className="absolute inset-0 bg-slate-800 opacity-30"></div>
            
            <div className="relative z-10 max-w-7xl mx-auto px-4 py-16">
              <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
                {/* Brand Section */}
                <div className="md:col-span-2">
                  <h3 className={`${playfair.className} text-3xl font-bold text-white mb-4 bg-gradient-to-r from-blue-400 to-amber-400 bg-clip-text text-transparent`}>
                    ListAcrossEU
                  </h3>
                  <p className="text-slate-300 mb-4 leading-relaxed">
                    Connecting European businesses across borders. Discover, explore, and connect with thousands of businesses throughout the European Union.
                  </p>
                  <div className="flex space-x-4">
                    <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-blue-600 rounded-full flex items-center justify-center">
                      <span className="text-white text-sm font-bold">EU</span>
                    </div>
                    <div className="w-8 h-8 bg-gradient-to-r from-amber-500 to-amber-600 rounded-full flex items-center justify-center">
                      <span className="text-white text-sm">★</span>
                    </div>
                  </div>
                </div>

                {/* Quick Links */}
                <div>
                  <h4 className="text-white font-semibold mb-4 text-lg">Quick Links</h4>
                  <ul className="space-y-2">
                    <li><a href="/en/categories" className="text-slate-300 hover:text-amber-400 transition-colors">Categories</a></li>
                    <li><a href="/en/businesses" className="text-slate-300 hover:text-amber-400 transition-colors">Browse Businesses</a></li>
                    <li><a href="/en" className="text-slate-300 hover:text-amber-400 transition-colors">Home</a></li>
                  </ul>
                </div>

                {/* Languages */}
                <div>
                  <h4 className="text-white font-semibold mb-4 text-lg">Languages</h4>
                  <div className="grid grid-cols-2 gap-2">
                    <a href="/en" className="text-slate-300 hover:text-amber-400 transition-colors text-sm">🇬🇧 English</a>
                    <a href="/de" className="text-slate-300 hover:text-amber-400 transition-colors text-sm">🇩🇪 Deutsch</a>
                    <a href="/fr" className="text-slate-300 hover:text-amber-400 transition-colors text-sm">🇫🇷 Français</a>
                    <a href="/es" className="text-slate-300 hover:text-amber-400 transition-colors text-sm">🇪🇸 Español</a>
                    <a href="/nl" className="text-slate-300 hover:text-amber-400 transition-colors text-sm">🇳🇱 Nederlands</a>
                    <a href="/pt" className="text-slate-300 hover:text-amber-400 transition-colors text-sm">🇵🇹 Português</a>
                  </div>
                </div>
              </div>

              {/* Bottom Bar */}
              <div className="border-t border-slate-700 pt-8">
                <div className="flex flex-col md:flex-row justify-between items-center">
                  <p className="text-slate-400 text-sm">
                    &copy; 2025 ListAcrossEU. All rights reserved. Made with ❤️ for Europe.
                  </p>
                  <div className="flex items-center space-x-4 mt-4 md:mt-0">
                    <span className="text-slate-500 text-xs">Powered by</span>
                    <div className="flex space-x-2">
                      <div className="w-6 h-6 bg-blue-600 rounded text-white text-xs flex items-center justify-center font-bold">EU</div>
                      <div className="w-6 h-6 bg-amber-500 rounded text-white text-xs flex items-center justify-center">★</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}