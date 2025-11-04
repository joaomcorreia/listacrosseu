'use client';

import Link from 'next/link';
import { translate, Language, getTranslatedPath } from '@/lib/i18n';

interface Subcategory {
    slug: string;
    name: string;
    count: number;
}

interface EnhancedCategoryProps {
    mainCategory: {
        slug: string;
        name: string;
        totalCount: number;
        icon: string;
        color: {
            primary: string;
            secondary: string;
            accent: string;
        };
    };
    subcategories: Subcategory[];
    lang: string;
}

export default function EnhancedCategoryCard({ mainCategory, subcategories, lang }: EnhancedCategoryProps) {
    return (
        <div className="group relative bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-3 border border-slate-100 overflow-hidden">
            {/* Animated gradient background */}
            <div 
                className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-700 bg-gradient-to-br"
                style={{
                    background: `linear-gradient(135deg, ${mainCategory.color.primary}05, ${mainCategory.color.secondary}10, ${mainCategory.color.accent}05)`
                }}
            ></div>
            
            {/* Decorative elements */}
            <div className="absolute top-0 right-0 w-24 h-24 opacity-10 group-hover:opacity-20 transition-opacity duration-500">
                <div 
                    className="w-full h-full rounded-bl-full"
                    style={{ background: `linear-gradient(225deg, ${mainCategory.color.primary}, ${mainCategory.color.secondary})` }}
                ></div>
            </div>
            
            {/* Floating dots */}
            <div className="absolute inset-0 overflow-hidden">
                <div 
                    className="absolute top-6 right-8 w-2 h-2 rounded-full animate-pulse opacity-30"
                    style={{ backgroundColor: mainCategory.color.accent }}
                ></div>
                <div 
                    className="absolute bottom-8 left-6 w-1.5 h-1.5 rounded-full animate-pulse opacity-25"
                    style={{ backgroundColor: mainCategory.color.secondary, animationDelay: '0.7s' }}
                ></div>
                <div 
                    className="absolute top-16 left-8 w-1 h-1 rounded-full animate-pulse opacity-20"
                    style={{ backgroundColor: mainCategory.color.primary, animationDelay: '1.2s' }}
                ></div>
            </div>

            <div className="relative p-6">
                {/* Main category header */}
                <div className="flex items-center mb-6">
                    <div 
                        className="w-14 h-14 rounded-xl flex items-center justify-center text-2xl shadow-lg group-hover:shadow-xl transition-shadow duration-300"
                        style={{ background: `linear-gradient(135deg, ${mainCategory.color.primary}, ${mainCategory.color.secondary})` }}
                    >
                        <span className="filter drop-shadow-sm">{mainCategory.icon}</span>
                    </div>
                    
                    <div className="ml-4 flex-1">
                        <h3 className="text-2xl font-bold text-slate-900 group-hover:text-slate-700 transition-colors">
                            {mainCategory.name}
                        </h3>
                        <div 
                            className="text-sm font-semibold mt-1 px-3 py-1 rounded-full inline-block"
                            style={{ 
                                backgroundColor: `${mainCategory.color.primary}15`,
                                color: mainCategory.color.primary 
                            }}
                        >
                            {mainCategory.totalCount} {translate('common.businesses', lang as Language)}
                        </div>
                    </div>
                </div>

                {/* Subcategories grid */}
                <div className="space-y-3 mb-6">
                    {subcategories.slice(0, 4).map((subcategory, index) => (
                        <Link
                            key={subcategory.slug}
                            href={`/${lang}/${getTranslatedPath('categories', lang as Language)}/${subcategory.slug}`}
                            className="group/sub flex items-center justify-between p-3 rounded-lg hover:bg-slate-50 transition-all duration-200 border border-transparent hover:border-slate-200"
                            style={{ 
                                animationDelay: `${index * 100}ms`,
                            }}
                        >
                            <div className="flex items-center flex-1">
                                <div 
                                    className="w-2 h-2 rounded-full mr-3 opacity-70 group-hover/sub:opacity-100 transition-opacity"
                                    style={{ backgroundColor: mainCategory.color.secondary }}
                                ></div>
                                <span className="font-medium text-slate-700 group-hover/sub:text-slate-900 transition-colors text-sm">
                                    {subcategory.name}
                                </span>
                            </div>
                            
                            <div className="flex items-center space-x-2">
                                <span className="text-xs text-slate-500 font-medium">
                                    {subcategory.count}
                                </span>
                                <div 
                                    className="w-5 h-5 rounded-full flex items-center justify-center opacity-0 group-hover/sub:opacity-100 transition-all duration-200 transform translate-x-2 group-hover/sub:translate-x-0"
                                    style={{ backgroundColor: `${mainCategory.color.accent}20` }}
                                >
                                    <span 
                                        className="text-xs font-bold"
                                        style={{ color: mainCategory.color.accent }}
                                    >→</span>
                                </div>
                            </div>
                        </Link>
                    ))}
                    
                    {subcategories.length > 4 && (
                        <div className="text-center pt-2">
                            <span className="text-xs text-slate-400 font-medium">
                                +{subcategories.length - 4} more categories
                            </span>
                        </div>
                    )}
                </div>

                {/* Main CTA */}
                <Link
                    href={`/${lang}/${getTranslatedPath('categories', lang as Language)}?category=${mainCategory.slug}`}
                    className="w-full flex items-center justify-center space-x-3 py-3 rounded-xl font-semibold transition-all duration-300 transform group-hover:translate-y-0 hover:shadow-lg text-white"
                    style={{ 
                        background: `linear-gradient(135deg, ${mainCategory.color.primary}, ${mainCategory.color.secondary})`,
                    }}
                >
                    <span>{translate('common.view_all', lang as Language)}</span>
                    <div className="w-6 h-6 rounded-full bg-white bg-opacity-20 flex items-center justify-center">
                        <span className="text-sm font-bold">→</span>
                    </div>
                </Link>
            </div>

            {/* Hover border effect */}
            <div 
                className="absolute inset-0 rounded-2xl border-2 border-transparent group-hover:border-opacity-20 transition-all duration-300 pointer-events-none"
                style={{ borderColor: mainCategory.color.primary }}
            ></div>
        </div>
    );
}