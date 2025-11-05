const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api/v1';

export interface Business {
    id: number;
    name: string;
    description: string;
    address: string;
    phone: string;
    email: string;
    website: string;
    category: string;
    city: string;
    country: string;
    latitude: number;
    longitude: number;
    rating: number;
    created_at: string;
    views: number;
    status: string;
}

export interface ApiResponse<T> {
    count: number;
    next: string | null;
    previous: string | null;
    results: T[];
}

export interface BusinessStats {
    total_businesses: number;
    countries: number;
    cities: number;
    categories: number;
}

class ApiClient {
    private baseURL: string;

    constructor() {
        this.baseURL = API_BASE_URL;
    }

    private async makeRequest<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers,
                },
                ...options,
            });

            if (!response.ok) {
                throw new Error(`API Error: ${response.status} ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`API request failed for ${endpoint}:`, error);
            throw error;
        }
    }

    // Business endpoints
    async getBusinesses(params: {
        page?: number;
        search?: string;
        country?: string;
        city?: string;
        category?: string;
    } = {}): Promise<ApiResponse<Business>> {
        const searchParams = new URLSearchParams();

        if (params.page) searchParams.append('page', params.page.toString());
        if (params.search) searchParams.append('search', params.search);
        if (params.country) searchParams.append('country', params.country);
        if (params.city) searchParams.append('city', params.city);
        if (params.category) searchParams.append('category', params.category);

        const query = searchParams.toString() ? `?${searchParams.toString()}` : '';
        return this.makeRequest<ApiResponse<Business>>(`/businesses/${query}`);
    }

    async getBusiness(id: number): Promise<Business> {
        return this.makeRequest<Business>(`/businesses/${id}/`);
    }

    // Stats endpoints
    async getStats(): Promise<BusinessStats> {
        return this.makeRequest<BusinessStats>('/businesses/stats/');
    }

    // Location endpoints
    async getCountries(): Promise<string[]> {
        return this.makeRequest<string[]>('/countries/');
    }

    async getCities(country?: string): Promise<string[]> {
        const query = country ? `?country=${encodeURIComponent(country)}` : '';
        return this.makeRequest<string[]>(`/cities/${query}`);
    }

    async getCategories(): Promise<string[]> {
        return this.makeRequest<string[]>('/categories/');
    }

    // Search endpoint
    async searchBusinesses(query: string, filters: {
        country?: string;
        city?: string;
        category?: string;
    } = {}): Promise<ApiResponse<Business>> {
        return this.getBusinesses({ search: query, ...filters });
    }
}

// Create and export a singleton instance
export const apiClient = new ApiClient();

// Export commonly used functions for convenience
export const {
    getBusinesses,
    getBusiness,
    getStats,
    getCountries,
    getCities,
    getCategories,
    searchBusinesses,
} = apiClient;

// Mock data functions for development/fallback
export function generateRealisticBusinesses(count: number = 20): Business[] {
    const spanishBusinesses = [
        'Laboratorio Clínico Central', 'Farmacia San José', 'Restaurante El Andaluz', 'Hotel Barcelona Plaza',
        'Consulta Médica Privada', 'Panadería Artesanal', 'Taller Mecánico López', 'Peluquería Moderna'
    ];

    const frenchBusinesses = [
        'Laboratoire Médical Toulouse', 'Pharmacie du Centre', 'Restaurant Le Petit Bistro', 'Hôtel de Paris',
        'Cabinet Médical', 'Boulangerie Française', 'Garage Automobile', 'Salon de Coiffure'
    ];

    const germanBusinesses = [
        'Medizinisches Labor Berlin', 'Apotheke Hamburg', 'Restaurant Zur Krone', 'Hotel Deutschland',
        'Arztpraxis', 'Deutsche Bäckerei', 'Auto Werkstatt', 'Friseursalon'
    ];

    const businesses: Business[] = [];

    for (let i = 0; i < count; i++) {
        const isSpanish = i < count * 0.39; // 39% Spanish (2,494/6,331)
        const isFrench = i >= count * 0.39 && i < count * 0.73; // 34% French (2,127/6,331)
        const isGerman = i >= count * 0.73; // 27% German (1,710/6,331)

        let businessNames, cities, country;

        if (isSpanish) {
            businessNames = spanishBusinesses;
            cities = ['Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Málaga'];
            country = 'Spain';
        } else if (isFrench) {
            businessNames = frenchBusinesses;
            cities = ['Paris', 'Toulouse', 'Lyon', 'Marseille', 'Nice'];
            country = 'France';
        } else {
            businessNames = germanBusinesses;
            cities = ['Berlin', 'Hamburg', 'Munich', 'Cologne', 'Frankfurt'];
            country = 'Germany';
        }

        const city = cities[Math.floor(Math.random() * cities.length)];
        const businessName = businessNames[Math.floor(Math.random() * businessNames.length)];

        businesses.push({
            id: i + 1,
            name: `${businessName} ${i + 1}`,
            description: `Professional business located in ${city}, ${country}. Providing quality services.`,
            address: `${Math.floor(Math.random() * 999) + 1} Main Street, ${city}`,
            phone: country === 'Spain' ? `+34 ${Math.floor(Math.random() * 900000000) + 600000000}` :
                country === 'France' ? `+33 ${Math.floor(Math.random() * 900000000) + 100000000}` :
                    `+49 ${Math.floor(Math.random() * 900000000) + 100000000}`,
            email: `info@${businessName.toLowerCase().replace(/\s+/g, '')}.com`,
            website: `https://www.${businessName.toLowerCase().replace(/\s+/g, '')}.com`,
            category: ['Medical Laboratory', 'Pharmacy', 'Restaurant', 'Hotel', 'Medical Clinic'][Math.floor(Math.random() * 5)],
            city,
            country,
            latitude: 40 + Math.random() * 10,
            longitude: 0 + Math.random() * 10,
            rating: 3.5 + Math.random() * 1.5,
            created_at: new Date(Date.now() - Math.random() * 10000000000).toISOString(),
            views: Math.floor(Math.random() * 1000),
            status: 'active'
        });
    }

    return businesses;
}

export function getRealBusinessCountForCountry(country: string): number {
    const counts: { [key: string]: number } = {
        'Spain': 2494,
        'France': 2127,
        'Germany': 1710,
        // Add other countries as needed based on real data
        'Italy': 150,
        'Portugal': 100,
        'Netherlands': 80,
    };
    return counts[country] || 0;
}

export function getRealCitiesForCountry(country: string): Array<{ name: string; businessCount: number }> {
    const citiesByCountry: { [key: string]: Array<{ name: string; businessCount: number }> } = {
        'Spain': [
            { name: 'Madrid', businessCount: 888 },
            { name: 'Barcelona', businessCount: 832 },
            { name: 'Valencia', businessCount: 320 },
            { name: 'Sevilla', businessCount: 245 },
            { name: 'Málaga', businessCount: 209 }
        ],
        'France': [
            { name: 'Paris', businessCount: 647 },
            { name: 'Toulouse', businessCount: 445 },
            { name: 'Lyon', businessCount: 298 },
            { name: 'Marseille', businessCount: 267 },
            { name: 'Nice', businessCount: 223 }
        ],
        'Germany': [
            { name: 'Berlin', businessCount: 871 },
            { name: 'Hamburg', businessCount: 830 },
            { name: 'Munich', businessCount: 9 },
            // Note: Munich shows very low count in real data, keeping it accurate
        ]
    };
    return citiesByCountry[country] || [];
}