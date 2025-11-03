"use client";

import React, { useState, useEffect } from 'react';
import AdminLayout from '../../../components/admin/AdminLayout';
import { 
  Plus, 
  Search, 
  Filter, 
  Edit, 
  Trash2, 
  Eye, 
  MapPin,
  Phone,
  Mail,
  Globe,
  Star,
  CheckCircle,
  XCircle,
  Clock,
  MoreVertical
} from 'lucide-react';

interface Business {
  id: number;
  name: string;
  city: {
    name: string;
  };
  country: {
    name: string;
    code: string;
  };
  street?: string;
  phone?: string;
  email?: string;
  website?: string;
  status: 'active' | 'inactive';
  created_at: string;
  categories?: Array<{
    slug: string;
    names_json: Record<string, string>;
  }>;
}

const BusinessManagement: React.FC = () => {
  const [businesses, setBusinesses] = useState<Business[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterCountry, setFilterCountry] = useState('all');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);

  useEffect(() => {
    fetchBusinesses();
  }, [currentPage, filterStatus, filterCountry]);

  const fetchBusinesses = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      params.append('page', currentPage.toString());
      params.append('page_size', '10');
      if (filterStatus !== 'all') params.append('status', filterStatus);
      if (filterCountry !== 'all') params.append('country', filterCountry);
      if (searchTerm) params.append('search', searchTerm);

      const response = await fetch(`http://127.0.0.1:8000/api/businesses/?${params}`);
      const data = await response.json();
      setBusinesses(data.results || []);
      setTotalCount(data.count || 0);
    } catch (error) {
      console.error('Error fetching businesses:', error);
      // Mock data for development
      setBusinesses([
        {
          id: 1,
          name: 'Café Central',
          city: { name: 'Vienna' },
          country: { name: 'Austria', code: 'AT' },
          street: 'Herrengasse 14',
          phone: '+43 1 533 37 64',
          email: 'info@cafecentral.wien',
          website: 'https://cafecentral.wien',
          status: 'active',
          created_at: '2024-10-15T10:30:00Z',
          categories: [
            { slug: 'restaurants', names_json: { en: 'Restaurants' } }
          ]
        },
        {
          id: 2,
          name: 'Tech Solutions Ltd',
          city: { name: 'Berlin' },
          country: { name: 'Germany', code: 'DE' },
          street: 'Unter den Linden 77',
          phone: '+49 30 2062 1234',
          email: 'contact@techsolutions.de',
          website: 'https://techsolutions.de',
          status: 'active',
          created_at: '2024-10-14T14:20:00Z',
          categories: [
            { slug: 'technology', names_json: { en: 'Technology' } }
          ]
        },
        {
          id: 3,
          name: 'Bistro Le Paris',
          city: { name: 'Paris' },
          country: { name: 'France', code: 'FR' },
          street: 'Rue de Rivoli 123',
          phone: '+33 1 42 97 48 85',
          email: 'contact@bistroleparis.fr',
          status: 'inactive',
          created_at: '2024-10-13T09:15:00Z',
          categories: [
            { slug: 'restaurants', names_json: { en: 'Restaurants' } }
          ]
        }
      ]);
      setTotalCount(3);
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status: string) => {
    if (status === 'active') {
      return {
        icon: CheckCircle,
        className: 'bg-green-100 text-green-800',
        iconClassName: 'text-green-500'
      };
    }
    return {
      icon: XCircle,
      className: 'bg-red-100 text-red-800',
      iconClassName: 'text-red-500'
    };
  };

  const getCountryFlag = (countryCode: string) => {
    const flags: Record<string, string> = {
      AT: '🇦🇹', DE: '🇩🇪', FR: '🇫🇷', IT: '🇮🇹', ES: '🇪🇸',
      PT: '🇵🇹', NL: '🇳🇱', BE: '🇧🇪', PL: '🇵🇱', CZ: '🇨🇿'
    };
    return flags[countryCode] || '🌐';
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const toggleBusinessStatus = async (businessId: number, currentStatus: string) => {
    const newStatus = currentStatus === 'active' ? 'inactive' : 'active';
    // In real app, make API call to update business status
    setBusinesses(businesses.map(business => 
      business.id === businessId ? { ...business, status: newStatus as 'active' | 'inactive' } : business
    ));
  };

  const filteredBusinesses = businesses.filter(business => {
    const matchesSearch = business.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         business.city.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = filterStatus === 'all' || business.status === filterStatus;
    const matchesCountry = filterCountry === 'all' || business.country.code === filterCountry;
    return matchesSearch && matchesStatus && matchesCountry;
  });

  return (
    <AdminLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Business Management</h1>
            <p className="text-gray-600 mt-2">Manage and verify business listings across the EU</p>
          </div>
          <button className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
            <Plus className="w-5 h-5 mr-2" />
            Add Business
          </button>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center">
              <CheckCircle className="w-8 h-8 text-green-500" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Active Businesses</p>
                <p className="text-2xl font-bold text-gray-900">
                  {businesses.filter(b => b.status === 'active').length}
                </p>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center">
              <XCircle className="w-8 h-8 text-red-500" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Inactive Businesses</p>
                <p className="text-2xl font-bold text-gray-900">
                  {businesses.filter(b => b.status === 'inactive').length}
                </p>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center">
              <Clock className="w-8 h-8 text-yellow-500" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Pending Review</p>
                <p className="text-2xl font-bold text-gray-900">23</p>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center">
              <Star className="w-8 h-8 text-purple-500" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Featured</p>
                <p className="text-2xl font-bold text-gray-900">156</p>
              </div>
            </div>
          </div>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Search businesses..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
            
            <select
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
            >
              <option value="all">All Status</option>
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
            </select>

            <select
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              value={filterCountry}
              onChange={(e) => setFilterCountry(e.target.value)}
            >
              <option value="all">All Countries</option>
              <option value="AT">🇦🇹 Austria</option>
              <option value="DE">🇩🇪 Germany</option>
              <option value="FR">🇫🇷 France</option>
              <option value="IT">🇮🇹 Italy</option>
              <option value="ES">🇪🇸 Spain</option>
            </select>

            <button className="inline-flex items-center justify-center px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
              <Filter className="w-5 h-5 mr-2" />
              More Filters
            </button>
          </div>
        </div>

        {/* Businesses Table */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          {loading ? (
            <div className="p-8 text-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
              <p className="text-gray-500 mt-2">Loading businesses...</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Business
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Location
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Contact
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Date Added
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {filteredBusinesses.map((business) => {
                    const statusInfo = getStatusBadge(business.status);
                    const StatusIcon = statusInfo.icon;

                    return (
                      <tr key={business.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4">
                          <div className="flex items-center">
                            <div>
                              <div className="text-sm font-medium text-gray-900">
                                {business.name}
                              </div>
                              {business.categories && business.categories.length > 0 && (
                                <div className="text-sm text-gray-500">
                                  {business.categories.map(cat => cat.names_json.en).join(', ')}
                                </div>
                              )}
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center space-x-2">
                            <span className="text-lg">{getCountryFlag(business.country.code)}</span>
                            <div>
                              <div className="text-sm text-gray-900">{business.city.name}</div>
                              <div className="text-xs text-gray-500">{business.country.name}</div>
                              {business.street && (
                                <div className="text-xs text-gray-400">{business.street}</div>
                              )}
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="space-y-1">
                            {business.phone && (
                              <div className="flex items-center space-x-1 text-sm text-gray-600">
                                <Phone className="w-3 h-3" />
                                <span>{business.phone}</span>
                              </div>
                            )}
                            {business.email && (
                              <div className="flex items-center space-x-1 text-sm text-gray-600">
                                <Mail className="w-3 h-3" />
                                <span className="truncate max-w-32">{business.email}</span>
                              </div>
                            )}
                            {business.website && (
                              <div className="flex items-center space-x-1 text-sm text-gray-600">
                                <Globe className="w-3 h-3" />
                                <span>Website</span>
                              </div>
                            )}
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <button
                            onClick={() => toggleBusinessStatus(business.id, business.status)}
                            className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${statusInfo.className} hover:opacity-80 transition-opacity`}
                          >
                            <StatusIcon className={`w-3 h-3 mr-1 ${statusInfo.iconClassName}`} />
                            {business.status}
                          </button>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {formatDate(business.created_at)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                          <div className="flex items-center justify-end space-x-2">
                            <button className="text-blue-600 hover:text-blue-900 p-1 rounded">
                              <Eye className="w-4 h-4" />
                            </button>
                            <button className="text-gray-600 hover:text-gray-900 p-1 rounded">
                              <Edit className="w-4 h-4" />
                            </button>
                            <button className="text-red-600 hover:text-red-900 p-1 rounded">
                              <Trash2 className="w-4 h-4" />
                            </button>
                            <button className="text-gray-400 hover:text-gray-600 p-1 rounded">
                              <MoreVertical className="w-4 h-4" />
                            </button>
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}

          {/* Pagination */}
          <div className="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
            <div className="flex-1 flex justify-between sm:hidden">
              <button 
                disabled={currentPage === 1}
                onClick={() => setCurrentPage(currentPage - 1)}
                className="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Previous
              </button>
              <button 
                disabled={filteredBusinesses.length < 10}
                onClick={() => setCurrentPage(currentPage + 1)}
                className="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next
              </button>
            </div>
            <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
              <div>
                <p className="text-sm text-gray-700">
                  Showing <span className="font-medium">{((currentPage - 1) * 10) + 1}</span> to{' '}
                  <span className="font-medium">{Math.min(currentPage * 10, totalCount)}</span> of{' '}
                  <span className="font-medium">{totalCount}</span> results
                </p>
              </div>
              <div className="flex space-x-2">
                <button
                  disabled={currentPage === 1}
                  onClick={() => setCurrentPage(currentPage - 1)}
                  className="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Previous
                </button>
                <button
                  disabled={filteredBusinesses.length < 10}
                  onClick={() => setCurrentPage(currentPage + 1)}
                  className="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Next
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </AdminLayout>
  );
};

export default BusinessManagement;