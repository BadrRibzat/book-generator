import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { User, UserLogin, UserRegistration } from '../types';
import apiClient from '../services/api';

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null);
  const userProfile = ref<any | null>(null);
  const initialized = ref(false);
  const loading = ref(false);
  const error = ref<string | null>(null);

  // Getters
  const isAuthenticated = computed(() => user.value !== null);
  const currentUser = computed(() => user.value);

  // Actions
  async function checkAuth() {
    try {
      loading.value = true;
      error.value = null;
      const response = await apiClient.get<User>('/users/profile/');
      user.value = response.data;
      
      // Also fetch user profile data
      await fetchUserProfile();
    } catch (err: any) {
      // Not authenticated or network error
      user.value = null;
      userProfile.value = null;
      if (err.response?.status === 403) {
        // User needs to sign in
        console.log('User not authenticated - please sign in');
      } else if (err.response?.status !== 401) {
        console.error('Auth check failed:', err);
      }
    } finally {
      initialized.value = true;
      loading.value = false;
    }
  }

  async function fetchUserProfile() {
    try {
      const response = await apiClient.get('/users/profiles/');
      if (response.data && response.data.length > 0) {
        userProfile.value = response.data[0]; // Get first profile (current user)
      }
    } catch (err: any) {
      console.error('Failed to fetch user profile:', err);
      userProfile.value = null;
    }
  }

  async function signUp(credentials: UserRegistration) {
    try {
      loading.value = true;
      error.value = null;
      
      // Add password2 field for backend validation
      const registerData = {
        username: credentials.username,
        email: credentials.email,
        password: credentials.password,
        password2: credentials.password // Backend expects confirmation
      };
      
      await apiClient.post<any>('/users/auth/register/', registerData);
      // Don't set user.value here - user must sign in after registration
      return { success: true };
    } catch (err: any) {
      let message = 'Sign up failed';
      if (err.response?.data) {
        // Handle Django validation errors
        const errors = err.response.data;
        if (typeof errors === 'object') {
          const errorMessages = [];
          for (const [field, fieldErrors] of Object.entries(errors)) {
            if (Array.isArray(fieldErrors)) {
              errorMessages.push(`${field}: ${fieldErrors.join(', ')}`);
            } else {
              errorMessages.push(`${field}: ${fieldErrors}`);
            }
          }
          message = errorMessages.join('; ');
        } else if (errors.error) {
          message = errors.error;
        } else if (errors.detail) {
          message = errors.detail;
        }
      }
      error.value = message;
      console.error('Registration error:', err.response?.data);
      return { success: false, error: message };
    } finally {
      loading.value = false;
    }
  }

  async function signIn(credentials: UserLogin) {
    try {
      loading.value = true;
      error.value = null;
      
      const response = await apiClient.post<any>('/users/auth/login/', credentials);
      
      // Store user data from login response
      if (response.data.user) {
        user.value = response.data.user;
      }
      
      // Double-check by fetching current user to ensure session is working
      await checkAuth();
      
      return { success: true };
    } catch (err: any) {
      let message = 'Sign in failed';
      if (err.response?.data?.error) {
        message = err.response.data.error;
      } else if (err.response?.data?.detail) {
        message = err.response.data.detail;
      } else if (err.response?.data) {
        // Handle validation errors
        const errors = err.response.data;
        if (typeof errors === 'object') {
          const errorMessages = [];
          for (const [, fieldErrors] of Object.entries(errors)) {
            if (Array.isArray(fieldErrors)) {
              errorMessages.push(fieldErrors.join(', '));
            } else {
              errorMessages.push(String(fieldErrors));
            }
          }
          message = errorMessages.join('; ');
        }
      }
      error.value = message;
      console.error('Login error:', err.response?.data);
      return { success: false, error: message };
    } finally {
      loading.value = false;
    }
  }

  async function signOut() {
    try {
      loading.value = true;
      error.value = null;
      await apiClient.post('/users/auth/logout/');
      user.value = null;
      return { success: true };
    } catch (err: any) {
      // Even if logout fails, clear local state
      user.value = null;
      console.warn('Logout request failed, but cleared local state:', err);
      return { success: true };
    } finally {
      loading.value = false;
    }
  }

  function clearError() {
    error.value = null;
  }

  return {
    // State
    user,
    userProfile,
    initialized,
    loading,
    error,
    // Getters
    isAuthenticated,
    currentUser,
    // Actions
    checkAuth,
    fetchUserProfile,
    signUp,
    signIn,
    signOut,
    clearError,
  };
});
