<template>
  <Layout>
    <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <!-- Page Header -->
        <div class="mb-8 animate-fade-in">
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
            Welcome back, {{ authStore.currentUser?.username }}!
          </h1>
          <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
            Manage your books and create amazing content
          </p>
        </div>

        <div class="bg-white dark:bg-gray-800 shadow-xl rounded-2xl overflow-hidden border border-gray-200 dark:border-gray-700">
          <!-- Tab Navigation -->
          <div class="border-b border-gray-200 dark:border-gray-700">
            <nav class="flex">
              <router-link
                to="/profile"
                class="flex-1 py-4 px-6 text-center border-b-2 font-medium text-sm transition-colors"
                :class="currentTab === 'dashboard' ? 'border-primary-500 text-primary-600 dark:text-primary-400' : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'"
              >
                <font-awesome-icon :icon="['fas', 'tachometer-alt']" class="mr-2" />
                Dashboard
              </router-link>
              
              <router-link
                to="/profile/mybooks"
                class="flex-1 py-4 px-6 text-center border-b-2 font-medium text-sm transition-colors"
                :class="currentTab === 'mybooks' ? 'border-primary-500 text-primary-600 dark:text-primary-400' : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'"
              >
                <font-awesome-icon :icon="['fas', 'book']" class="mr-2" />
                My Books
              </router-link>
              
              <router-link
                to="/profile/subscription"
                class="flex-1 py-4 px-6 text-center border-b-2 font-medium text-sm transition-colors"
                :class="currentTab === 'subscription' ? 'border-primary-500 text-primary-600 dark:text-primary-400' : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'"
              >
                <font-awesome-icon :icon="['fas', 'credit-card']" class="mr-2" />
                Subscription
              </router-link>
              
              <button
                @click="handleSignOut"
                class="flex-1 py-4 px-6 text-center border-b-2 font-medium text-sm text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300 transition-colors border-transparent"
              >
                <font-awesome-icon :icon="['fas', 'sign-out-alt']" class="mr-2" />
                Sign Out
              </button>
            </nav>
          </div>

          <!-- Tab Content -->
          <div class="p-6">
            <!-- Dashboard Tab -->
            <div v-if="currentTab === 'dashboard'" class="space-y-6">
              <!-- Welcome Header -->
              <div class="text-center">
                <h2 class="text-2xl font-bold text-gray-900 dark:text-white">
                  Welcome back, {{ authStore.currentUser?.username }}!
                </h2>
                <p class="mt-2 text-gray-600 dark:text-gray-400">
                  Here's an overview of your book creation activity
                </p>
              </div>

              <!-- Stats Cards -->
              <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="bg-gradient-to-r from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/20 rounded-xl p-6 shadow-lg border border-blue-200 dark:border-blue-800 transform hover:scale-105 transition-transform duration-200">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 bg-blue-500 rounded-lg p-3">
                      <font-awesome-icon :icon="['fas', 'book']" class="h-6 w-6 text-white" />
                    </div>
                    <div class="ml-4">
                      <p class="text-sm font-medium text-blue-800 dark:text-blue-200">Total Books</p>
                      <p class="text-2xl font-bold text-blue-900 dark:text-blue-100">{{ totalBooks }}</p>
                    </div>
                  </div>
                </div>

                <div class="bg-gradient-to-r from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/20 rounded-xl p-6 shadow-lg border border-green-200 dark:border-green-800 transform hover:scale-105 transition-transform duration-200">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 bg-green-500 rounded-lg p-3">
                      <font-awesome-icon :icon="['fas', 'check-circle']" class="h-6 w-6 text-white" />
                    </div>
                    <div class="ml-4">
                      <p class="text-sm font-medium text-green-800 dark:text-green-200">Completed</p>
                      <p class="text-2xl font-bold text-green-900 dark:text-green-100">{{ completedBooks }}</p>
                    </div>
                  </div>
                </div>

                <div class="bg-gradient-to-r from-yellow-50 to-yellow-100 dark:from-yellow-900/20 dark:to-yellow-800/20 rounded-xl p-6 shadow-lg border border-yellow-200 dark:border-yellow-800 transform hover:scale-105 transition-transform duration-200">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 bg-yellow-500 rounded-lg p-3">
                      <font-awesome-icon :icon="['fas', 'spinner']" class="h-6 w-6 text-white" />
                    </div>
                    <div class="ml-4">
                      <p class="text-sm font-medium text-yellow-800 dark:text-yellow-200">In Progress</p>
                      <p class="text-2xl font-bold text-yellow-900 dark:text-yellow-100">{{ inProgressBooks }}</p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Quick Actions -->
              <div class="bg-gradient-to-r from-primary-50 to-blue-50 dark:from-primary-900/20 dark:to-blue-900/20 rounded-xl p-6">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Quick Actions</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <router-link
                    to="/profile/create"
                    class="flex items-center p-4 bg-white dark:bg-gray-800 rounded-lg shadow hover:shadow-lg transition-shadow"
                  >
                    <div class="w-10 h-10 bg-primary-500 rounded-lg flex items-center justify-center mr-4">
                      <font-awesome-icon :icon="['fas', 'plus']" class="text-white" />
                    </div>
                    <div>
                      <h4 class="font-medium text-gray-900 dark:text-white">Create New Book</h4>
                      <p class="text-sm text-gray-600 dark:text-gray-400">Start the guided book creation process</p>
                    </div>
                  </router-link>
                  
                  <router-link
                    to="/profile/mybooks"
                    class="flex items-center p-4 bg-white dark:bg-gray-800 rounded-lg shadow hover:shadow-lg transition-shadow"
                  >
                    <div class="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center mr-4">
                      <font-awesome-icon :icon="['fas', 'list']" class="text-white" />
                    </div>
                    <div>
                      <h4 class="font-medium text-gray-900 dark:text-white">View All Books</h4>
                      <p class="text-sm text-gray-600 dark:text-gray-400">Manage your existing books</p>
                    </div>
                  </router-link>
                </div>
              </div>

              <!-- Recent Activity or Empty State -->
              <div v-if="totalBooks === 0" class="text-center py-8">
                <div class="inline-flex items-center justify-center h-16 w-16 rounded-full bg-primary-100 dark:bg-primary-900/30 mb-4">
                  <font-awesome-icon :icon="['fas', 'book-open']" class="h-8 w-8 text-primary-600 dark:text-primary-400" />
                </div>
                <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">No books yet</h3>
                <p class="text-gray-600 dark:text-gray-400 mb-4">Create your first book to get started!</p>
                <router-link
                  to="/profile/create"
                  class="inline-flex items-center px-6 py-3 border border-transparent text-sm font-medium rounded-lg text-white bg-gradient-to-r from-primary-600 to-blue-700 hover:from-primary-700 hover:to-blue-800"
                >
                  <font-awesome-icon :icon="['fas', 'magic']" class="mr-2" />
                  Create Your First Book
                </router-link>
              </div>
            </div>

            <!-- My Books Tab -->
            <div v-else-if="currentTab === 'mybooks'">
              <router-view />
            </div>

            <!-- Create Book Tab -->
            <div v-else-if="currentTab === 'create'">
              <router-view />
            </div>

            <!-- Subscription Tab -->
            <div v-else-if="currentTab === 'subscription'" class="space-y-6">
              <!-- Subscription Status Card -->
              <div class="bg-gradient-to-r from-primary-50 to-blue-50 dark:from-primary-900/20 dark:to-blue-900/20 rounded-xl p-6 border border-primary-200 dark:border-primary-800">
                <div class="flex items-center justify-between mb-4">
                  <h3 class="text-xl font-bold text-gray-900 dark:text-white">Current Plan</h3>
                  <span
                    class="px-3 py-1 rounded-full text-sm font-medium"
                    :class="paymentStore.isSubscribed ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'"
                  >
                    {{ paymentStore.isSubscribed ? 'Active' : 'Free Plan' }}
                  </span>
                </div>

                <div v-if="paymentStore.currentSubscription" class="space-y-4">
                  <div class="flex items-center justify-between">
                    <div>
                      <h4 class="text-lg font-semibold text-gray-900 dark:text-white">
                        {{ paymentStore.currentSubscription.plan.name }}
                      </h4>
                      <p class="text-gray-600 dark:text-gray-400">
                        ${{ paymentStore.currentSubscription.plan.price }}/{{ paymentStore.currentSubscription.plan.interval }}
                      </p>
                    </div>
                    <div class="text-right">
                      <p class="text-sm text-gray-600 dark:text-gray-400">Next billing</p>
                      <p class="font-medium text-gray-900 dark:text-white">
                        {{ formatDate(paymentStore.currentSubscription.current_period_end) }}
                      </p>
                    </div>
                  </div>

                  <!-- Plan Features -->
                  <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">
                    <div class="text-center">
                      <div class="text-2xl font-bold text-primary-600">{{ paymentStore.currentSubscription.plan.max_books_per_month }}</div>
                      <div class="text-sm text-gray-600 dark:text-gray-400">Books/month</div>
                    </div>
                    <div class="text-center">
                      <div class="text-2xl font-bold text-primary-600">{{ paymentStore.currentSubscription.plan.max_pages_per_book }}</div>
                      <div class="text-sm text-gray-600 dark:text-gray-400">Pages/book</div>
                    </div>
                    <div class="text-center">
                      <div class="text-2xl font-bold text-primary-600">
                        <font-awesome-icon v-if="paymentStore.currentSubscription.plan.priority_support" :icon="['fas', 'check']" class="text-green-500" />
                        <font-awesome-icon v-else :icon="['fas', 'times']" class="text-red-500" />
                      </div>
                      <div class="text-sm text-gray-600 dark:text-gray-400">Priority Support</div>
                    </div>
                    <div class="text-center">
                      <div class="text-2xl font-bold text-primary-600">
                        <font-awesome-icon v-if="paymentStore.currentSubscription.plan.custom_covers" :icon="['fas', 'check']" class="text-green-500" />
                        <font-awesome-icon v-else :icon="['fas', 'times']" class="text-red-500" />
                      </div>
                      <div class="text-sm text-gray-600 dark:text-gray-400">Custom Covers</div>
                    </div>
                  </div>
                </div>

                <div v-else class="text-center py-8">
                  <div class="inline-flex items-center justify-center h-16 w-16 rounded-full bg-gray-100 dark:bg-gray-700 mb-4">
                    <font-awesome-icon :icon="['fas', 'crown']" class="h-8 w-8 text-gray-400" />
                  </div>
                  <h4 class="text-lg font-medium text-gray-900 dark:text-white mb-2">Free Plan</h4>
                  <p class="text-gray-600 dark:text-gray-400 mb-4">Upgrade to unlock more features and create unlimited books!</p>
                  <router-link
                    to="/pricing"
                    class="inline-flex items-center px-6 py-3 border border-transparent text-sm font-medium rounded-lg text-white bg-gradient-to-r from-primary-600 to-blue-700 hover:from-primary-700 hover:to-blue-800"
                  >
                    <font-awesome-icon :icon="['fas', 'rocket']" class="mr-2" />
                    View Plans
                  </router-link>
                </div>
              </div>

              <!-- Usage Stats -->
              <div v-if="paymentStore.currentSubscription" class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-200 dark:border-gray-700">
                  <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Monthly Usage</h4>
                  <div class="space-y-4">
                    <div>
                      <div class="flex justify-between text-sm mb-1">
                        <span class="text-gray-600 dark:text-gray-400">Books Created</span>
                        <span class="font-medium">{{ monthlyBooksUsed }}/{{ paymentStore.currentSubscription.plan.max_books_per_month }}</span>
                      </div>
                      <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                        <div
                          class="bg-primary-600 h-2 rounded-full transition-all duration-300"
                          :style="{ width: `${Math.min((monthlyBooksUsed / paymentStore.currentSubscription.plan.max_books_per_month) * 100, 100)}%` }"
                        ></div>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-200 dark:border-gray-700">
                  <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Plan Actions</h4>
                  <div class="space-y-3">
                    <router-link
                      to="/pricing"
                      class="block w-full text-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
                    >
                      <font-awesome-icon :icon="['fas', 'arrow-up']" class="mr-2" />
                      Upgrade Plan
                    </router-link>

                    <button
                      v-if="!paymentStore.currentSubscription.cancel_at_period_end"
                      @click="showCancelModal = true"
                      class="block w-full text-center px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                    >
                      <font-awesome-icon :icon="['fas', 'times']" class="mr-2" />
                      Cancel Subscription
                    </button>

                    <button
                      v-else
                      @click="handleReactivateSubscription"
                      class="block w-full text-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                    >
                      <font-awesome-icon :icon="['fas', 'redo']" class="mr-2" />
                      Reactivate Subscription
                    </button>
                  </div>
                </div>
              </div>

              <!-- Cancellation Notice -->
              <div v-if="paymentStore.currentSubscription?.cancel_at_period_end" class="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-xl p-6">
                <div class="flex items-start">
                  <font-awesome-icon :icon="['fas', 'exclamation-triangle']" class="text-yellow-500 mt-1 mr-3" />
                  <div>
                    <h4 class="text-lg font-semibold text-yellow-800 dark:text-yellow-200">Subscription Scheduled for Cancellation</h4>
                    <p class="text-yellow-700 dark:text-yellow-300 mt-1">
                      Your subscription will end on {{ formatDate(paymentStore.currentSubscription.current_period_end) }}.
                      You'll retain access to all features until then.
                    </p>
                    <button
                      @click="handleReactivateSubscription"
                      class="mt-3 px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition-colors"
                    >
                      Keep My Subscription
                    </button>
                  </div>
                </div>
              </div>

              <!-- Payment History -->
              <div class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-200 dark:border-gray-700">
                <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Payment History</h4>
                <div v-if="paymentStore.paymentHistory.length > 0" class="space-y-3">
                  <div
                    v-for="payment in paymentStore.paymentHistory.slice(0, 5)"
                    :key="payment.id"
                    class="flex items-center justify-between py-3 border-b border-gray-200 dark:border-gray-700 last:border-b-0"
                  >
                    <div>
                      <p class="font-medium text-gray-900 dark:text-white">${{ payment.amount }}</p>
                      <p class="text-sm text-gray-600 dark:text-gray-400">{{ formatDate(payment.created_at) }}</p>
                    </div>
                    <span
                      class="px-2 py-1 rounded-full text-xs font-medium"
                      :class="payment.status === 'succeeded' ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'"
                    >
                      {{ payment.status }}
                    </span>
                  </div>
                </div>
                <div v-else class="text-center py-8 text-gray-500 dark:text-gray-400">
                  <font-awesome-icon :icon="['fas', 'credit-card']" class="h-12 w-12 mb-4 opacity-50" />
                  <p>No payment history yet</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

        <!-- Cancel Subscription Modal -->
    <div v-if="showCancelModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md w-full mx-4">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Cancel Subscription</h3>
        <p class="text-gray-600 dark:text-gray-400 mb-6">
          Are you sure you want to cancel your subscription? You'll lose access to premium features at the end of your billing period.
        </p>
        <div class="flex justify-end space-x-3">
          <button
            @click="showCancelModal = false"
            class="px-4 py-2 text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200"
          >
            Keep Subscription
          </button>
          <button
            @click="handleCancelSubscription"
            class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
          >
            Cancel Subscription
          </button>
        </div>
      </div>
    </div>
  </Layout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { usePaymentStore } from '../stores/payment';
