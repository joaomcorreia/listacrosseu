'use client';

import { useState, useEffect } from 'react';
import DashboardLayout from '@/components/DashboardLayout';
import LanguageSelector from '@/components/LanguageSelector';
import MagicAIAssistant from '@/components/MagicAIAssistant';

export default function AdminDashboard() {
    const [selectedLanguage, setSelectedLanguage] = useState('en');
    const [stats, setStats] = useState({
        totalBusinesses: 6331,
        activeUsers: 127,
        pendingApprovals: 15,
        monthlyGrowth: 8.5
    });

    const recentActivities = [
        { id: 1, action: 'New business registered', business: 'Tech Solutions Ltd', time: '2 hours ago', type: 'success' },
        { id: 2, action: 'User verification pending', user: 'maria.silva@email.com', time: '4 hours ago', type: 'warning' },
        { id: 3, action: 'Business profile updated', business: 'Green Energy Co', time: '6 hours ago', type: 'info' },
        { id: 4, action: 'Translation completed', business: 'Local Restaurant', time: '1 day ago', type: 'success' },
        { id: 5, action: 'AI content generated', business: 'Fashion Boutique', time: '1 day ago', type: 'info' }
    ];

    return (
        <DashboardLayout title="Admin Dashboard" userRole="admin">
            <div className="space-y-6">
                {/* Header with Language Selector */}
                <div className="flex justify-between items-center">
                    <div>
                        <h2 className="text-2xl font-bold text-gray-900">Welcome back, Admin</h2>
                        <p className="text-gray-600">Here's what's happening with your platform today.</p>
                    </div>
                    <LanguageSelector
                        selectedLanguage={selectedLanguage}
                        onLanguageChange={setSelectedLanguage}
                        className="ml-4"
                    />
                </div>

                {/* Stats Cards */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <div className="bg-white rounded-lg shadow p-6">
                        <div className="flex items-center">
                            <div className="p-2 bg-blue-100 rounded-md">
                                <span className="text-2xl">🏢</span>
                            </div>
                            <div className="ml-4">
                                <p className="text-sm font-medium text-gray-500">Total Businesses</p>
                                <p className="text-2xl font-bold text-gray-900">{stats.totalBusinesses.toLocaleString()}</p>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white rounded-lg shadow p-6">
                        <div className="flex items-center">
                            <div className="p-2 bg-green-100 rounded-md">
                                <span className="text-2xl">👥</span>
                            </div>
                            <div className="ml-4">
                                <p className="text-sm font-medium text-gray-500">Active Users</p>
                                <p className="text-2xl font-bold text-gray-900">{stats.activeUsers}</p>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white rounded-lg shadow p-6">
                        <div className="flex items-center">
                            <div className="p-2 bg-yellow-100 rounded-md">
                                <span className="text-2xl">⏳</span>
                            </div>
                            <div className="ml-4">
                                <p className="text-sm font-medium text-gray-500">Pending Approvals</p>
                                <p className="text-2xl font-bold text-gray-900">{stats.pendingApprovals}</p>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white rounded-lg shadow p-6">
                        <div className="flex items-center">
                            <div className="p-2 bg-purple-100 rounded-md">
                                <span className="text-2xl">📈</span>
                            </div>
                            <div className="ml-4">
                                <p className="text-sm font-medium text-gray-500">Monthly Growth</p>
                                <p className="text-2xl font-bold text-gray-900">{stats.monthlyGrowth}%</p>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Main Content Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* Recent Activity */}
                    <div className="bg-white rounded-lg shadow">
                        <div className="p-6 border-b border-gray-200">
                            <h3 className="text-lg font-medium text-gray-900">Recent Activity</h3>
                        </div>
                        <div className="p-6">
                            <div className="space-y-4">
                                {recentActivities.map((activity) => (
                                    <div key={activity.id} className="flex items-start space-x-3">
                                        <div className={`w-2 h-2 rounded-full mt-2 ${activity.type === 'success' ? 'bg-green-500' :
                                                activity.type === 'warning' ? 'bg-yellow-500' :
                                                    'bg-blue-500'
                                            }`}></div>
                                        <div className="flex-1 min-w-0">
                                            <p className="text-sm text-gray-900">
                                                {activity.action}
                                                {activity.business && (
                                                    <span className="font-medium"> {activity.business}</span>
                                                )}
                                                {activity.user && (
                                                    <span className="font-medium"> {activity.user}</span>
                                                )}
                                            </p>
                                            <p className="text-xs text-gray-500">{activity.time}</p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>

                    {/* Quick Actions */}
                    <div className="bg-white rounded-lg shadow">
                        <div className="p-6 border-b border-gray-200">
                            <h3 className="text-lg font-medium text-gray-900">Quick Actions</h3>
                        </div>
                        <div className="p-6">
                            <div className="grid grid-cols-2 gap-4">
                                <button className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                                    <div className="text-center">
                                        <div className="text-2xl mb-2">➕</div>
                                        <div className="text-sm font-medium text-gray-900">Add Business</div>
                                    </div>
                                </button>

                                <button className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                                    <div className="text-center">
                                        <div className="text-2xl mb-2">👤</div>
                                        <div className="text-sm font-medium text-gray-900">Manage Users</div>
                                    </div>
                                </button>

                                <button className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                                    <div className="text-center">
                                        <div className="text-2xl mb-2">📊</div>
                                        <div className="text-sm font-medium text-gray-900">View Analytics</div>
                                    </div>
                                </button>

                                <button className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                                    <div className="text-center">
                                        <div className="text-2xl mb-2">⚙️</div>
                                        <div className="text-sm font-medium text-gray-900">Settings</div>
                                    </div>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                {/* MagicAI Assistant */}
                <MagicAIAssistant
                    className="mt-6"
                    onResult={(feature, result) => {
                        console.log(`AI Result for ${feature}:`, result);
                    }}
                />

                {/* System Status */}
                <div className="bg-white rounded-lg shadow p-6">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">System Status</h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div className="text-center">
                            <div className="text-2xl mb-2">🟢</div>
                            <div className="text-sm font-medium text-gray-900">API Status</div>
                            <div className="text-xs text-gray-500">All systems operational</div>
                        </div>

                        <div className="text-center">
                            <div className="text-2xl mb-2">🟢</div>
                            <div className="text-sm font-medium text-gray-900">Database</div>
                            <div className="text-xs text-gray-500">Connected and healthy</div>
                        </div>

                        <div className="text-center">
                            <div className="text-2xl mb-2">🟡</div>
                            <div className="text-sm font-medium text-gray-900">AI Services</div>
                            <div className="text-xs text-gray-500">Moderate load</div>
                        </div>
                    </div>
                </div>
            </div>
        </DashboardLayout>
    );
}