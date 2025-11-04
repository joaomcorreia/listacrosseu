'use client';

import { useSiteSettings } from '../hooks/useSiteSettings';
import LanguageDropdown from './LanguageDropdown';
import { usePathname } from 'next/navigation';

export default function Navigation() {
    const { settings } = useSiteSettings();
    const pathname = usePathname();

    // Extract current language from pathname
    const currentLanguage = pathname.split('/')[1] || 'en';

    const getAnimationClasses = () => {
        const colors = settings?.nav_animation_colors || 'from-blue-500 via-purple-500 to-indigo-500';
        return `bg-gradient-to-r ${colors} animate-gradient-x`;
    };

    const getAnimationDuration = () => {
        const speed = settings?.nav_animation_speed || 'medium';
        const speedMap = {
            'slow': '5s',
            'medium': '3s',
            'fast': '1s'
        };
        return speedMap[speed as keyof typeof speedMap] || '3s';
    };

    return (
        <nav className="bg-white/95 backdrop-blur-sm shadow-lg border-b border-blue-100 sticky top-0 z-50">
            {/* Animated border - controlled by settings */}
            <div className={`absolute bottom-0 left-0 right-0 h-1 ${settings?.enable_nav_animation
                    ? getAnimationClasses()
                    : 'bg-blue-500'
                }`}
                style={settings?.enable_nav_animation ? {
                    animationDuration: getAnimationDuration(),
                } : {}}></div>

            <div className="max-w-7xl mx-auto px-4">
                <div className="flex items-center justify-between h-20">
                    {/* Logo Section */}
                    <div className="flex items-center">
                        <a href="/" className="group flex items-center space-x-3">
                            {/* Logo - Use uploaded logo if available, otherwise fallback */}
                            <div className="relative">
                                {settings?.logo_url ? (
                                    <img
                                        src={settings.logo_url}
                                        alt={settings.site_name}
                                        className="w-12 h-12 object-contain"
                                    />
                                ) : (
                                    <div className="w-10 h-10 bg-gradient-to-br from-blue-400 to-blue-500 rounded-xl flex items-center justify-center">
                                        <span className="text-white font-bold text-sm">EU</span>
                                    </div>
                                )}
                                {!settings?.logo_url && (
                                    <div className="absolute -top-1 -right-1 w-4 h-4 bg-gradient-to-br from-amber-400 to-amber-500 rounded-full flex items-center justify-center">
                                        <span className="text-white text-xs">★</span>
                                    </div>
                                )}
                            </div>
                            <div className="flex flex-col">
                                <span className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-amber-400 bg-clip-text text-transparent">
                                    {settings?.site_name || 'ListAcrossEU'}
                                </span>
                                <span className="text-xs text-slate-500 -mt-1">
                                    {settings?.site_tagline || 'European Business Directory'}
                                </span>
                            </div>
                        </a>
                    </div>

                    {/* Navigation Links */}
                    <div className="hidden lg:flex items-center space-x-8">
                        <a
                            href={`/${currentLanguage}/categories`}
                            className="group flex items-center space-x-2 text-slate-700 hover:text-blue-600 px-4 py-2 rounded-xl hover:bg-blue-50 transition-all duration-200 font-medium"
                        >
                            <span>📂</span>
                            <span>Categories</span>
                        </a>
                        <a
                            href={`/${currentLanguage}/countries`}
                            className="group flex items-center space-x-2 text-slate-700 hover:text-blue-600 px-4 py-2 rounded-xl hover:bg-blue-50 transition-all duration-200 font-medium"
                        >
                            <span>🌍</span>
                            <span>Countries</span>
                        </a>
                        <a
                            href={`/${currentLanguage}/businesses`}
                            className="group flex items-center space-x-2 text-slate-700 hover:text-blue-600 px-4 py-2 rounded-xl hover:bg-blue-50 transition-all duration-200 font-medium"
                        >
                            <span>🏢</span>
                            <span>Businesses</span>
                        </a>

                        {/* Language Dropdown */}
                        <LanguageDropdown
                            currentLanguage={currentLanguage}
                            displayMode={settings?.navigation_display_mode || 'both'}
                        />
                    </div>

                    {/* Mobile Menu Button */}
                    <div className="lg:hidden">
                        <button className="p-2 rounded-xl text-slate-600 hover:text-blue-600 hover:bg-blue-50 transition-all">
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        </nav>
    );
}