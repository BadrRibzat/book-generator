<template>
  <Layout>
    <!-- Hero Section -->
    <section class="bg-gradient-to-br from-primary-50 to-white py-20">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <!-- User Status -->
        <div v-if="authStore.isAuthenticated" class="mb-6">
          <div class="inline-flex items-center px-4 py-2 bg-primary-100 text-primary-800 rounded-full text-sm font-medium">
            <font-awesome-icon :icon="['fas', 'user']" class="mr-2" />
            Currently on {{ currentPlanName }} plan
            <span v-if="currentPlan !== 'free'" class="ml-2 px-2 py-1 bg-primary-200 rounded text-xs">ACTIVE</span>
          </div>
        </div>
        
        <h1 class="text-4xl md:text-5xl font-extrabold text-gray-900 mb-6">
          Simple, Transparent Pricing
        </h1>
        <p class="text-xl text-gray-600">
          Start free and scale as you grow. No hidden fees.
        </p>
      </div>
    </section>

    <!-- Pricing Cards -->
    <section class="py-20 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <!-- Free Plan -->
          <div class="bg-white border-2 border-gray-200 rounded-2xl p-8 hover:shadow-xl transition-shadow">
            <h3 class="text-2xl font-bold text-gray-900 mb-2">Free</h3>
            <div class="mb-6">
              <span class="text-5xl font-extrabold text-gray-900">$0</span>
              <span class="text-gray-600">/month</span>
            </div>
            <p class="text-gray-600 mb-6">Perfect for getting started and exploring the platform</p>
            
            <ul class="space-y-4 mb-8">
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3" />
                <span class="text-gray-700">1 book per day</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3" />
                <span class="text-gray-700">All 15 trending niches</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3" />
                <span class="text-gray-700">3 cover styles per book</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3" />
                <span class="text-gray-700">Up to 30 pages</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3" />
                <span class="text-gray-700">PDF downloads</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3" />
                <span class="text-gray-700">Cloud storage</span>
              </li>
            </ul>

            <button
              @click="selectPlan('free')"
              class="block w-full text-center px-6 py-3 border border-gray-300 text-base font-medium rounded-lg transition-all"
              :class="currentPlan === 'free' ? 'bg-green-100 text-green-800 border-green-300 cursor-default' : 'text-gray-700 bg-white hover:bg-gray-50'"
              :disabled="currentPlan === 'free'"
            >
              {{ currentPlan === 'free' ? '✓ Current Plan' : 'Get Started Free' }}
            </button>
          </div>

          <!-- Basic Plan -->
          <div class="bg-gradient-to-br from-primary-600 to-primary-700 rounded-2xl p-8 transform scale-105 shadow-2xl relative">
            <div class="absolute top-0 right-0 bg-yellow-400 text-gray-900 px-4 py-1 rounded-bl-lg rounded-tr-lg text-sm font-bold">
              MOST POPULAR
            </div>
            <h3 class="text-2xl font-bold text-white mb-2">Basic</h3>
            <div class="mb-6">
              <span class="text-5xl font-extrabold text-white">$15</span>
              <span class="text-primary-100">/month</span>
            </div>
            <p class="text-primary-100 mb-6">Perfect for individual authors and content creators</p>
            
            <ul class="space-y-4 mb-8">
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-300 mt-1 mr-3" />
                <span class="text-white">1 book per day</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-300 mt-1 mr-3" />
                <span class="text-white">All 15 trending niches</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-300 mt-1 mr-3" />
                <span class="text-white">3 cover styles per book</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-300 mt-1 mr-3" />
                <span class="text-white">Up to 30 pages</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-300 mt-1 mr-3" />
                <span class="text-white">Priority generation</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-300 mt-1 mr-3" />
                <span class="text-white">Email support</span>
              </li>
            </ul>

            <button
              @click="selectPlan('basic')"
              class="block w-full text-center px-6 py-3 border-2 text-base font-medium rounded-lg transition-all"
              :class="currentPlan === 'basic' ? 'border-green-300 text-green-800 bg-green-100 cursor-default' : 'border-white text-primary-600 bg-white hover:bg-primary-50'"
              :disabled="currentPlan === 'basic'"
            >
              {{ currentPlan === 'basic' ? '✓ Current Plan' : 'Start Basic Plan' }}
            </button>
          </div>

          <!-- Premium Plan -->
          <div class="bg-white border-2 border-gray-200 rounded-2xl p-8 hover:shadow-xl transition-shadow">
            <h3 class="text-2xl font-bold text-gray-900 mb-2">Premium</h3>
            <div class="mb-6">
              <span class="text-5xl font-extrabold text-gray-900">$45</span>
              <span class="text-gray-600">/month</span>
            </div>
            <p class="text-gray-600 mb-6">For prolific authors and growing businesses</p>
            
            <ul class="space-y-4 mb-8">
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3" />
                <span class="text-gray-700">3 books per day</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3" />
                <span class="text-gray-700">All 15 trending niches</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3" />
                <span class="text-gray-700">3 cover styles per book</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3" />
                <span class="text-gray-700">Up to 30 pages</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3" />
                <span class="text-gray-700">Priority generation</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3" />
                <span class="text-gray-700">Advanced customization</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3" />
                <span class="text-gray-700">Priority support</span>
              </li>
            </ul>

            <button
              @click="selectPlan('premium')"
              class="block w-full text-center px-6 py-3 border border-gray-300 text-base font-medium rounded-lg transition-all"
              :class="currentPlan === 'premium' ? 'bg-green-100 text-green-800 border-green-300 cursor-default' : 'text-gray-700 bg-white hover:bg-gray-50'"
              :disabled="currentPlan === 'premium'"
            >
              {{ currentPlan === 'premium' ? '✓ Current Plan' : 'Start Premium Plan' }}
            </button>
          </div>
        </div>

        <!-- Enterprise Plan -->
        <div class="mt-12 max-w-md mx-auto">
          <div class="bg-gradient-to-r from-purple-600 to-indigo-600 rounded-2xl p-8 text-center text-white">
            <h3 class="text-2xl font-bold mb-2">Enterprise</h3>
            <div class="mb-4">
              <span class="text-4xl font-extrabold">$60</span>
              <span class="text-purple-100">/month</span>
            </div>
            <p class="text-purple-100 mb-6">For teams and high-volume publishers</p>
            
            <ul class="space-y-2 mb-6 text-sm">
              <li class="flex items-center justify-center">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-300 mr-2" />
                <span>5 books per day</span>
              </li>
              <li class="flex items-center justify-center">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-300 mr-2" />
                <span>Everything in Premium</span>
              </li>
              <li class="flex items-center justify-center">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-300 mr-2" />
                <span>Custom niches & AI training</span>
              </li>
              <li class="flex items-center justify-center">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-300 mr-2" />
                <span>Dedicated support</span>
              </li>
            </ul>

            <button
              @click="selectPlan('enterprise')"
              class="block w-full text-center px-6 py-3 border-2 border-white text-base font-medium rounded-lg bg-white text-purple-600 hover:bg-purple-50 transition-all"
              :disabled="currentPlan === 'enterprise'"
            >
              {{ currentPlan === 'enterprise' ? '✓ Current Plan' : 'Contact Sales' }}
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- FAQ Section -->
    <section class="py-20 bg-gray-50">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 class="text-3xl font-bold text-gray-900 text-center mb-12">
          Frequently Asked Questions
        </h2>

        <div class="space-y-6">
          <div class="bg-white rounded-lg p-6 shadow-sm">
            <h3 class="text-lg font-bold text-gray-900 mb-2">Can I upgrade or downgrade my plan?</h3>
            <p class="text-gray-600">Yes! You can upgrade or downgrade at any time. Changes will be reflected in your next billing cycle.</p>
          </div>

          <div class="bg-white rounded-lg p-6 shadow-sm">
            <h3 class="text-lg font-bold text-gray-900 mb-2">What payment methods do you accept?</h3>
            <p class="text-gray-600">We accept all major credit cards, PayPal, and wire transfers for Enterprise plans.</p>
          </div>

          <div class="bg-white rounded-lg p-6 shadow-sm">
            <h3 class="text-lg font-bold text-gray-900 mb-2">Is there a free trial for Pro?</h3>
            <p class="text-gray-600">Yes! All Pro plans come with a 14-day free trial. No credit card required.</p>
          </div>

          <div class="bg-white rounded-lg p-6 shadow-sm">
            <h3 class="text-lg font-bold text-gray-900 mb-2">Can I cancel anytime?</h3>
            <p class="text-gray-600">Absolutely. Cancel anytime with no penalties. You'll retain access until the end of your billing period.</p>
          </div>

          <div class="bg-white rounded-lg p-6 shadow-sm">
            <h3 class="text-lg font-bold text-gray-900 mb-2">Do you offer refunds?</h3>
            <p class="text-gray-600">We offer a 30-day money-back guarantee if you're not satisfied with the service.</p>
          </div>

          <div class="bg-white rounded-lg p-6 shadow-sm">
            <h3 class="text-lg font-bold text-gray-900 mb-2">What happens to my books if I cancel?</h3>
            <p class="text-gray-600">You retain full ownership of all books created. Download them before cancellation and keep them forever.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="py-20 bg-primary-600">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-3xl font-bold text-white mb-6">
          Ready to Start Creating?
        </h2>
        <p class="text-xl text-primary-100 mb-8">
          Join thousands of authors using BookGen AI
        </p>
        <router-link
          to="/auth/signup"
          class="inline-flex items-center justify-center px-8 py-4 border-2 border-white text-lg font-medium rounded-lg text-primary-600 bg-white hover:bg-primary-50 transition-all duration-200"
        >
          Start Free Today
          <font-awesome-icon :icon="['fas', 'arrow-right']" class="ml-2" />
        </router-link>
      </div>
    </section>
  </Layout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import Layout from '../components/Layout.vue'
