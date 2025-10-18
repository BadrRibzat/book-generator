import axios from 'axios';

// API Base URL - use proxy in development, can be overridden with VITE_API_BASE_URL env var
// In development: requests to /api will be proxied to http://127.0.0.1:8000/api by Vite
// In production: set VITE_API_BASE_URL to your actual API URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true, // Important for session-based auth - sends cookies
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  // Add timeout to avoid hanging requests
  timeout: 30000,
});

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle common errors
    if (error.response?.status === 401) {
      // Unauthorized - redirect to login
      console.log('Unauthorized - please login');
    } else if (error.response?.status === 403) {
      // Forbidden - user not authenticated
      console.log('Access forbidden - user not authenticated');
    } else if (error.response?.status === 500) {
      // Server error
      console.error('Server error');
    }
    return Promise.reject(error);
  }
);

export default apiClient;
export { API_BASE_URL };
