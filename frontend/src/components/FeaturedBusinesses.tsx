"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { apiCall } from "@/lib/api";

interface Business {
  id: number;
  name: string;
  description: string;
  category: {
    name: string;
    slug: string;
  };
  city: string;
  country: string;
  address: string;
  website?: string;
  phone?: string;
  email?: string;
}

interface FeaturedBusinessesProps {
  lang: string;
  country?: string;
  scope?: string;
  limit?: number;
}

export default function FeaturedBusinesses({ 
  lang, 
  country, 
  scope, 
  limit = 12 
}: FeaturedBusinessesProps) {
  const [businesses, setBusinesses] = useState<Business[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchBusinesses = async () => {
      try {
        setLoading(true);
        const params = new URLSearchParams();
        
        if (scope?.toUpperCase() === "EU") {
          params.set("scope", "EU");
        } else if (country) {
          params.set("country", country);
        }
        
        params.set("limit", limit.toString());
        
        const data = await apiCall(`/featured/?${params.toString()}`);
        setBusinesses(data?.results || []);
      } catch (error) {
        console.error('Error fetching featured businesses:', error);
        setBusinesses([]);
      } finally {
        setLoading(false);
      }
    };

    fetchBusinesses();
  }, [country, scope, limit]);

  if (loading) {
    return (
      <section className="mt-10">
        <h2 className="mb-6 text-lg font-semibold">
          {scope?.toUpperCase() === "EU" ? "Featured across the EU" : `Featured in ${country || "Europe"}`}
        </h2>
        <div className="grid gap-4 md:grid-cols-3 lg:grid-cols-4">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="bg-gray-200 animate-pulse rounded-lg h-48"></div>
          ))}
        </div>
      </section>
    );
  }

  if (!businesses.length) {
    return null;
  }

  return (
    <section className="mt-10">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-lg font-semibold">
          {scope?.toUpperCase() === "EU" ? (
            <span className="flex items-center">
              🇪🇺 Featured across the EU
            </span>
          ) : (
            `✨ Featured in ${country || "Europe"}`
          )}
        </h2>
        <Link 
          href={`/${lang}/search${scope === 'EU' ? '?scope=EU' : country ? `?country=${country}` : ''}`}
          className="text-blue-600 hover:text-blue-800 text-sm font-medium"
        >
          View all →
        </Link>
      </div>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        {businesses.map((business) => (
          <article 
            key={`${business.id}-${business.name}`} 
            className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden"
          >
            <div className="p-4">
              <div className="mb-2">
                <span className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
                  ⭐ Featured
                </span>
              </div>
              
              <h3 className="font-semibold text-gray-900 mb-2 line-clamp-1">
                {business.name}
              </h3>
              
              <div className="text-sm text-gray-600 mb-3">
                <div className="flex items-center mb-1">
                  <span className="font-medium">{business.category.name}</span>
                </div>
                <div className="flex items-center text-xs">
                  📍 {business.city}, {business.country}
                </div>
              </div>
              
              {business.description && (
                <p className="text-sm text-gray-600 line-clamp-2 mb-3">
                  {business.description}
                </p>
              )}
              
              <div className="flex items-center justify-between">
                {business.website && (
                  <a 
                    href={business.website}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-xs text-blue-600 hover:text-blue-800"
                  >
                    Visit Website →
                  </a>
                )}
                
                {business.phone && (
                  <a 
                    href={`tel:${business.phone}`}
                    className="text-xs text-green-600 hover:text-green-800"
                  >
                    📞 Call
                  </a>
                )}
              </div>
              
              {business.address && (
                <div className="mt-2 text-xs text-gray-500 line-clamp-1">
                  {business.address}
                </div>
              )}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}