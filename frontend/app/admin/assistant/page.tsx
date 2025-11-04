"use client";

import React from 'react';
import AdminLayout from '../../../components/admin/AdminLayout';
import AssistantPanel from '../../../components/AssistantPanel';
import AssistantEditor from '../../../components/AssistantEditor';
import AssistantPublishPanel from '../../../components/AssistantPublishPanel';
import AssistantKBPanel from '../../../components/AssistantKBPanel';
import AssistantToolsPanel from '../../../components/AssistantToolsPanel';
import AssistantIntentsPanel from '../../../components/admin/AssistantIntentsPanel';
import AssistantChatTest from '../../../components/AssistantChatTest';
import { Bot, MessageSquare, Lightbulb, BarChart3, FileEdit, Settings, GitBranch, Database, Wrench, Target } from 'lucide-react';

export default function AssistantPage() {
    return (
        <AdminLayout>
            {/* Page Header */}
            <div className="border-b border-gray-200 pb-6 mb-8 bg-white -mx-4 px-4 sm:-mx-6 sm:px-6 lg:-mx-8 lg:px-8 pt-2">
                <h1 className="text-3xl font-bold text-gray-900">AI Assistant</h1>
                <p className="text-gray-600 mt-2">Intelligent help for managing your business listings and content</p>
            </div>

            <div className="space-y-8">

                {/* Quick Actions */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
                        <div className="flex items-center">
                            <div className="p-2 bg-blue-100 rounded-lg">
                                <MessageSquare className="h-6 w-6 text-blue-600" />
                            </div>
                            <div className="ml-4">
                                <h3 className="text-lg font-medium text-gray-900">Chat Assistant</h3>
                                <p className="text-sm text-gray-500">Ask questions and get help</p>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
                        <div className="flex items-center">
                            <div className="p-2 bg-green-100 rounded-lg">
                                <FileEdit className="h-6 w-6 text-green-600" />
                            </div>
                            <div className="ml-4">
                                <h3 className="text-lg font-medium text-gray-900">Content Generation</h3>
                                <p className="text-sm text-gray-500">Auto-create descriptions</p>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
                        <div className="flex items-center">
                            <div className="p-2 bg-purple-100 rounded-lg">
                                <Lightbulb className="h-6 w-6 text-purple-600" />
                            </div>
                            <div className="ml-4">
                                <h3 className="text-lg font-medium text-gray-900">SEO Suggestions</h3>
                                <p className="text-sm text-gray-500">Optimize your listings</p>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
                        <div className="flex items-center">
                            <div className="p-2 bg-orange-100 rounded-lg">
                                <BarChart3 className="h-6 w-6 text-orange-600" />
                            </div>
                            <div className="ml-4">
                                <h3 className="text-lg font-medium text-gray-900">Analytics Insights</h3>
                                <p className="text-sm text-gray-500">Performance recommendations</p>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Assistant Configuration */}
                <div className="bg-white rounded-lg shadow-sm border border-gray-200">
                    <div className="px-6 py-4 border-b border-gray-200">
                        <div className="flex items-center">
                            <Bot className="h-6 w-6 text-blue-600 mr-3" />
                            <h2 className="text-lg font-medium text-gray-900">Assistant Configuration</h2>
                        </div>
                    </div>

                    <div className="p-6">
                        <AssistantPanel />
                    </div>
                </div>

                {/* Assistant Editor */}
                <div className="bg-white rounded-lg shadow-sm border border-gray-200">
                    <div className="px-6 py-4 border-b border-gray-200">
                        <div className="flex items-center">
                            <Settings className="h-6 w-6 text-purple-600 mr-3" />
                            <h2 className="text-lg font-medium text-gray-900">Configuration Editor</h2>
                        </div>
                    </div>

                    <div className="p-6">
                        <AssistantEditor />
                    </div>
                </div>

                {/* Knowledge Base Management */}
                <div className="bg-white rounded-lg shadow-sm border border-gray-200">
                    <div className="px-6 py-4 border-b border-gray-200">
                        <div className="flex items-center">
                            <Database className="h-6 w-6 text-orange-600 mr-3" />
                            <h2 className="text-lg font-medium text-gray-900">Knowledge Base</h2>
                        </div>
                    </div>

                    <div className="p-6">
                        <AssistantKBPanel />
                    </div>
                </div>

                {/* Intent Management */}
                <div className="bg-white rounded-lg shadow-sm border border-gray-200">
                    <div className="px-6 py-4 border-b border-gray-200">
                        <div className="flex items-center">
                            <Target className="h-6 w-6 text-red-600 mr-3" />
                            <h2 className="text-lg font-medium text-gray-900">Intents (Step 8)</h2>
                        </div>
                    </div>

                    <div className="p-6">
                        <AssistantIntentsPanel />
                    </div>
                </div>

                {/* Chat Testing */}
                <div className="bg-white rounded-lg shadow-sm border border-gray-200">
                    <div className="px-6 py-4 border-b border-gray-200">
                        <div className="flex items-center">
                            <MessageSquare className="h-6 w-6 text-purple-600 mr-3" />
                            <h2 className="text-lg font-medium text-gray-900">Assistant Chat Test (Step 9)</h2>
                        </div>
                    </div>

                    <div className="p-6">
                        <AssistantChatTest />
                    </div>
                </div>

                {/* Action Tools Testing */}
                <div className="bg-white rounded-lg shadow-sm border border-gray-200">
                    <div className="px-6 py-4 border-b border-gray-200">
                        <div className="flex items-center">
                            <Wrench className="h-6 w-6 text-indigo-600 mr-3" />
                            <h2 className="text-lg font-medium text-gray-900">Action Tools (Step 7)</h2>
                        </div>
                    </div>

                    <div className="p-6">
                        <AssistantToolsPanel />
                    </div>
                </div>

                {/* Publish & Version Control */}
                <div className="bg-white rounded-lg shadow-sm border border-gray-200">
                    <div className="px-6 py-4 border-b border-gray-200">
                        <div className="flex items-center">
                            <GitBranch className="h-6 w-6 text-green-600 mr-3" />
                            <h2 className="text-lg font-medium text-gray-900">Publish & Version Control</h2>
                        </div>
                    </div>

                    <div className="p-6">
                        <AssistantPublishPanel />
                    </div>
                </div>

                {/* Main Assistant Interface */}
                <div className="bg-white rounded-lg shadow-sm border border-gray-200">
                    <div className="px-6 py-4 border-b border-gray-200">
                        <div className="flex items-center">
                            <Bot className="h-6 w-6 text-blue-600 mr-3" />
                            <h2 className="text-lg font-medium text-gray-900">Assistant Chat</h2>
                        </div>
                    </div>

                    <div className="p-6">
                        {/* Coming Soon Message */}
                        <div className="text-center py-12">
                            <div className="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-blue-100 mb-6">
                                <Bot className="h-8 w-8 text-blue-600" />
                            </div>
                            <h3 className="text-lg font-medium text-gray-900 mb-2">AI Assistant Coming Soon</h3>
                            <p className="text-gray-500 mb-8 max-w-md mx-auto">
                                We're building an intelligent assistant to help you manage your business listings,
                                create content, and optimize your presence across Europe.
                            </p>

                            {/* Feature Preview */}
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-2xl mx-auto">
                                <div className="text-left p-4 bg-gray-50 rounded-lg">
                                    <h4 className="font-medium text-gray-900 mb-2">Smart Content Creation</h4>
                                    <p className="text-sm text-gray-600">
                                        Generate compelling business descriptions, blog posts, and marketing copy
                                        tailored to your target markets.
                                    </p>
                                </div>

                                <div className="text-left p-4 bg-gray-50 rounded-lg">
                                    <h4 className="font-medium text-gray-900 mb-2">SEO Optimization</h4>
                                    <p className="text-sm text-gray-600">
                                        Get personalized recommendations to improve your search rankings
                                        and visibility across different European markets.
                                    </p>
                                </div>

                                <div className="text-left p-4 bg-gray-50 rounded-lg">
                                    <h4 className="font-medium text-gray-900 mb-2">Market Insights</h4>
                                    <p className="text-sm text-gray-600">
                                        Receive intelligent analysis of your performance data and
                                        actionable insights to grow your business.
                                    </p>
                                </div>

                                <div className="text-left p-4 bg-gray-50 rounded-lg">
                                    <h4 className="font-medium text-gray-900 mb-2">Multi-language Support</h4>
                                    <p className="text-sm text-gray-600">
                                        Create and optimize content in multiple European languages
                                        to reach broader audiences.
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </AdminLayout>
    );
}