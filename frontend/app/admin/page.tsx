"use client";

import React from 'react';
import AdminLayout from '../../components/admin/AdminLayout';
import {
    Users,
    FileText,
    CreditCard,
    TrendingUp,
    Eye,
    Calendar,
    DollarSign,
    Activity
} from 'lucide-react';

interface StatCardProps {
    title: string;
    value: string;
    icon: React.ComponentType<{ className?: string }>;
    trend?: 'up' | 'down';
    trendValue?: string;
    color?: 'blue' | 'green' | 'purple' | 'orange';
}

const StatCard: React.FC<StatCardProps> = ({ title, value, icon: Icon, trend, trendValue, color = 'blue' }) => {
    const colorClasses: Record<string, string> = {
        blue: 'bg-blue-500 text-blue-700 bg-blue-50',
        green: 'bg-green-500 text-green-700 bg-green-50',
        purple: 'bg-purple-500 text-purple-700 bg-purple-50',
        orange: 'bg-orange-500 text-orange-700 bg-orange-50'
    };

    return (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
                <div>
                    <p className="text-sm font-medium text-gray-600">{title}</p>
                    <p className="text-3xl font-bold text-gray-900 mt-1">{value}</p>
                    {trend && (
                        <div className="flex items-center mt-2">
                            <TrendingUp className={`w-4 h-4 ${trend === 'up' ? 'text-green-500' : 'text-red-500'}`} />
                            <span className={`text-sm font-medium ml-1 ${trend === 'up' ? 'text-green-600' : 'text-red-600'}`}>
                                {trendValue}
                            </span>
                            <span className="text-sm text-gray-500 ml-1">vs last month</span>
                        </div>
                    )}
                </div>
                <div className={`w-12 h-12 ${colorClasses[color].split(' ')[2]} rounded-lg flex items-center justify-center`}>
                    <Icon className={`w-6 h-6 ${colorClasses[color].split(' ')[0]}`} />
                </div>
            </div>
        </div>
    );
};

interface ActivityItem {
    title: string;
    subtitle: string;
    time: string;
}

interface RecentActivityProps {
    title: string;
    items: ActivityItem[];
}

const RecentActivity: React.FC<RecentActivityProps> = ({ title, items }) => (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
        <div className="space-y-4">
            {items.map((item: ActivityItem, index: number) => (
                <div key={index} className="flex items-center space-x-3">
                    <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                    <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-gray-900 truncate">{item.title}</p>
                        <p className="text-xs text-gray-500">{item.subtitle}</p>
                    </div>
                    <div className="text-xs text-gray-400">{item.time}</div>
                </div>
            ))}
        </div>
    </div>
);

const QuickActions = () => (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
        <div className="grid grid-cols-2 gap-3">
            <button className="flex items-center justify-center px-4 py-3 bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100 transition-colors">
                <FileText className="w-4 h-4 mr-2" />
                New Post
            </button>
            <button className="flex items-center justify-center px-4 py-3 bg-green-50 text-green-700 rounded-lg hover:bg-green-100 transition-colors">
                <Users className="w-4 h-4 mr-2" />
                Add Business
            </button>
            <button className="flex items-center justify-center px-4 py-3 bg-purple-50 text-purple-700 rounded-lg hover:bg-purple-100 transition-colors">
                <CreditCard className="w-4 h-4 mr-2" />
                New Plan
            </button>
            <button className="flex items-center justify-center px-4 py-3 bg-orange-50 text-orange-700 rounded-lg hover:bg-orange-100 transition-colors">
                <Activity className="w-4 h-4 mr-2" />
                Analytics
            </button>
        </div>
    </div>
);

const AdminDashboard = () => {
    // Mock data - in real app, this would come from API
    const stats = {
        totalSubscribers: '6,331',
        blogPosts: '24',
        activeSubscriptions: '89',
        monthlyRevenue: '€2,340'
    };

    const recentSubscribers = [
        { title: 'Café Central', subtitle: 'Vienna, Austria', time: '2 min ago' },
        { title: 'Tech Solutions Ltd', subtitle: 'Berlin, Germany', time: '5 min ago' },
        { title: 'Bistro Le Paris', subtitle: 'Paris, France', time: '12 min ago' },
        { title: 'Milano Fashion', subtitle: 'Milan, Italy', time: '18 min ago' }
    ];

    const recentBlogPosts = [
        { title: 'How to Start a Business in EU', subtitle: 'Published in English', time: '1 hour ago' },
        { title: 'Cómo Iniciar un Negocio en UE', subtitle: 'Published in Spanish', time: '2 hours ago' },
        { title: 'Marketing Strategies for EU', subtitle: 'Draft', time: '1 day ago' },
        { title: 'Legal Requirements Guide', subtitle: 'Scheduled', time: '2 days ago' }
    ];

    return (
        <AdminLayout>
            <div className="space-y-6">
                {/* Header */}
                <div>
                    <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
                    <p className="text-gray-600 mt-2">Welcome back! Here's what's happening with your platform.</p>
                </div>

                {/* Stats Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <StatCard
                        title="Total Subscribers"
                        value={stats.totalSubscribers}
                        icon={Users}
                        trend="up"
                        trendValue="+12%"
                        color="blue"
                    />
                    <StatCard
                        title="Blog Posts"
                        value={stats.blogPosts}
                        icon={FileText}
                        trend="up"
                        trendValue="+3"
                        color="green"
                    />
                    <StatCard
                        title="Active Subscriptions"
                        value={stats.activeSubscriptions}
                        icon={CreditCard}
                        trend="up"
                        trendValue="+8%"
                        color="purple"
                    />
                    <StatCard
                        title="Monthly Revenue"
                        value={stats.monthlyRevenue}
                        icon={DollarSign}
                        trend="up"
                        trendValue="+15%"
                        color="orange"
                    />
                </div>

                {/* Content Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* Recent Activity */}
                    <div className="lg:col-span-2 space-y-6">
                        <RecentActivity
                            title="Recent Subscribers"
                            items={recentSubscribers}
                        />
                        <RecentActivity
                            title="Recent Blog Posts"
                            items={recentBlogPosts}
                        />
                    </div>

                    {/* Sidebar */}
                    <div className="space-y-6">
                        <QuickActions />

                        {/* Performance Overview */}
                        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                            <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance Overview</h3>
                            <div className="space-y-4">
                                <div>
                                    <div className="flex justify-between text-sm">
                                        <span className="text-gray-600">Page Views</span>
                                        <span className="font-medium">+24%</span>
                                    </div>
                                    <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
                                        <div className="bg-blue-500 h-2 rounded-full" style={{ width: '74%' }}></div>
                                    </div>
                                </div>
                                <div>
                                    <div className="flex justify-between text-sm">
                                        <span className="text-gray-600">New Registrations</span>
                                        <span className="font-medium">+18%</span>
                                    </div>
                                    <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
                                        <div className="bg-green-500 h-2 rounded-full" style={{ width: '68%' }}></div>
                                    </div>
                                </div>
                                <div>
                                    <div className="flex justify-between text-sm">
                                        <span className="text-gray-600">Conversion Rate</span>
                                        <span className="font-medium">+5%</span>
                                    </div>
                                    <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
                                        <div className="bg-purple-500 h-2 rounded-full" style={{ width: '45%' }}></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </AdminLayout>
    );
};

export default AdminDashboard;