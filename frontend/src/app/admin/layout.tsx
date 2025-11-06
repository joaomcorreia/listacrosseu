import { Metadata } from 'next';
import Link from 'next/link';
import { Toaster } from 'react-hot-toast';
import '../globals.css';

export const metadata: Metadata = {
  title: 'ListAcross EU Admin',
  description: 'Admin panel for managing ListAcross EU content',
  robots: 'noindex,nofollow'
};

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="bg-gray-50 min-h-screen">
      <Toaster position="top-right" />
      <div className="flex h-screen">
        {/* Sidebar */}
        <div className="w-64 bg-white shadow-lg">
          <div className="p-6 border-b">
            <h1 className="text-xl font-bold text-gray-900">ListAcross EU</h1>
            <p className="text-sm text-gray-600">Admin Panel</p>
          </div>
            
            <nav className="mt-6">
              <div className="px-6 py-2">
                <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
                  Content Management
                </h3>
              </div>
              
              <Link 
                href="/admin/dashboard" 
                className="flex items-center px-6 py-3 text-gray-700 hover:bg-gray-100"
              >
                <svg className="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z" />
                </svg>
                Dashboard
              </Link>
              
              <Link 
                href="/admin/pages" 
                className="flex items-center px-6 py-3 text-gray-700 hover:bg-gray-100"
              >
                <svg className="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z" clipRule="evenodd" />
                </svg>
                Pages
              </Link>
              
              <a 
                href="/admin/blog/posts" 
                className="flex items-center px-6 py-3 text-gray-700 hover:bg-gray-100"
              >
                <svg className="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clipRule="evenodd" />
                </svg>
                Blog Posts
              </a>
              
              <a 
                href="/admin/blog/categories" 
                className="flex items-center px-6 py-3 text-gray-700 hover:bg-gray-100"
              >
                <svg className="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M3 4a1 1 0 011-1h4a1 1 0 010 2H6.414l2.293 2.293a1 1 0 01-1.414 1.414L5 6.414V8a1 1 0 01-2 0V4zm9 1a1 1 0 010-2h4a1 1 0 011 1v4a1 1 0 01-2 0V6.414l-2.293 2.293a1 1 0 11-1.414-1.414L13.586 5H12zm-9 7a1 1 0 012 0v1.586l2.293-2.293a1 1 0 111.414 1.414L6.414 15H8a1 1 0 010 2H4a1 1 0 01-1-1v-4zm13-1a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 010-2h1.586l-2.293-2.293a1 1 0 111.414-1.414L15.586 13H14a1 1 0 01-1-1z" clipRule="evenodd" />
                </svg>
                Categories
              </a>
              
              <a 
                href="/admin/blog/generate" 
                className="flex items-center px-6 py-3 text-gray-700 hover:bg-gray-100"
              >
                <svg className="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clipRule="evenodd" />
                </svg>
                Blog → Generate
              </a>
              
              <a 
                href="/admin/businesses" 
                className="flex items-center px-6 py-3 text-gray-700 hover:bg-gray-100"
              >
                <svg className="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M4 4a2 2 0 00-2 2v8a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2H4zm3 5a1 1 0 011-1h4a1 1 0 110 2H8a1 1 0 01-1-1zm0 3a1 1 0 011-1h4a1 1 0 110 2H8a1 1 0 01-1-1z" clipRule="evenodd" />
                </svg>
                Businesses
              </a>
              
              <Link 
                href="/admin/csv-uploads" 
                className="flex items-center px-6 py-3 text-gray-700 hover:bg-gray-100"
              >
                <svg className="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
                CSV Uploads
              </Link>
              
              <div className="px-6 py-2 mt-8">
                <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
                  SEO & Analytics
                </h3>
              </div>
              
              <a 
                href="/admin/pages" 
                className="flex items-center px-6 py-3 text-gray-700 hover:bg-gray-100"
              >
                <svg className="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
                SEO Manager
              </a>
              
              <div className="px-6 py-2 mt-8">
                <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
                  System Admin
                </h3>
              </div>
              
              <Link 
                href="/admin/settings" 
                className="flex items-center px-6 py-3 text-gray-700 hover:bg-gray-100"
              >
                <svg className="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" clipRule="evenodd" />
                  <path fillRule="evenodd" d="M13 8a3 3 0 11-6 0 3 3 0 016 0z" clipRule="evenodd" />
                </svg>
                Settings
              </Link>
              
              <a 
                href="/admin/django" 
                className="flex items-center px-6 py-3 text-gray-700 hover:bg-gray-100"
              >
                <svg className="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M3 5a2 2 0 012-2h10a2 2 0 012 2v8a2 2 0 01-2 2h-2.22l.123.489.804.804A1 1 0 0113 18H7a1 1 0 01-.707-1.707l.804-.804L7.22 15H5a2 2 0 01-2-2V5zm5.771 7H9a1 1 0 110-2h.771l.422-1.687a1 1 0 111.94.484L11.613 12H12a1 1 0 110 2h-.387l-.422 1.687a1 1 0 11-1.94-.484L9.771 12z" clipRule="evenodd" />
                </svg>
                Django Admin
              </a>
              
              <a 
                href="http://127.0.0.1:8000/admin/" 
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center px-6 py-3 text-gray-700 hover:bg-gray-100"
              >
                <svg className="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
                SEO Manager
              </a>
            </nav>
          </div>
          
          {/* Main Content */}
          <div className="flex-1 flex flex-col overflow-hidden">
            {/* Top Bar */}
            <header className="bg-white shadow-sm border-b px-6 py-4">
              <div className="flex justify-between items-center">
                <h2 className="text-lg font-semibold text-gray-900">Admin Dashboard</h2>
                <div className="flex items-center space-x-4">
                  <button className="text-gray-500 hover:text-gray-700">
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                    </svg>
                  </button>
                  <div className="text-sm text-gray-600">Welcome, Admin</div>
                </div>
              </div>
            </header>
            
            {/* Content Area */}
            <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50 p-6">
              {children}
            </main>
          </div>
        </div>
      </div>
  );
}