import Layout from '../components/Layout.vue';
import apiClient from '../services/api';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const paymentStore = usePaymentStore();

// Stats
const totalBooks = ref(0);
const completedBooks = ref(0);
const inProgressBooks = ref(0);
const monthlyBooksUsed = ref(0);
const loading = ref(false);
const showCancelModal = ref(false);

// Computed
const currentTab = computed(() => {
  if (route.path === '/profile/subscription') return 'subscription';
  if (route.path === '/profile/mybooks') return 'mybooks';
  if (route.path === '/profile/create') return 'create';
  return 'dashboard';
});

// Load user's books and subscription data on mount
onMounted(async () => {
  try {
    loading.value = true;

    // Load books
    const response = await apiClient.get('/books/');
    const books = response.data;

    totalBooks.value = books.length;
    completedBooks.value = books.filter((b: any) => b.status === 'ready').length;
    inProgressBooks.value = books.filter((b: any) => ['generating', 'content_generated', 'cover_pending'].includes(b.status)).length;

    // Calculate monthly usage
    const now = new Date();
    const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1);
    monthlyBooksUsed.value = books.filter((b: any) => new Date(b.created_at) >= startOfMonth).length;

    // Load subscription data
    await paymentStore.fetchCurrentSubscription();
    await paymentStore.fetchPaymentHistory();

  } catch (error) {
    console.error('Failed to load data:', error);
  } finally {
    loading.value = false;
  }
});

// Utility functions
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

// Subscription management
const handleReactivateSubscription = async () => {
  try {
    await paymentStore.reactivateSubscription();
  } catch (error) {
    console.error('Failed to reactivate subscription:', error);
  }
};

const handleCancelSubscription = async () => {
  try {
    await paymentStore.cancelSubscription();
    showCancelModal.value = false;
  } catch (error) {
    console.error('Failed to cancel subscription:', error);
  }
};

const handleSignOut = async () => {
  const result = await authStore.signOut();
  if (result.success) {
    router.push('/auth/signin');
  }
};
</script>
