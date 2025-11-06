'use client';

import { Metadata } from 'next';
import Link from 'next/link';
import { useState, useEffect } from 'react';
import { fetchDashboardStats, fetchBusinesses, fetchBlogPosts } from '@/lib/django-admin-api';

// Dashboard stats interface
interface DashboardStat {
  title: string;
  value: string;
  change: string;
  color: string;
}

// Mock data as fallback
const fallbackStats: DashboardStat[] = [
  { title: 'Total Blog Posts', value: '24', change: '+12%', color: 'text-blue-600' },
  { title: 'Business Listings', value: '156', change: '+8%', color: 'text-green-600' },
  { title: 'Featured Businesses', value: '12', change: '+4%', color: 'text-purple-600' },
  { title: 'Monthly Views', value: '8.4K', change: '+23%', color: 'text-orange-600' },
];

const recentActivity = [
  { action: 'New blog post published', item: 'EU Business Opportunities', time: '2 hours ago' },
  { action: 'Business listing updated', item: 'Tech Solutions Berlin', time: '4 hours ago' },
  { action: 'Category created', item: 'Digital Marketing', time: '1 day ago' },
  { action: 'SEO metadata updated', item: 'Homepage', time: '2 days ago' },
];

export default function AdminDashboard() {
  const [dashboardStats, setDashboardStats] = useState<DashboardStat[]>(fallbackStats);
  const [isLoading, setIsLoading] = useState(true);
  const [businesses, setBusinesses] = useState<any[]>([]);
  const [blogPosts, setBlogPosts] = useState<any[]>([]);

  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        // Try to fetch real data from Django
        const [businessData, blogData] = await Promise.all([
          fetchBusinesses(),
          fetchBlogPosts()
        ]);

        if (businessData && blogData) {
          setBusinesses(businessData);
          setBlogPosts(blogData);
          
          // Update stats with real data
          const realStats: DashboardStat[] = [
            { title: 'Total Blog Posts', value: blogData.length.toString(), change: '+12%', color: 'text-blue-600' },
            { title: 'Business Listings', value: businessData.length.toString(), change: '+8%', color: 'text-green-600' },
            { title: 'Featured Businesses', value: businessData.filter((b: any) => b.is_featured).length.toString(), change: '+4%', color: 'text-purple-600' },
            { title: 'Active Listings', value: businessData.filter((b: any) => b.is_active).length.toString(), change: '+23%', color: 'text-orange-600' },
          ];
          setDashboardStats(realStats);
        }
      } catch (error) {
        console.error('Failed to load dashboard data:', error);
        // Keep fallback stats
      } finally {
        setIsLoading(false);
      }
    };

    loadDashboardData();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <p className="mt-1 text-sm text-gray-600">
            Welcome to the ListAcross EU admin panel. Manage your content and monitor site performance.
          </p>
        </div>
        
        <div className="flex space-x-3">
          <Link
            href="/admin/django"
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
          >
            Django Admin
          </Link>
          <a
            href="http://127.0.0.1:8000/admin/"
            target="_blank"
            rel="noopener noreferrer"
            className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
          >
            Direct Access
          </a>
        </div>
      </div>

      {/* Django Connection Status */}
      <div className={`p-4 rounded-lg border ${isLoading ? 'bg-yellow-50 border-yellow-200' : 'bg-green-50 border-green-200'}`}>
        <div className="flex items-center">
          <div className={`w-3 h-3 rounded-full mr-3 ${isLoading ? 'bg-yellow-400 animate-pulse' : 'bg-green-400'}`}></div>
          <span className={`text-sm font-medium ${isLoading ? 'text-yellow-800' : 'text-green-800'}`}>
            {isLoading ? 'Connecting to Django backend...' : `Django backend connected (${businesses.length} businesses, ${blogPosts.length} posts)`}
          </span>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {dashboardStats.map((stat: DashboardStat) => (
          <div key={stat.title} className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
              </div>
              <div className={`text-sm ${stat.color}`}>
                {stat.change}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow">
        <div className="p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Quick Actions</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Link 
              href="/admin/blog/posts/new"
              className="flex items-center p-4 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors"
            >
              <svg className="w-8 h-8 text-blue-600 mr-3" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
              </svg>
              <div>
                <h4 className="font-medium text-gray-900">Create Blog Post</h4>
                <p className="text-sm text-gray-600">Add new content to your blog</p>
              </div>
            </Link>

            <Link 
              href="/admin/businesses/new"
              className="flex items-center p-4 bg-green-50 rounded-lg hover:bg-green-100 transition-colors"
            >
              <svg className="w-8 h-8 text-green-600 mr-3" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M4 4a2 2 0 00-2 2v8a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2H4zm3 5a1 1 0 011-1h4a1 1 0 110 2H8a1 1 0 01-1-1zm0 3a1 1 0 011-1h4a1 1 0 110 2H8a1 1 0 01-1-1z" clipRule="evenodd" />
              </svg>
              <div>
                <h4 className="font-medium text-gray-900">Add Business</h4>
                <p className="text-sm text-gray-600">List a new business</p>
              </div>
            </Link>

            <Link 
              href="/admin/pages"
              className="flex items-center p-4 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors"
            >
              <svg className="w-8 h-8 text-purple-600 mr-3" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11.707 4.707a1 1 0 00-1.414-1.414L10 9.586 8.707 8.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <div>
                <h4 className="font-medium text-gray-900">Manage SEO</h4>
                <p className="text-sm text-gray-600">SEO settings in Website Preview</p>
              </div>
            </Link>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow">
        <div className="p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Recent Activity</h3>
          <div className="flow-root">
            <ul className="-mb-8">
              {recentActivity.map((activity, index) => (
                <li key={index}>
                  <div className="relative pb-8">
                    {index < recentActivity.length - 1 && (
                      <span className="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200" />
                    )}
                    <div className="relative flex space-x-3">
                      <div>
                        <span className="h-8 w-8 rounded-full bg-blue-500 flex items-center justify-center ring-8 ring-white">
                          <svg className="h-5 w-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                          </svg>
                        </span>
                      </div>
                      <div className="min-w-0 flex-1 pt-1.5 flex justify-between space-x-4">
                        <div>
                          <p className="text-sm text-gray-500">
                            {activity.action}{' '}
                            <span className="font-medium text-gray-900">{activity.item}</span>
                          </p>
                        </div>
                        <div className="text-right text-sm whitespace-nowrap text-gray-500">
                          {activity.time}
                        </div>
                      </div>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}