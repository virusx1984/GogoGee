// API Configuration
const API_CONFIG = {
    BASE_URL: 'http://127.0.0.1:5000/api',
    ENDPOINTS: {
        AUTH: {
            LOGIN: '/auth/login',
            USER: '/auth/user',
            LOGOUT: '/auth/logout'
        },
        MENUS: '/menus/',
        CONTENT: '' // Will be appended with the route
    }
};

// API Service
const ApiService = {
    getUrl: function(endpoint) {
        return API_CONFIG.BASE_URL + endpoint;
    },

    // Generic request method
    request: function(endpoint, options = {}) {
        const token = localStorage.getItem('authToken');
        
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token ? `Bearer ${token}` : undefined
            },
            crossDomain: true,
            xhrFields: {
                withCredentials: false
            }
        };

        return $.ajax({
            url: this.getUrl(endpoint),
            ...defaultOptions,
            ...options
        });
    },

    // Common API methods
    get: function(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    },

    post: function(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            data: JSON.stringify(data)
        });
    },

    put: function(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            data: JSON.stringify(data)
        });
    },

    delete: function(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }
}; 