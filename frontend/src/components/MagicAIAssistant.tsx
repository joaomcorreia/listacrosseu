'use client';

import { useState } from 'react';

interface MagicAIFeature {
    id: string;
    name: string;
    description: string;
    icon: string;
    category: 'content' | 'marketing' | 'analysis';
}

const AI_FEATURES: MagicAIFeature[] = [
    {
        id: 'description-generator',
        name: 'Description Generator',
        description: 'Generate compelling business descriptions and content',
        icon: '✍️',
        category: 'content'
    },
    {
        id: 'multilingual-translator',
        name: 'Multilingual Translator',
        description: 'Translate content across all 27 EU languages',
        icon: '🌍',
        category: 'content'
    },
    {
        id: 'seo-optimizer',
        name: 'SEO Optimizer',
        description: 'Optimize content for search engines',
        icon: '🚀',
        category: 'marketing'
    },
    {
        id: 'content-enhancer',
        name: 'Content Enhancer',
        description: 'Improve and enhance existing business content',
        icon: '✨',
        category: 'content'
    },
    {
        id: 'social-media-generator',
        name: 'Social Media Generator',
        description: 'Create social media posts and campaigns',
        icon: '📱',
        category: 'marketing'
    },
    {
        id: 'market-analyzer',
        name: 'Market Analyzer',
        description: 'Analyze market trends and competition',
        icon: '📊',
        category: 'analysis'
    }
];

interface MagicAIAssistantProps {
    businessData?: any;
    onResult?: (feature: string, result: string) => void;
    className?: string;
}

