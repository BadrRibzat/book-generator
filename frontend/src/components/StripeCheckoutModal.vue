<template>
  <div class="stripe-checkout-modal">
    <div class="modal-overlay" @click="$emit('close')">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white">
            Subscribe to {{ plan.name }}
          </h2>
          <button
            @click="$emit('close')"
            class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
          >
            <font-awesome-icon :icon="['fas', 'times']" />
          </button>
        </div>

        <div class="modal-body">
          <!-- Plan Summary -->
          <div class="plan-summary mb-6">
            <div class="flex items-center justify-between mb-4">
              <span class="text-lg font-semibold text-gray-900 dark:text-white">
                {{ plan.name }}
              </span>
              <span class="text-2xl font-bold text-primary-600">
                ${{ plan.price }}/{{ plan.interval }}
              </span>
            </div>
                          <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3 flex-shrink-0" />
                <span class="text-gray-700 dark:text-gray-300 text-sm">Up to {{ plan.max_pages_per_book }} pages per book</span>
              </li>
              <li v-if="plan.priority_support" class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3 flex-shrink-0" />
                <span class="text-gray-700 dark:text-gray-300 text-sm">Priority support</span>
              </li>
              <li v-if="plan.custom_covers" class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3 flex-shrink-0" />
                <span class="text-gray-700 dark:text-gray-300 text-sm">Custom covers</span>
              </li>
              <li v-if="plan.api_access" class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3 flex-shrink-0" />
                <span class="text-gray-700 dark:text-gray-300 text-sm">API access</span>
              </li>
          </div>

          <!-- Payment Form -->
          <form @submit.prevent="handleSubmit" class="space-y-6">
            <!-- Card Element -->
            <div class="form-group">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Card Information
              </label>
              <div
                ref="cardElementRef"
                class="stripe-card-element"
                :class="{ 'error': cardError }"
              ></div>
              <p v-if="cardError" class="mt-1 text-sm text-red-600">
                {{ cardError }}
              </p>
            </div>

            <!-- Billing Details -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="form-group">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Full Name
                </label>
                <input
                  v-model="billingDetails.name"
                  type="text"
                  required
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
                  placeholder="John Doe"
                />
              </div>
              <div class="form-group">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Email
                </label>
                <input
                  v-model="billingDetails.email"
                  type="email"
                  required
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
                  placeholder="john@example.com"
                />
              </div>
            </div>

            <!-- Error Message -->
            <div v-if="error" class="text-red-600 text-sm bg-red-50 dark:bg-red-900/20 p-3 rounded-md">
              {{ error }}
            </div>

            <!-- Submit Button -->
            <button
              type="submit"
              :disabled="loading || !stripe"
              class="w-full flex justify-center items-center px-4 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <font-awesome-icon
                v-if="loading"
                :icon="['fas', 'spinner']"
                class="animate-spin mr-2"
              />
              {{ loading ? 'Processing...' : `Subscribe for $${plan.price}/${plan.interval}` }}
            </button>
          </form>

          <!-- Security Notice -->
          <div class="mt-6 text-center text-xs text-gray-500 dark:text-gray-400">
            <font-awesome-icon :icon="['fas', 'lock']" class="mr-1" />
            Your payment information is secure and encrypted
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue';
import { usePaymentStore } from '../stores/payment';
import { getStripe, createSubscription } from '../services/stripe';
import type { SubscriptionPlan } from '../stores/payment';

// Props
interface Props {
  plan: SubscriptionPlan;
}

const props = defineProps<Props>();

// Emits
const emit = defineEmits<{
  close: [];
  success: [subscription: any];
}>();

// State
const paymentStore = usePaymentStore();
const cardElementRef = ref<HTMLDivElement>();
const stripe = ref<any>(null);
const cardElement = ref<any>(null);
const loading = ref(false);
const error = ref<string>('');
const cardError = ref<string>('');

const billingDetails = ref({
  name: '',
  email: '',
});

// Initialize Stripe
onMounted(async () => {
  try {
    // Get Stripe publishable key
    await paymentStore.fetchStripeConfig();

    // Initialize Stripe
    const stripeInstance = await getStripe(paymentStore.stripePublishableKey);
    if (!stripeInstance) {
      throw new Error('Failed to initialize Stripe');
    }

    stripe.value = stripeInstance;

    // Create card element
    await nextTick();
    if (cardElementRef.value) {
      const elements = stripeInstance.elements();
      cardElement.value = elements.create('card', {
        style: {
          base: {
            fontSize: '16px',
            color: '#424770',
            '::placeholder': {
              color: '#aab7c4',
            },
          },
        },
      });

      cardElement.value.mount(cardElementRef.value);

      // Handle card element events
      cardElement.value.on('change', (event: any) => {
        if (event.error) {
          cardError.value = event.error.message;
        } else {
          cardError.value = '';
        }
      });
    }
  } catch (err: any) {
    console.error('Failed to initialize Stripe:', err);
    error.value = 'Failed to initialize payment system';
  }
});

// Cleanup
onUnmounted(() => {
  if (cardElement.value) {
    cardElement.value.destroy();
  }
});

// Handle form submission
const handleSubmit = async () => {
  if (!stripe.value || !cardElement.value) {
    error.value = 'Payment system not initialized';
    return;
  }

  if (!billingDetails.value.name || !billingDetails.value.email) {
    error.value = 'Please fill in all billing details';
    return;
  }

  try {
    loading.value = true;
    error.value = '';
    cardError.value = '';

    // Create subscription
    const result = await createSubscription(
      stripe.value,
      props.plan.stripe_price_id,
      cardElement.value,
      billingDetails.value
    );

    // Success
    emit('success', result.subscription);

    // Show success message
    if (typeof window !== 'undefined' && (window as any).$toast) {
      (window as any).$toast.success(
        'Subscription Created!',
        `Welcome to the ${props.plan.name} plan`
      );
    }

    emit('close');
  } catch (err: any) {
    console.error('Subscription creation failed:', err);
    error.value = err.message || 'Failed to create subscription';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.stripe-checkout-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.modal-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
}

.modal-content {
  position: relative;
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.dark .modal-content {
  background: #1f2937;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.dark .modal-header {
  border-bottom-color: #374151;
}

.modal-body {
  padding: 1.5rem;
}

.stripe-card-element {
  padding: 12px 16px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: white;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.stripe-card-element:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.dark .stripe-card-element {
  background: #374151;
  border-color: #4b5563;
}

.stripe-card-element.error {
  border-color: #ef4444;
}

.dark .stripe-card-element.error {
  border-color: #dc2626;
}

.form-group {
  margin-bottom: 1rem;
}
</style>