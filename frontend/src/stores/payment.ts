import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import apiClient from '../services/api';

export interface SubscriptionPlan {
  id: number;
  name: string;
  plan_type: string;
  stripe_price_id: string;
  price: number;
  currency: string;
  interval: 'month' | 'year';
  max_books_per_month: number;
  max_pages_per_book: number;
  priority_support: boolean;
  custom_covers: boolean;
  api_access: boolean;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Subscription {
  id: number;
  user: number;
  plan: SubscriptionPlan;
  stripe_subscription_id: string;
  status: 'active' | 'canceled' | 'past_due' | 'incomplete';
  current_period_start: string;
  current_period_end: string;
  cancel_at_period_end: boolean;
  created_at: string;
  updated_at: string;
}

export interface Payment {
  id: number;
  user: number;
  stripe_payment_intent_id: string;
  amount: number;
  currency: string;
  status: 'succeeded' | 'pending' | 'failed';
  created_at: string;
  description?: string;
}

export const usePaymentStore = defineStore('payment', () => {
  // State
  const subscriptionPlans = ref<SubscriptionPlan[]>([]);
  const currentSubscription = ref<Subscription | null>(null);
  const paymentHistory = ref<Payment[]>([]);
  const stripePublishableKey = ref<string>('');
  const loading = ref(false);
  const error = ref<string | null>(null);

  // Getters
  const isSubscribed = computed(() => {
    return currentSubscription.value?.status === 'active';
  });

  const currentPlan = computed(() => {
    return currentSubscription.value?.plan || null;
  });

  const canCreateBook = computed(() => {
    // Free tier: 2 books/month
    // Parents: 8 books/month
    // Creators: 12 books/month
    if (!currentSubscription.value) return true; // Free tier
    return true; // For now, allow creation - backend will handle limits
  });

  // Actions
  async function fetchSubscriptionPlans() {
    try {
      loading.value = true;
      error.value = null;
      const response = await apiClient.get('/payments/plans/');
      subscriptionPlans.value = response.data;
    } catch (err: any) {
      console.error('Failed to fetch subscription plans:', err);
      error.value = 'Failed to load subscription plans';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function fetchCurrentSubscription() {
    try {
      loading.value = true;
      error.value = null;
      const response = await apiClient.get('/payments/subscription/');
      currentSubscription.value = response.data;
    } catch (err: any) {
      if (err.response?.status === 404) {
        // No subscription found
        currentSubscription.value = null;
      } else {
        console.error('Failed to fetch current subscription:', err);
        error.value = 'Failed to load subscription';
        throw err;
      }
    } finally {
      loading.value = false;
    }
  }

  async function fetchPaymentHistory() {
    try {
      loading.value = true;
      error.value = null;
      const response = await apiClient.get('/payments/payments/');
      paymentHistory.value = response.data;
    } catch (err: any) {
      console.error('Failed to fetch payment history:', err);
      error.value = 'Failed to load payment history';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function fetchStripeConfig() {
    try {
      const response = await apiClient.get('/payments/config/');
      stripePublishableKey.value = response.data.publishableKey;
    } catch (err: any) {
      console.error('Failed to fetch Stripe config:', err);
      throw err;
    }
  }

  async function createSubscription(planId: number, paymentMethodId?: string) {
    try {
      loading.value = true;
      error.value = null;

      const data: any = { plan_id: planId };
      if (paymentMethodId) {
        data.payment_method_id = paymentMethodId;
      }

      const response = await apiClient.post('/payments/subscription/create/', data);

      // Update current subscription
      await fetchCurrentSubscription();

      return response.data;
    } catch (err: any) {
      console.error('Failed to create subscription:', err);
      error.value = 'Failed to create subscription';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function cancelSubscription() {
    try {
      loading.value = true;
      error.value = null;

      await apiClient.post('/payments/subscription/cancel/');

      // Update current subscription
      await fetchCurrentSubscription();

      if (typeof window !== 'undefined' && (window as any).$toast) {
        (window as any).$toast.success('Subscription Canceled', 'Your subscription will remain active until the end of the billing period');
      }
    } catch (err: any) {
      console.error('Failed to cancel subscription:', err);
      error.value = 'Failed to cancel subscription';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function reactivateSubscription() {
    try {
      loading.value = true;
      error.value = null;

      await apiClient.post('/payments/subscription/reactivate/');

      // Update current subscription
      await fetchCurrentSubscription();

      if (typeof window !== 'undefined' && (window as any).$toast) {
        (window as any).$toast.success('Subscription Reactivated', 'Your subscription has been reactivated');
      }
    } catch (err: any) {
      console.error('Failed to reactivate subscription:', err);
      error.value = 'Failed to reactivate subscription';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function updateSubscription(planId: number) {
    try {
      loading.value = true;
      error.value = null;

      await apiClient.post('/payments/subscription/update/', { plan_id: planId });

      // Update current subscription
      await fetchCurrentSubscription();

      if (typeof window !== 'undefined' && (window as any).$toast) {
        (window as any).$toast.success('Subscription Updated', 'Your subscription plan has been updated');
      }
    } catch (err: any) {
      console.error('Failed to update subscription:', err);
      error.value = 'Failed to update subscription';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  function clearError() {
    error.value = null;
  }

  return {
    // State
    subscriptionPlans,
    currentSubscription,
    paymentHistory,
    stripePublishableKey,
    loading,
    error,

    // Getters
    isSubscribed,
    currentPlan,
    canCreateBook,

    // Actions
    fetchSubscriptionPlans,
    fetchCurrentSubscription,
    fetchPaymentHistory,
    fetchStripeConfig,
    createSubscription,
    cancelSubscription,
    reactivateSubscription,
    updateSubscription,
    clearError,
  };
});