import apiClient from '../services/api'

const authStore = useAuthStore()
const router = useRouter()

// State
const subscriptionPlans = ref<any[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

// Computed
const currentPlan = computed(() => {
  return authStore.userProfile?.subscription_tier || 'free'
})

// Get current plan display name
const currentPlanName = computed(() => {
  const tier = currentPlan.value
  if (tier === 'basic') return 'Pro'
  if (tier === 'premium') return 'Pro'
  if (tier === 'enterprise') return 'Enterprise'
  return 'Free'
})

// Methods
async function fetchSubscriptionPlans() {
  try {
    loading.value = true
    const response = await apiClient.get('/users/subscription-plans/')
    subscriptionPlans.value = response.data
  } catch (err: any) {
    console.error('Failed to fetch subscription plans:', err)
    error.value = 'Failed to load subscription plans'
  } finally {
    loading.value = false
  }
}

async function selectPlan(planTier: string) {
  if (!authStore.isAuthenticated) {
    router.push('/auth/login')
    return
  }

  if (planTier === 'free') {
    // Handle free plan selection
    return
  }

  // For paid plans, redirect to payment/checkout
  // This will be implemented when Stripe integration is ready
  console.log(`Selected plan: ${planTier}`)
  
  // Placeholder for now - in production this would redirect to Stripe Checkout
  alert(`Plan selection for ${planTier} will be implemented with Stripe integration. Current plan: ${currentPlanName.value}`)
}

// Lifecycle
onMounted(async () => {
  await fetchSubscriptionPlans()
})
</script>
