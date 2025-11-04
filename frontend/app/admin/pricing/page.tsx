"use client";

import React, { useState, useEffect } from 'react';
import AdminLayout from '../../../components/admin/AdminLayout';
import {
    Plus,
    Edit,
    Trash2,
    Star,
    DollarSign,
    Users,
    Check,
    X,
    MoreVertical,
    Eye
} from 'lucide-react';

interface PricingPlan {
    id: number;
    name: string;
    description: string;
    price: number;
    currency: string;
    billing_cycle: 'monthly' | 'yearly' | 'one_time';
    features: string[];
    max_listings: number;
    max_images: number;
    priority_support: boolean;
    is_active: boolean;
    is_featured: boolean;
    color_scheme: 'blue' | 'green' | 'purple' | 'gold';
    order: number;
    trial_days: number;
}

const PricingManagement: React.FC = () => {
    const [plans, setPlans] = useState<PricingPlan[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchPlans();
    }, []);

    const fetchPlans = async () => {
        try {
            setLoading(true);
            const response = await fetch('http://127.0.0.1:8000/api/blog/v2/pricing/');
            const data = await response.json();
            setPlans(data.results || []);
        } catch (error) {
            console.error('Error fetching pricing plans:', error);
            // Mock data for development
            setPlans([
                {
                    id: 1,
                    name: 'Starter',
                    description: 'Perfect for new businesses just starting out',
                    price: 0,
                    currency: 'EUR',
                    billing_cycle: 'monthly',
                    features: [
                        '1 Business listing',
                        'Basic contact information',
                        'Community support',
                        'Mobile-friendly profile'
                    ],
                    max_listings: 1,
                    max_images: 3,
                    priority_support: false,
                    is_active: true,
                    is_featured: false,
                    color_scheme: 'blue',
                    order: 1,
                    trial_days: 0
                },
                {
                    id: 2,
                    name: 'Professional',
                    description: 'For growing businesses that need more visibility',
                    price: 29.99,
                    currency: 'EUR',
                    billing_cycle: 'monthly',
                    features: [
                        'Up to 5 business listings',
                        'Enhanced business profiles',
                        'Priority listing placement',
                        'Analytics dashboard',
                        'Email support',
                        'Custom business hours',
                        'Photo gallery (up to 10 images per listing)'
                    ],
                    max_listings: 5,
                    max_images: 10,
                    priority_support: false,
                    is_active: true,
                    is_featured: true,
                    color_scheme: 'green',
                    order: 2,
                    trial_days: 14
                },
                {
                    id: 3,
                    name: 'Enterprise',
                    description: 'Comprehensive solution for large businesses and franchises',
                    price: 99.99,
                    currency: 'EUR',
                    billing_cycle: 'monthly',
                    features: [
                        'Unlimited business listings',
                        'Premium business profiles',
                        'Top placement guarantee',
                        'Advanced analytics & insights',
                        'Priority phone & email support',
                        'API access for integrations',
                        'Custom branding options',
                        'Bulk listing management',
                        'Dedicated account manager'
                    ],
                    max_listings: 999999,
                    max_images: 50,
                    priority_support: true,
                    is_active: true,
                    is_featured: false,
                    color_scheme: 'purple',
                    order: 3,
                    trial_days: 30
                }
            ]);
        } finally {
            setLoading(false);
        }
    };

    const getColorClasses = (scheme: string, type: 'card' | 'badge' | 'button') => {
        const colors = {
            blue: {
                card: 'border-blue-200 bg-blue-50',
                badge: 'bg-blue-100 text-blue-800',
                button: 'bg-blue-600 hover:bg-blue-700'
            },
            green: {
                card: 'border-green-200 bg-green-50',
                badge: 'bg-green-100 text-green-800',
                button: 'bg-green-600 hover:bg-green-700'
            },
            purple: {
                card: 'border-purple-200 bg-purple-50',
                badge: 'bg-purple-100 text-purple-800',
                button: 'bg-purple-600 hover:bg-purple-700'
            },
            gold: {
                card: 'border-yellow-200 bg-yellow-50',
                badge: 'bg-yellow-100 text-yellow-800',
                button: 'bg-yellow-600 hover:bg-yellow-700'
            }
        };
        return colors[scheme as keyof typeof colors]?.[type] || colors.blue[type];
    };

    const formatPrice = (price: number, currency: string, billingCycle: string) => {
        if (price === 0) return 'Free';
        const formatted = new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: currency,
        }).format(price);

        if (billingCycle === 'monthly') return `${formatted}/month`;
        if (billingCycle === 'yearly') return `${formatted}/year`;
        return formatted;
    };

    const togglePlanStatus = async (planId: number, currentStatus: boolean) => {
        // In real app, make API call to update plan status
        setPlans(plans.map(plan =>
            plan.id === planId ? { ...plan, is_active: !currentStatus } : plan
        ));
    };

    const toggleFeaturedStatus = async (planId: number, currentStatus: boolean) => {
        // In real app, make API call to update featured status
        setPlans(plans.map(plan =>
            plan.id === planId ? { ...plan, is_featured: !currentStatus } : plan
        ));
    };

    return (
        <AdminLayout>
            <div className="space-y-6">
                {/* Header */}
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900">Pricing Plans</h1>
                        <p className="text-gray-600 mt-2">Manage subscription plans and pricing for your platform</p>
                    </div>
                    <button className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                        <Plus className="w-5 h-5 mr-2" />
                        New Plan
                    </button>
                </div>

                {/* Plans Grid */}
                {loading ? (
                    <div className="flex items-center justify-center py-12">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                        <span className="ml-2 text-gray-600">Loading pricing plans...</span>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
                        {plans.map((plan) => (
                            <div
                                key={plan.id}
                                className={`
                  relative bg-white rounded-xl shadow-sm border-2 p-6 hover:shadow-lg transition-shadow
                  ${plan.is_featured ? getColorClasses(plan.color_scheme, 'card') : 'border-gray-200'}
                `}
                            >
                                {/* Featured Badge */}
                                {plan.is_featured && (
                                    <div className="absolute -top-3 left-6">
                                        <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${getColorClasses(plan.color_scheme, 'badge')}`}>
                                            <Star className="w-3 h-3 mr-1" />
                                            Featured
                                        </span>
                                    </div>
                                )}

                                {/* Plan Header */}
                                <div className="text-center pb-6 border-b border-gray-200">
                                    <h3 className="text-xl font-bold text-gray-900">{plan.name}</h3>
                                    <p className="text-sm text-gray-600 mt-2">{plan.description}</p>
                                    <div className="mt-4">
                                        <span className="text-4xl font-bold text-gray-900">
                                            {formatPrice(plan.price, plan.currency, plan.billing_cycle)}
                                        </span>
                                    </div>
                                    {plan.trial_days > 0 && (
                                        <p className="text-sm text-green-600 mt-2">
                                            {plan.trial_days}-day free trial
                                        </p>
                                    )}
                                </div>

                                {/* Plan Details */}
                                <div className="py-6 space-y-4">
                                    <div className="flex justify-between items-center text-sm">
                                        <span className="text-gray-600">Max Listings:</span>
                                        <span className="font-medium">
                                            {plan.max_listings === 999999 ? 'Unlimited' : plan.max_listings}
                                        </span>
                                    </div>
                                    <div className="flex justify-between items-center text-sm">
                                        <span className="text-gray-600">Max Images:</span>
                                        <span className="font-medium">{plan.max_images}</span>
                                    </div>
                                    <div className="flex justify-between items-center text-sm">
                                        <span className="text-gray-600">Priority Support:</span>
                                        <div className="flex items-center">
                                            {plan.priority_support ? (
                                                <Check className="w-4 h-4 text-green-500" />
                                            ) : (
                                                <X className="w-4 h-4 text-red-500" />
                                            )}
                                        </div>
                                    </div>
                                </div>

                                {/* Features List */}
                                <div className="py-4 border-t border-gray-200">
                                    <h4 className="text-sm font-medium text-gray-900 mb-3">Features:</h4>
                                    <ul className="space-y-2">
                                        {plan.features.slice(0, 4).map((feature, index) => (
                                            <li key={index} className="flex items-start space-x-2 text-sm text-gray-600">
                                                <Check className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
                                                <span>{feature}</span>
                                            </li>
                                        ))}
                                        {plan.features.length > 4 && (
                                            <li className="text-sm text-gray-500">
                                                +{plan.features.length - 4} more features
                                            </li>
                                        )}
                                    </ul>
                                </div>

                                {/* Plan Actions */}
                                <div className="pt-6 border-t border-gray-200 space-y-3">
                                    {/* Status Toggles */}
                                    <div className="flex items-center justify-between">
                                        <div className="flex items-center space-x-4">
                                            <label className="flex items-center">
                                                <input
                                                    type="checkbox"
                                                    checked={plan.is_active}
                                                    onChange={() => togglePlanStatus(plan.id, plan.is_active)}
                                                    className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                                                />
                                                <span className="ml-2 text-sm text-gray-600">Active</span>
                                            </label>
                                            <label className="flex items-center">
                                                <input
                                                    type="checkbox"
                                                    checked={plan.is_featured}
                                                    onChange={() => toggleFeaturedStatus(plan.id, plan.is_featured)}
                                                    className="rounded border-gray-300 text-yellow-600 focus:ring-yellow-500"
                                                />
                                                <span className="ml-2 text-sm text-gray-600">Featured</span>
                                            </label>
                                        </div>
                                    </div>

                                    {/* Action Buttons */}
                                    <div className="flex items-center justify-between">
                                        <div className="flex items-center space-x-2">
                                            <button className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors">
                                                <Eye className="w-4 h-4" />
                                            </button>
                                            <button className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-50 rounded-lg transition-colors">
                                                <Edit className="w-4 h-4" />
                                            </button>
                                            <button className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors">
                                                <Trash2 className="w-4 h-4" />
                                            </button>
                                        </div>
                                        <button className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-50 rounded-lg transition-colors">
                                            <MoreVertical className="w-4 h-4" />
                                        </button>
                                    </div>
                                </div>

                                {/* Subscribers Count (Mock) */}
                                <div className="mt-4 p-3 bg-gray-50 rounded-lg">
                                    <div className="flex items-center justify-between text-sm">
                                        <span className="text-gray-600">Current Subscribers:</span>
                                        <div className="flex items-center space-x-1">
                                            <Users className="w-4 h-4 text-gray-400" />
                                            <span className="font-medium">
                                                {plan.id === 1 ? '1,234' : plan.id === 2 ? '567' : '89'}
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}

                {/* Summary Stats */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mt-8">
                    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                        <div className="flex items-center">
                            <DollarSign className="w-8 h-8 text-green-500" />
                            <div className="ml-4">
                                <p className="text-sm font-medium text-gray-600">Total Revenue</p>
                                <p className="text-2xl font-bold text-gray-900">€8,456</p>
                            </div>
                        </div>
                    </div>
                    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                        <div className="flex items-center">
                            <Users className="w-8 h-8 text-blue-500" />
                            <div className="ml-4">
                                <p className="text-sm font-medium text-gray-600">Total Subscribers</p>
                                <p className="text-2xl font-bold text-gray-900">1,890</p>
                            </div>
                        </div>
                    </div>
                    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                        <div className="flex items-center">
                            <Star className="w-8 h-8 text-yellow-500" />
                            <div className="ml-4">
                                <p className="text-sm font-medium text-gray-600">Featured Plans</p>
                                <p className="text-2xl font-bold text-gray-900">1</p>
                            </div>
                        </div>
                    </div>
                    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                        <div className="flex items-center">
                            <Check className="w-8 h-8 text-green-500" />
                            <div className="ml-4">
                                <p className="text-sm font-medium text-gray-600">Active Plans</p>
                                <p className="text-2xl font-bold text-gray-900">{plans.filter(p => p.is_active).length}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </AdminLayout>
    );
};

export default PricingManagement;