export default function MagicAIAssistant({
    businessData,
    onResult,
    className = ''
}: MagicAIAssistantProps) {
    const [activeFeature, setActiveFeature] = useState<string | null>(null);
    const [isProcessing, setIsProcessing] = useState(false);
    const [results, setResults] = useState<Record<string, string>>({});
    const [selectedCategory, setSelectedCategory] = useState<'all' | 'content' | 'marketing' | 'analysis'>('all');

    const filteredFeatures = selectedCategory === 'all'
        ? AI_FEATURES
        : AI_FEATURES.filter(feature => feature.category === selectedCategory);

    const handleFeatureClick = async (feature: MagicAIFeature) => {
        setActiveFeature(feature.id);
        setIsProcessing(true);

        // Simulate AI processing
        try {
            await new Promise(resolve => setTimeout(resolve, 2000));

            // Mock AI results based on feature type
            let mockResult = '';

            switch (feature.id) {
                case 'description-generator':
                    mockResult = businessData
                        ? `Enhanced description for ${businessData.name}: A premium establishment offering exceptional services with a focus on customer satisfaction and quality excellence.`
                        : 'Generate compelling business descriptions that attract customers and showcase your unique value proposition.';
                    break;
                case 'multilingual-translator':
                    mockResult = 'Content translated to: Français, Deutsch, Español, Italiano, and 23 other EU languages. All translations reviewed for cultural accuracy.';
                    break;
                case 'seo-optimizer':
                    mockResult = 'SEO Score: 85/100. Suggested improvements: Add location-based keywords, optimize meta descriptions, improve page loading speed. Target keywords identified: "premium services", "local business", "customer satisfaction".';
                    break;
                case 'content-enhancer':
                    mockResult = 'Content enhanced with emotional triggers, power words, and customer-focused language. Readability improved by 40%. Added compelling call-to-action elements.';
                    break;
                case 'social-media-generator':
                    mockResult = 'Generated 12 social media posts for Facebook, Instagram, and LinkedIn. Includes hashtags, optimal posting times, and engagement strategies. Estimated reach: 15,000+ users.';
                    break;
                case 'market-analyzer':
                    mockResult = 'Market Analysis: High demand in local area, 23% growth potential. Main competitors identified. Recommended pricing strategy: Premium positioning with 15% markup. Best customer acquisition channels: Social media (40%), Local SEO (35%), Referrals (25%).';
                    break;
                default:
                    mockResult = 'AI analysis completed successfully. Results processed and ready for implementation.';
            }

            setResults(prev => ({
                ...prev,
                [feature.id]: mockResult
            }));

            if (onResult) {
                onResult(feature.id, mockResult);
            }
        } catch (error) {
            console.error('AI processing error:', error);
            setResults(prev => ({
                ...prev,
                [feature.id]: 'Error processing request. Please try again.'
            }));
        } finally {
            setIsProcessing(false);
        }
    };

    return (
        <div className={`bg-white rounded-lg shadow-lg p-6 ${className}`}>
            <div className="mb-6">
                <h3 className="text-xl font-bold text-gray-900 mb-2 flex items-center">
                    <span className="text-2xl mr-2">🪄</span>
                    MagicAI Assistant
                </h3>
                <p className="text-gray-600">
                    Enhance your business with AI-powered tools for content, marketing, and analysis.
                </p>
            </div>

            {/* Category Filter */}
            <div className="mb-6">
                <div className="flex flex-wrap gap-2">
                    {[
                        { key: 'all', label: 'All Features', icon: '🔮' },
                        { key: 'content', label: 'Content', icon: '✍️' },
                        { key: 'marketing', label: 'Marketing', icon: '📱' },
                        { key: 'analysis', label: 'Analysis', icon: '📊' }
                    ].map(category => (
                        <button
                            key={category.key}
                            onClick={() => setSelectedCategory(category.key as any)}
                            className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${selectedCategory === category.key
                                    ? 'bg-blue-600 text-white'
                                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                }`}
                        >
                            <span className="mr-1">{category.icon}</span>
                            {category.label}
                        </button>
                    ))}
                </div>
            </div>

            {/* AI Features Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
                {filteredFeatures.map((feature) => (
                    <div
                        key={feature.id}
                        className={`border rounded-lg p-4 cursor-pointer transition-all hover:shadow-md ${activeFeature === feature.id
                                ? 'border-blue-500 bg-blue-50'
                                : 'border-gray-200 hover:border-gray-300'
                            }`}
                        onClick={() => handleFeatureClick(feature)}
                    >
                        <div className="flex items-start space-x-3">
                            <span className="text-2xl">{feature.icon}</span>
                            <div className="flex-1">
                                <h4 className="font-medium text-gray-900 mb-1">{feature.name}</h4>
                                <p className="text-sm text-gray-600">{feature.description}</p>

                                <div className="mt-2">
                                    <span className={`inline-block px-2 py-1 rounded-full text-xs font-medium ${feature.category === 'content' ? 'bg-green-100 text-green-800' :
                                            feature.category === 'marketing' ? 'bg-purple-100 text-purple-800' :
                                                'bg-orange-100 text-orange-800'
                                        }`}>
                                        {feature.category}
                                    </span>
                                </div>
                            </div>
                        </div>

                        {activeFeature === feature.id && isProcessing && (
                            <div className="mt-3 flex items-center text-blue-600">
                                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
                                <span className="text-sm">Processing with AI...</span>
                            </div>
                        )}
                    </div>
                ))}
            </div>

            {/* Results Section */}
            {Object.keys(results).length > 0 && (
                <div className="border-t pt-6">
                    <h4 className="font-medium text-gray-900 mb-4">AI Results</h4>
                    <div className="space-y-4">
                        {Object.entries(results).map(([featureId, result]) => {
                            const feature = AI_FEATURES.find(f => f.id === featureId);
                            return (
                                <div key={featureId} className="bg-gray-50 rounded-lg p-4">
                                    <div className="flex items-center mb-2">
                                        <span className="text-lg mr-2">{feature?.icon}</span>
                                        <span className="font-medium text-gray-900">{feature?.name}</span>
                                    </div>
                                    <p className="text-gray-700 text-sm">{result}</p>
                                </div>
                            );
                        })}
                    </div>
                </div>
            )}

            {/* Help Text */}
            <div className="mt-6 p-4 bg-blue-50 rounded-lg">
                <p className="text-sm text-blue-800">
                    <span className="font-medium">💡 Pro Tip:</span> Click on any AI feature to generate
                    intelligent suggestions for your business. Results are tailored to your specific content and industry.
                </p>
            </div>
        </div>
    );
}

export { AI_FEATURES };
export type { MagicAIFeature };