import axios from 'axios';

// API Base URL - use proxy in development, can be overridden with VITE_API_BASE_URL env var
// In development: requests to /api will be proxied to http://127.0.0.1:8000/api by Vite
// In production: set VITE_API_BASE_URL to your actual API URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true, // Important for session-based auth - sends cookies
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
  },
  // Extended timeout for long-running operations like book generation
  timeout: 1200000, // 20 minutes (1200000ms) to handle 30+ page books
});

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle common errors with user-friendly messages
    let errorMessage = 'An unexpected error occurred';
    let errorTitle = 'Error';

    if (error.response?.status === 401) {
      errorTitle = 'Authentication Required';
      errorMessage = 'Please sign in to continue';
    } else if (error.response?.status === 403) {
      errorTitle = 'Access Denied';
      errorMessage = 'You don\'t have permission to perform this action';
    } else if (error.response?.status === 404) {
      errorTitle = 'Not Found';
      errorMessage = 'The requested resource was not found';
    } else if (error.response?.status === 429) {
      errorTitle = 'Too Many Requests';
      errorMessage = 'Please wait a moment before trying again';
    } else if (error.response?.status === 500) {
      errorTitle = 'Server Error';
      errorMessage = 'Something went wrong on our end. Please try again later';
    } else if (error.response?.status >= 400 && error.response?.status < 500) {
      errorTitle = 'Request Error';
      // Try to get detailed error from response
      if (error.response.data?.error) {
        errorMessage = error.response.data.error;
      } else if (error.response.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error.response.data?.message) {
        errorMessage = error.response.data.message;
      }
    }

    // Show toast notification for errors (but not for auth checks)
    if (typeof window !== 'undefined' && (window as any).$toast && error.response?.status !== 401) {
      (window as any).$toast.error(errorTitle, errorMessage);
    }

    return Promise.reject(error);
  }
);

// API Helper Methods
export const api = {
  // Domain & Niche endpoints
  getDomains() {
    return apiClient.get('/domains/');
  },
  
  getNiches(domainId?: string | number) {
    const params = domainId ? { domain: domainId } : {};
    return apiClient.get('/niches/', { params });
  },
  
  getCoverStyles() {
    return apiClient.get('/cover-styles/');
  },
  
  // Book creation
  createGuidedBook(bookData: any) {
    return apiClient.post('/books/create-guided/', bookData);
  },
  
  // Books endpoints
  getBooks() {
    return apiClient.get('/books/');
  },
  
  getBook(bookId: string | number) {
    return apiClient.get(`/books/${bookId}/`);
  },
  
  getBookStatus(bookId: string | number) {
    return apiClient.get(`/books/${bookId}/status/`);
  },
  
  selectCover(bookId: string | number, coverId: string | number) {
    return apiClient.post(`/books/${bookId}/select-cover/`, { cover_id: coverId });
  },
  
  downloadBook(bookId: string | number) {
    return apiClient.get(`/books/${bookId}/download/`, { responseType: 'blob' });
  },
  
  // Auth endpoints
  register(userData: any) {
    return apiClient.post('/auth/register/', userData);
  },
  
  login(credentials: any) {
    return apiClient.post('/auth/login/', credentials);
  },
  
  logout() {
    return apiClient.post('/auth/logout/');
  },
  
  getCurrentUser() {
    return apiClient.get('/auth/user/');
  }
};

export default apiClient;
export { API_BASE_URL };
