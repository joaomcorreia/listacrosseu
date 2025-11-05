'use client';

import { useState } from 'react';
import Link from 'next/link';
import LanguageSelector from '@/components/LanguageSelector';

export default function Home() {
    const [selectedLanguage, setSelectedLanguage] = useState('en');

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
            {/* Navigation */}
            <nav className="bg-white shadow-sm">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between items-center h-16">
                        <div className="flex items-center">
                            <h1 className="text-2xl font-bold text-blue-600">ListAcrossEU</h1>
                        </div>
                        <div className="flex items-center space-x-4">
                            <LanguageSelector
                                selectedLanguage={selectedLanguage}
                                onLanguageChange={setSelectedLanguage}
                            />
                            <Link
                                href="/dashboard"
                                className="text-blue-600 hover:text-blue-800 font-medium"
                            >
                                Dashboard
                            </Link>
                            <Link
                                href="/admin"
                                className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
                            >
                                Admin
                            </Link>
                        </div>
                    </div>
                </div>
            </nav>

            {/* Hero Section */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <div className="text-center">
                    <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
                        Discover Business
                        <span className="text-blue-600"> Across Europe</span>
                    </h1>
                    <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
                        Connect with over 6,593 verified businesses across all 27 EU countries.
                        Powered by AI translations and intelligent search in your preferred language.
                    </p>

                    {/* Feature Highlights */}
                    <div className="grid md:grid-cols-3 gap-8 mb-12">
                        <div className="bg-white rounded-lg shadow-lg p-6">
                            <div className="text-3xl mb-4">🏢</div>
                            <h3 className="text-xl font-bold text-gray-900 mb-2">6,593+ Businesses</h3>
                            <p className="text-gray-600">Verified businesses across all EU countries with detailed profiles and contact information.</p>
                        </div>

                        <div className="bg-white rounded-lg shadow-lg p-6">
                            <div className="text-3xl mb-4">🌍</div>
                            <h3 className="text-xl font-bold text-gray-900 mb-2">27 EU Languages</h3>
                            <p className="text-gray-600">Complete multilingual support with AI-powered translations for all EU official languages.</p>
                        </div>

                        <div className="bg-white rounded-lg shadow-lg p-6">
                            <div className="text-3xl mb-4">🤖</div>
                            <h3 className="text-xl font-bold text-gray-900 mb-2">MagicAI Assistant</h3>
                            <p className="text-gray-600">AI-powered content generation, SEO optimization, and market analysis tools.</p>
                        </div>
                    </div>

                    {/* CTA Buttons */}
                    <div className="flex flex-col sm:flex-row gap-4 justify-center">
                        <Link
                            href="/dashboard"
                            className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
                        >
                            User Dashboard
                        </Link>
                        <Link
                            href="/admin"
                            className="bg-white text-blue-600 border-2 border-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors"
                        >
                            Admin Panel
                        </Link>
                    </div>
                </div>

                {/* Statistics Section */}
                <div className="mt-20 bg-white rounded-lg shadow-lg p-8">
                    <h2 className="text-3xl font-bold text-center text-gray-900 mb-8">Platform Statistics</h2>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
                        <div className="text-center">
                            <div className="text-3xl font-bold text-blue-600">6,593+</div>
                            <div className="text-gray-600">Businesses Listed</div>
                        </div>
                        <div className="text-center">
                            <div className="text-3xl font-bold text-green-600">27</div>
                            <div className="text-gray-600">EU Languages</div>
                        </div>
                        <div className="text-center">
                            <div className="text-3xl font-bold text-purple-600">100%</div>
                            <div className="text-gray-600">Data Preserved</div>
                        </div>
                        <div className="text-center">
                            <div className="text-3xl font-bold text-orange-600">6</div>
                            <div className="text-gray-600">AI Features</div>
                        </div>
                    </div>
                </div>

                {/* Technology Stack */}
                <div className="mt-20 text-center">
                    <h2 className="text-3xl font-bold text-gray-900 mb-8">Modern Technology Stack</h2>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                        <div className="bg-white rounded-lg shadow p-6">
                            <div className="text-2xl mb-2">⚡</div>
                            <div className="font-semibold">Django 5.2.7</div>
                            <div className="text-sm text-gray-600">REST API Backend</div>
                        </div>
                        <div className="bg-white rounded-lg shadow p-6">
                            <div className="text-2xl mb-2">⚛️</div>
                            <div className="font-semibold">Next.js 15</div>
                            <div className="text-sm text-gray-600">React Frontend</div>
                        </div>
                        <div className="bg-white rounded-lg shadow p-6">
                            <div className="text-2xl mb-2">🎨</div>
                            <div className="font-semibold">Tailwind CSS</div>
                            <div className="text-sm text-gray-600">Modern Styling</div>
                        </div>
                        <div className="bg-white rounded-lg shadow p-6">
                            <div className="text-2xl mb-2">🤖</div>
                            <div className="font-semibold">MagicAI</div>
                            <div className="text-sm text-gray-600">AI Integration</div>
                        </div>
                    </div>
                </div>
            </main>

            {/* Footer */}
            <footer className="bg-gray-900 text-white py-12 mt-20">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="grid md:grid-cols-3 gap-8">
                        <div>
                            <h3 className="text-xl font-bold mb-4">ListAcrossEU</h3>
                            <p className="text-gray-300">
                                Your gateway to European business discovery with AI-powered features
                                and complete multilingual support.
                            </p>
                        </div>
                        <div>
                            <h4 className="font-semibold mb-4">Features</h4>
                            <ul className="space-y-2 text-gray-300">
                                <li>Business Directory</li>
                                <li>27 EU Languages</li>
                                <li>AI Content Generation</li>
                                <li>Advanced Search</li>
                            </ul>
                        </div>
                        <div>
                            <h4 className="font-semibtml-medium mb-4">Platform</h4>
                            <ul className="space-y-2 text-gray-300">
                                <li>Django REST API</li>
                                <li>Next.js Frontend</li>
                                <li>Modern Architecture</li>
                                <li>Production Ready</li>
                            </ul>
                        </div>
                    </div>
                    <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
                        <p>&copy; 2024 ListAcrossEU. Modern Django + Next.js Migration Complete.</p>
                    </div>
                </div>
            </footer>
        </div>
    );
}