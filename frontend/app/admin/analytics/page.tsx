"use client";

import React from 'react';
import AdminLayout from '../../../components/admin/AdminLayout';
import { 
  BarChart3,
  TrendingUp,
  Users,
  Eye,
  Calendar,
  Download
} from 'lucide-react';

export default function AnalyticsPage() {
  // Analytics page - November 1, 2025
  return (
    <AdminLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 flex items-center">
              <BarChart3 className="w-8 h-8 text-blue-600 mr-3" />
              Analytics & Reporting
            </h1>
            <p className="text-gray-600 mt-2">
              Track performance metrics and generate comprehensive reports
            </p>
          </div>
          
          <div className="flex items-center space-x-3">
            <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center">
              <Download className="w-4 h-4 mr-2" />
              Export Report
            </button>
          </div>
        </div>

        {/* Coming Soon Content */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
          <div className="max-w-md mx-auto">
            <div className="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <BarChart3 className="w-10 h-10 text-blue-600" />
            </div>
            
            <h2 className="text-xl font-semibold text-gray-900 mb-3">
              Analytics Dashboard Coming Soon
            </h2>
            
            <p className="text-gray-600 mb-6">
              We're building comprehensive analytics to help you track business listings performance, 
              blog engagement, and subscription metrics. Stay tuned for detailed insights and reports.
            </p>
            
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div className="bg-gray-50 rounded-lg p-4">
                <TrendingUp className="w-6 h-6 text-green-600 mx-auto mb-2" />
                <div className="font-medium text-gray-900">Performance Metrics</div>
              </div>
              <div className="bg-gray-50 rounded-lg p-4">
                <Users className="w-6 h-6 text-blue-600 mx-auto mb-2" />
                <div className="font-medium text-gray-900">User Analytics</div>
              </div>
              <div className="bg-gray-50 rounded-lg p-4">
                <Eye className="w-6 h-6 text-purple-600 mx-auto mb-2" />
                <div className="font-medium text-gray-900">View Tracking</div>
              </div>
              <div className="bg-gray-50 rounded-lg p-4">
                <Calendar className="w-6 h-6 text-orange-600 mx-auto mb-2" />
                <div className="font-medium text-gray-900">Time-based Reports</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </AdminLayout>
  );
}