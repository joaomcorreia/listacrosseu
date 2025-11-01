'use client';

import { useState, useEffect } from 'react';
import DashboardLayout from '@/components/DashboardLayout';
import LanguageSelector from '@/components/LanguageSelector';
import MagicAIAssistant from '@/components/MagicAIAssistant';

export default function UserDashboard() {
    const [selectedLanguage, setSelectedLanguage] = useState('en');
    const [userBusinesses, setUserBusinesses] = useState([
        {
            id: 1,
            name: 'My Restaurant',
            category: 'Food & Beverage',
            status: 'active',
            views: 234,
            lastUpdated: '2024-10-28'
        },
        {
            id: 2,
            name: 'Tech Consulting',
            category: 'Technology',
            status: 'pending',
            views: 89,
            lastUpdated: '2024-10-30'
        }
    ]);

    const [favorites, setFavorites] = useState([
        { id: 1, name: 'Best Pizza Place', category: 'Restaurant', city: 'Rome' },
        { id: 2, name: 'Green Energy Solutions', category: 'Technology', city: 'Berlin' },
        { id: 3, name: 'Fashion Boutique', category: 'Retail', city: 'Paris' }
    ]);

    return (
        <DashboardLayout title="My Dashboard" userRole="user">
            <div className="space-y-6">
                {/* Header with Language Selector */}
                <div className="flex justify-between items-center">
                    <div>
                        <h2 className="text-2xl font-bold text-gray-900">Welcome back!</h2>
                        <p className="text-gray-600">Manage your businesses and explore new opportunities across Europe.</p>
                    </div>
                    <LanguageSelector
                        selectedLanguage={selectedLanguage}
                        onLanguageChange={setSelectedLanguage}
                        className="ml-4"
                    />
                </div>

                {/* Quick Stats */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="bg-white rounded-lg shadow p-6">
                        <div className="flex items-center">
                            <div className="p-2 bg-blue-100 rounded-md">
                                <span className="text-2xl">🏢</span>
                            </div>
                            <div className="ml-4">
                                <p className="text-sm font-medium text-gray-500">My Businesses</p>
                                <p className="text-2xl font-bold text-gray-900">{userBusinesses.length}</p>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white rounded-lg shadow p-6">
                        <div className="flex items-center">
                            <div className="p-2 bg-green-100 rounded-md">
                                <span className="text-2xl">👁️</span>
                            </div>
                            <div className="ml-4">
                                <p className="text-sm font-medium text-gray-500">Total Views</p>
                                <p className="text-2xl font-bold text-gray-900">
                                    {userBusinesses.reduce((total, business) => total + business.views, 0)}
                                </p>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white rounded-lg shadow p-6">
                        <div className="flex items-center">
                            <div className="p-2 bg-purple-100 rounded-md">
                                <span className="text-2xl">❤️</span>
                            </div>
                            <div className="ml-4">
                                <p className="text-sm font-medium text-gray-500">Favorites</p>
                                <p className="text-2xl font-bold text-gray-900">{favorites.length}</p>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Main Content Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* My Businesses */}
                    <div className="bg-white rounded-lg shadow">
                        <div className="p-6 border-b border-gray-200 flex justify-between items-center">
                            <h3 className="text-lg font-medium text-gray-900">My Businesses</h3>
                            <button className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700">
                                Add Business
                            </button>
                        </div>
                        <div className="p-6">
                            <div className="space-y-4">
                                {userBusinesses.map((business) => (
                                    <div key={business.id} className="border border-gray-200 rounded-lg p-4">
                                        <div className="flex justify-between items-start">
                                            <div className="flex-1">
                                                <h4 className="font-medium text-gray-900">{business.name}</h4>
                                                <p className="text-sm text-gray-500">{business.category}</p>
                                                <div className="flex items-center mt-2 space-x-4">
                                                    <span className="text-xs text-gray-500">👁️ {business.views} views</span>
                                                    <span className="text-xs text-gray-500">
                                                        Updated: {new Date(business.lastUpdated).toLocaleDateString()}
                                                    </span>
                                                </div>
                                            </div>
                                            <div className="ml-4">
                                                <span className={`inline-block px-2 py-1 rounded-full text-xs font-medium ${business.status === 'active'
                                                        ? 'bg-green-100 text-green-800'
                                                        : 'bg-yellow-100 text-yellow-800'
                                                    }`}>
                                                    {business.status}
                                                </span>
                                            </div>
                                        </div>
                                        <div className="mt-3 flex space-x-2">
                                            <button className="text-xs text-blue-600 hover:text-blue-800">Edit</button>
                                            <button className="text-xs text-blue-600 hover:text-blue-800">View</button>
                                            <button className="text-xs text-blue-600 hover:text-blue-800">AI Enhance</button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>

                    {/* Favorites */}
                    <div className="bg-white rounded-lg shadow">
                        <div className="p-6 border-b border-gray-200">
                            <h3 className="text-lg font-medium text-gray-900">Favorite Businesses</h3>
                        </div>
                        <div className="p-6">
                            <div className="space-y-4">
                                {favorites.map((favorite) => (
                                    <div key={favorite.id} className="flex items-center space-x-3">
                                        <div className="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center">
                                            <span className="text-sm">❤️</span>
                                        </div>
                                        <div className="flex-1 min-w-0">
                                            <p className="text-sm font-medium text-gray-900">{favorite.name}</p>
                                            <p className="text-xs text-gray-500">{favorite.category} • {favorite.city}</p>
                                        </div>
                                        <button className="text-xs text-blue-600 hover:text-blue-800">View</button>
                                    </div>
                                ))}
                            </div>
                            <button className="mt-4 w-full text-sm text-blue-600 hover:text-blue-800 border border-blue-200 rounded-md py-2">
                                Browse More Businesses
                            </button>
                        </div>
                    </div>
                </div>

                {/* MagicAI Assistant for Users */}
                <MagicAIAssistant
                    className="mt-6"
                    businessData={userBusinesses[0]} // Pass first business as context
                    onResult={(feature, result) => {
                        console.log(`AI Result for ${feature}:`, result);
                        // You could show a notification or update the UI with the result
                    }}
                />

                {/* Quick Actions */}
                <div className="bg-white rounded-lg shadow p-6">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">Quick Actions</h3>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <button className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors text-center">
                            <div className="text-2xl mb-2">🔍</div>
                            <div className="text-sm font-medium text-gray-900">Search Businesses</div>
                        </button>

                        <button className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors text-center">
                            <div className="text-2xl mb-2">➕</div>
                            <div className="text-sm font-medium text-gray-900">Add Business</div>
                        </button>

                        <button className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors text-center">
                            <div className="text-2xl mb-2">🌍</div>
                            <div className="text-sm font-medium text-gray-900">Translate Content</div>
                        </button>

                        <button className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors text-center">
                            <div className="text-2xl mb-2">📊</div>
                            <div className="text-sm font-medium text-gray-900">View Analytics</div>
                        </button>
                    </div>
                </div>

                {/* Recent Activity */}
                <div className="bg-white rounded-lg shadow p-6">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">Recent Activity</h3>
                    <div className="space-y-3">
                        <div className="flex items-center space-x-3 text-sm">
                            <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                            <span className="text-gray-700">Your business "My Restaurant" received 12 new views</span>
                            <span className="text-gray-500 ml-auto">2 hours ago</span>
                        </div>
                        <div className="flex items-center space-x-3 text-sm">
                            <span className="w-2 h-2 bg-blue-500 rounded-full"></span>
                            <span className="text-gray-700">AI enhanced description for "Tech Consulting"</span>
                            <span className="text-gray-500 ml-auto">1 day ago</span>
                        </div>
                        <div className="flex items-center space-x-3 text-sm">
                            <span className="w-2 h-2 bg-purple-500 rounded-full"></span>
                            <span className="text-gray-700">Added "Best Pizza Place" to favorites</span>
                            <span className="text-gray-500 ml-auto">3 days ago</span>
                        </div>
                    </div>
                </div>
            </div>
        </DashboardLayout>
    );
}