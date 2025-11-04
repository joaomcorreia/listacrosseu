"use client";

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
    LayoutDashboard,
    FileText,
    Users,
    CreditCard,
    Settings,
    BarChart3,
    Bot,
    LogOut,
    Menu,
    X,
    ChevronLeft,
    ChevronRight
} from 'lucide-react';

interface AdminSidebarProps {
    isOpen: boolean;
    toggleSidebar: () => void;
    isCollapsed: boolean;
    toggleCollapsed: () => void;
}

interface AdminLayoutProps {
    children: React.ReactNode;
}

const AdminSidebar: React.FC<AdminSidebarProps> = ({ isOpen, toggleSidebar, isCollapsed, toggleCollapsed }) => {
    const pathname = usePathname();

    const navigation = [
        {
            name: 'Dashboard',
            href: '/admin',
            icon: LayoutDashboard,
            current: pathname === '/admin'
        },
        {
            name: 'Blog Posts',
            href: '/admin/blog',
            icon: FileText,
            current: pathname.startsWith('/admin/blog')
        },
        {
            name: 'Subscribers',
            href: '/admin/businesses',
            icon: Users,
            current: pathname.startsWith('/admin/businesses')
        },
        {
            name: 'Pricing Plans',
            href: '/admin/pricing',
            icon: CreditCard,
            current: pathname.startsWith('/admin/pricing')
        },
        {
            name: 'Analytics',
            href: '/admin/analytics',
            icon: BarChart3,
            current: pathname.startsWith('/admin/analytics')
        },
        {
            name: 'Assistant',
            href: '/admin/assistant',
            icon: Bot,
            current: pathname.startsWith('/admin/assistant')
        },
        {
            name: 'Settings',
            href: '/admin/settings',
            icon: Settings,
            current: pathname.startsWith('/admin/settings')
        }
    ];

    return (
        <>
            {/* Mobile backdrop */}
            {isOpen && (
                <div
                    className="fixed inset-0 bg-gray-600 bg-opacity-75 z-20 lg:hidden"
                    onClick={toggleSidebar}
                />
            )}

            {/* Sidebar */}
            <div className={`
        fixed inset-y-0 left-0 z-30 bg-white shadow-lg transform transition-all duration-200 ease-in-out flex flex-col
        ${isOpen ? 'translate-x-0' : '-translate-x-full'}
        lg:translate-x-0
        ${isCollapsed ? 'lg:w-16' : 'lg:w-64'}
        w-64
      `}>
                <div className="flex items-center justify-between h-16 px-6 bg-blue-600 flex-shrink-0">
                    <div className="flex items-center">
                        <div className="w-8 h-8 flex items-center justify-center">
                            <span className="text-white font-bold text-lg">L</span>
                        </div>
                        {!isCollapsed && <span className="ml-3 text-white font-semibold text-lg">ListAcrossEU</span>}
                    </div>
                    <div className="flex items-center space-x-2">
                        {/* Desktop collapse toggle */}
                        <button
                            onClick={toggleCollapsed}
                            className="hidden lg:block text-white hover:text-gray-200 transition-colors"
                            title={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
                        >
                            {isCollapsed ? <ChevronRight className="w-5 h-5" /> : <ChevronLeft className="w-5 h-5" />}
                        </button>
                        {/* Mobile close button */}
                        <button
                            onClick={toggleSidebar}
                            className="lg:hidden text-white hover:text-gray-200"
                        >
                            <X className="w-6 h-6" />
                        </button>
                    </div>
                </div>

                <nav className="mt-6 px-3 flex-1 flex flex-col">
                    <div className="space-y-1 relative flex-1">
                        {navigation.map((item) => {
                            const Icon = item.icon;
                            return (
                                <Link
                                    key={item.name}
                                    href={item.href}
                                    className={`
                    group flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-all duration-200 relative
                    ${isCollapsed ? 'justify-center' : ''}
                    ${item.current
                                            ? 'bg-blue-50 text-blue-700'
                                            : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
                                        }
                  `}
                                    title={isCollapsed ? item.name : undefined}
                                >
                                    <Icon className={`
                    h-5 w-5 flex-shrink-0 transition-colors duration-200
                    ${isCollapsed ? 'mr-0' : 'mr-3'}
                    ${item.current ? 'text-blue-500' : 'text-gray-400 group-hover:text-gray-500'}
                  `} />
                                    {!isCollapsed && (
                                        <>
                                            {item.name}

                                            {/* Animated bottom border */}
                                            <div className={`
                        absolute bottom-0 left-3 right-3 h-0.5 bg-blue-600 transform transition-all duration-300 ease-out
                        ${item.current
                                                    ? 'scale-x-100 opacity-100'
                                                    : 'scale-x-0 opacity-0 group-hover:scale-x-50 group-hover:opacity-50'
                                                }
                      `} />
                                        </>
                                    )}
                                </Link>
                            );
                        })}
                    </div>

                    <div className="mt-auto space-y-4">
                        <div className="pt-6 border-t border-gray-200">
                            <button
                                className={`
                  group flex items-center w-full px-3 py-2 text-sm font-medium text-gray-700 rounded-lg hover:bg-gray-50 hover:text-gray-900 transition-colors
                  ${isCollapsed ? 'justify-center' : ''}
                `}
                                title={isCollapsed ? 'Sign Out' : undefined}
                            >
                                <LogOut className={`
                  h-5 w-5 text-gray-400 group-hover:text-gray-500
                  ${isCollapsed ? 'mr-0' : 'mr-3'}
                `} />
                                {!isCollapsed && 'Sign Out'}
                            </button>
                        </div>

                        {!isCollapsed && (
                            <div className="pb-4">
                                <div className="bg-blue-50 rounded-lg p-3">
                                    <div className="text-xs text-blue-800 font-medium">Admin Panel</div>
                                    <div className="text-xs text-blue-600 mt-1">v2.0.0</div>
                                </div>
                            </div>
                        )}
                    </div>
                </nav>
            </div>
        </>
    );
};

const AdminLayout: React.FC<AdminLayoutProps> = ({ children }) => {
    const [sidebarOpen, setSidebarOpen] = React.useState(false);
    const [sidebarCollapsed, setSidebarCollapsed] = React.useState(false);
    const [currentDate, setCurrentDate] = React.useState('');
    // Updated: November 2, 2025 - Added collapsible sidebar functionality

    const toggleSidebar = () => {
        setSidebarOpen(!sidebarOpen);
    };

    const toggleCollapsed = () => {
        const newState = !sidebarCollapsed;
        setSidebarCollapsed(newState);
        // Persist the collapsed state in localStorage
        if (typeof window !== 'undefined') {
            localStorage.setItem('sidebar-collapsed', newState.toString());
        }
    };

    // Fix hydration mismatch by setting date on client side only
    React.useEffect(() => {
        setCurrentDate(new Date().toLocaleDateString('en-US', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }));

        // Restore sidebar collapsed state from localStorage
        if (typeof window !== 'undefined') {
            const savedState = localStorage.getItem('sidebar-collapsed');
            if (savedState !== null) {
                setSidebarCollapsed(savedState === 'true');
            }
        }
    }, []);

    return (
        <div className="min-h-screen bg-gray-50">
            <AdminSidebar
                isOpen={sidebarOpen}
                toggleSidebar={toggleSidebar}
                isCollapsed={sidebarCollapsed}
                toggleCollapsed={toggleCollapsed}
            />

            <div className={`min-h-screen flex flex-col transition-all duration-200 ease-in-out ${sidebarCollapsed ? 'lg:ml-16' : 'lg:ml-64'}`}>
                {/* Top header */}
                <div className="sticky top-20 z-40 bg-white border-b border-gray-200 shadow-sm">
                    <div className="flex items-center justify-between h-16 px-4 sm:px-6 lg:px-8">
                        <button
                            onClick={toggleSidebar}
                            className="lg:hidden p-2 text-gray-500 hover:text-gray-700"
                        >
                            <Menu className="w-6 h-6" />
                        </button>

                        <div className="flex items-center space-x-4">
                            <div className="text-sm text-gray-500">
                                {currentDate || 'Loading...'}
                            </div>
                        </div>

                        <div className="flex items-center space-x-4">
                            <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                                <span className="text-white text-sm font-medium">AD</span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Main content */}
                <main className="px-4 py-6 sm:px-6 lg:px-8 bg-gray-50 flex-1">
                    {children}
                </main>

                {/* Admin Footer */}
                <footer className="bg-white border-t border-gray-200 mt-auto">
                    <div className="px-4 py-4 sm:px-6 lg:px-8">
                        <div className="flex flex-col sm:flex-row justify-between items-center text-sm text-gray-500">
                            <div className="flex items-center space-x-4">
                                <span>&copy; 2025 ListAcrossEU Admin</span>
                                <span className="hidden sm:block">•</span>
                                <span className="flex items-center">
                                    <Bot className="w-4 h-4 mr-1" />
                                    AI Assistant Enabled
                                </span>
                            </div>
                            <div className="flex items-center space-x-4 mt-2 sm:mt-0">
                                <span className="text-xs">Version 1.0.0</span>
                                <div className="flex items-center space-x-1">
                                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                                    <span className="text-xs">System Online</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </footer>
            </div>
        </div>
    );
};

export default AdminLayout;