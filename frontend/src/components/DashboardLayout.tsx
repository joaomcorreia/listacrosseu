'use client';

import { ReactNode, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

interface DashboardLayoutProps {
    children: ReactNode;
    title: string;
    userRole?: 'admin' | 'user' | 'guest';
}

export default function DashboardLayout({ children, title, userRole = 'guest' }: DashboardLayoutProps) {
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const router = useRouter();

    const handleLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('refresh_token');
        router.push('/auth/login');
    };

    const navigationItems = [
        { name: 'Dashboard', href: '/dashboard', icon: '🏠', roles: ['admin', 'user'] },
        { name: 'All Businesses', href: '/businesses', icon: '🏢', roles: ['admin', 'user', 'guest'] },
        { name: 'EU Countries', href: '/countries', icon: '🇪🇺', roles: ['admin', 'user', 'guest'] },
        { name: 'Search', href: '/search', icon: '🔍', roles: ['admin', 'user', 'guest'] },
        { name: 'Admin Panel', href: '/admin', icon: '⚙️', roles: ['admin'] },
        { name: 'Analytics', href: '/analytics', icon: '📊', roles: ['admin'] },
        { name: 'Users', href: '/users', icon: '👥', roles: ['admin'] },
    ];

    const filteredNavigation = navigationItems.filter(item =>
        item.roles.includes(userRole)
    );

    return (
        <div className="min-h-screen bg-gray-100">
            {/* Mobile sidebar */}
            <div className={`fixed inset-0 z-40 lg:hidden ${sidebarOpen ? '' : 'pointer-events-none'}`}>
                <div className={`fixed inset-0 bg-gray-600 bg-opacity-75 transition-opacity ${sidebarOpen ? 'opacity-100' : 'opacity-0'}`}
                    onClick={() => setSidebarOpen(false)} />

                <div className={`relative flex-1 flex flex-col max-w-xs w-full bg-white transform transition ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}>
                    <div className="absolute top-0 right-0 -mr-12 pt-2">
                        <button
                            className="ml-1 flex items-center justify-center h-10 w-10 rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
                            onClick={() => setSidebarOpen(false)}
                        >
                            <span className="sr-only">Close sidebar</span>
                            <span className="text-white text-xl">×</span>
                        </button>
                    </div>

                    <div className="flex-1 h-0 pt-5 pb-4 overflow-y-auto">
                        <div className="flex-shrink-0 flex items-center px-4">
                            <h2 className="text-xl font-bold text-blue-600">ListAcrossEU</h2>
                        </div>
                        <nav className="mt-5 px-2 space-y-1">
                            {filteredNavigation.map((item) => (
                                <Link
                                    key={item.name}
                                    href={item.href}
                                    className="group flex items-center px-2 py-2 text-base font-medium rounded-md text-gray-600 hover:bg-gray-50 hover:text-gray-900"
                                >
                                    <span className="mr-3 text-lg">{item.icon}</span>
                                    {item.name}
                                </Link>
                            ))}
                        </nav>
                    </div>
                </div>
            </div>

            {/* Desktop sidebar */}
            <div className="hidden lg:flex lg:w-64 lg:flex-col lg:fixed lg:inset-y-0">
                <div className="flex-1 flex flex-col min-h-0 bg-white border-r border-gray-200">
                    <div className="flex-1 flex flex-col pt-5 pb-4 overflow-y-auto">
                        <div className="flex items-center flex-shrink-0 px-4">
                            <h2 className="text-xl font-bold text-blue-600">ListAcrossEU</h2>
                        </div>
                        <nav className="mt-5 flex-1 px-2 space-y-1">
                            {filteredNavigation.map((item) => (
                                <Link
                                    key={item.name}
                                    href={item.href}
                                    className="group flex items-center px-2 py-2 text-sm font-medium rounded-md text-gray-600 hover:bg-gray-50 hover:text-gray-900"
                                >
                                    <span className="mr-3 text-lg">{item.icon}</span>
                                    {item.name}
                                </Link>
                            ))}
                        </nav>
                    </div>
                </div>
            </div>

            {/* Main content */}
            <div className="lg:pl-64 flex flex-col flex-1">
                {/* Top navigation */}
                <div className="relative z-10 flex-shrink-0 flex h-16 bg-white shadow">
                    <button
                        className="px-4 border-r border-gray-200 text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500 lg:hidden"
                        onClick={() => setSidebarOpen(true)}
                    >
                        <span className="sr-only">Open sidebar</span>
                        <span className="text-xl">☰</span>
                    </button>

                    <div className="flex-1 px-4 flex justify-between items-center">
                        <h1 className="text-2xl font-semibold text-gray-900">{title}</h1>

                        <div className="flex items-center space-x-4">
                            <div className="flex items-center space-x-2">
                                <span className="text-sm text-gray-500">Role:</span>
                                <span className={`px-2 py-1 rounded-full text-xs font-medium ${userRole === 'admin' ? 'bg-red-100 text-red-800' :
                                        userRole === 'user' ? 'bg-blue-100 text-blue-800' :
                                            'bg-gray-100 text-gray-800'
                                    }`}>
                                    {userRole}
                                </span>
                            </div>

                            {userRole !== 'guest' && (
                                <button
                                    onClick={handleLogout}
                                    className="text-sm text-gray-500 hover:text-gray-700"
                                >
                                    Logout
                                </button>
                            )}
                        </div>
                    </div>
                </div>

                {/* Page content */}
                <main className="flex-1 overflow-y-auto p-6">
                    {children}
                </main>
            </div>
        </div>
    );
}