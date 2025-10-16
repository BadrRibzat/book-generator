import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { User, UserLogin, UserRegistration } from '../types';
import apiClient from '../services/api';

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null);
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
      const response = await apiClient.get<User>('/users/me/');
      user.value = response.data;
    } catch (err: any) {
      // Not authenticated or network error
      user.value = null;
      if (err.response?.status !== 401) {
        console.error('Auth check failed:', err);
      }
    } finally {
      initialized.value = true;
      loading.value = false;
    }
  }

  async function signUp(credentials: UserRegistration) {
    try {
      loading.value = true;
      error.value = null;
      const response = await apiClient.post<User>('/users/register/', credentials);
      user.value = response.data;
      return { success: true };
    } catch (err: any) {
      const message = err.response?.data?.error || 'Sign up failed';
      error.value = message;
      return { success: false, error: message };
    } finally {
      loading.value = false;
    }
  }

  async function signIn(credentials: UserLogin) {
    try {
      loading.value = true;
      error.value = null;
      const response = await apiClient.post<User>('/users/login/', credentials);
      user.value = response.data;
      return { success: true };
    } catch (err: any) {
      const message = err.response?.data?.error || 'Sign in failed';
      error.value = message;
      return { success: false, error: message };
    } finally {
      loading.value = false;
    }
  }

  async function signOut() {
    try {
      loading.value = true;
      error.value = null;
      await apiClient.post('/users/logout/');
      user.value = null;
      return { success: true };
    } catch (err: any) {
      const message = err.response?.data?.error || 'Sign out failed';
      error.value = message;
      return { success: false, error: message };
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
    initialized,
    loading,
    error,
    // Getters
    isAuthenticated,
    currentUser,
    // Actions
    checkAuth,
    signUp,
    signIn,
    signOut,
    clearError,
  };
});
