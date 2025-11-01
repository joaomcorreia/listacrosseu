const API_BASE_URL = 'http://127.0.0.1:8000/api';

class ApiClient {
    private getHeaders(): HeadersInit {
        const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
        return {
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` }),
        };
    }

    private async handleResponse(response: Response) {
        if (!response.ok) {
            if (response.status === 401) {
                // Handle unauthorized - redirect to login
                if (typeof window !== 'undefined') {
                    localStorage.removeItem('token');
                    localStorage.removeItem('refresh_token');
                    window.location.href = '/auth/login';
                }
            }
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    }

    // Business endpoints
    async getBusinesses(params?: {
        page?: number;
        page_size?: number;
        search?: string;
        country?: string;
        city?: string;
        category?: string;
    }) {
        const queryParams = new URLSearchParams();
        if (params) {
            Object.entries(params).forEach(([key, value]) => {
                if (value !== undefined && value !== '') {
                    queryParams.append(key, value.toString());
                }
            });
        }

        const url = `${API_BASE_URL}/businesses/?${queryParams.toString()}`;
        const response = await fetch(url, {
            headers: this.getHeaders(),
        });
        return this.handleResponse(response);
    }

    async getBusiness(id: number) {
        const response = await fetch(`${API_BASE_URL}/businesses/${id}/`, {
            headers: this.getHeaders(),
        });
        return this.handleResponse(response);
    }

    async createBusiness(businessData: any) {
        const response = await fetch(`${API_BASE_URL}/businesses/`, {
            method: 'POST',
            headers: this.getHeaders(),
            body: JSON.stringify(businessData),
        });
        return this.handleResponse(response);
    }

    async updateBusiness(id: number, businessData: any) {
        const response = await fetch(`${API_BASE_URL}/businesses/${id}/`, {
            method: 'PATCH',
            headers: this.getHeaders(),
            body: JSON.stringify(businessData),
        });
        return this.handleResponse(response);
    }

    async deleteBusiness(id: number) {
        const response = await fetch(`${API_BASE_URL}/businesses/${id}/`, {
            method: 'DELETE',
            headers: this.getHeaders(),
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.status === 204;
    }

    // Stats endpoints
    async getBusinessStats() {
        const response = await fetch(`${API_BASE_URL}/businesses/stats/`, {
            headers: this.getHeaders(),
        });
        return this.handleResponse(response);
    }

    // Categories and filters
    async getCategories() {
        const response = await fetch(`${API_BASE_URL}/businesses/categories/`, {
            headers: this.getHeaders(),
        });
        return this.handleResponse(response);
    }

    async getCountries() {
        const response = await fetch(`${API_BASE_URL}/businesses/countries/`, {
            headers: this.getHeaders(),
        });
        return this.handleResponse(response);
    }

    async getCities(country?: string) {
        const url = country
            ? `${API_BASE_URL}/businesses/cities/?country=${encodeURIComponent(country)}`
            : `${API_BASE_URL}/businesses/cities/`;

        const response = await fetch(url, {
            headers: this.getHeaders(),
        });
        return this.handleResponse(response);
    }

    // Authentication endpoints
    async login(username: string, password: string) {
        const response = await fetch(`${API_BASE_URL}/auth/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });
        return this.handleResponse(response);
    }

    async register(userData: {
        username: string;
        email: string;
        password: string;
        first_name?: string;
        last_name?: string;
    }) {
        const response = await fetch(`${API_BASE_URL}/auth/register/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData),
        });
        return this.handleResponse(response);
    }

    async refreshToken() {
        const refreshToken = typeof window !== 'undefined'
            ? localStorage.getItem('refresh_token')
            : null;

        if (!refreshToken) {
            throw new Error('No refresh token available');
        }

        const response = await fetch(`${API_BASE_URL}/auth/refresh/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ refresh: refreshToken }),
        });
        return this.handleResponse(response);
    }

    // User profile
    async getProfile() {
        const response = await fetch(`${API_BASE_URL}/auth/profile/`, {
            headers: this.getHeaders(),
        });
        return this.handleResponse(response);
    }

    async updateProfile(profileData: any) {
        const response = await fetch(`${API_BASE_URL}/auth/profile/`, {
            method: 'PATCH',
            headers: this.getHeaders(),
            body: JSON.stringify(profileData),
        });
        return this.handleResponse(response);
    }
}

// Create a singleton instance
const apiClient = new ApiClient();

export default apiClient;