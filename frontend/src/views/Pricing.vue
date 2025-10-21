<template>
  <Layout>
    <div class="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-100 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900">
      <!-- Hero Section with Glassmorphism -->
      <div class="relative overflow-hidden">
        <!-- Animated Background -->
        <div class="absolute inset-0 bg-gradient-to-r from-primary-600 via-primary-700 to-primary-800">
          <div class="absolute inset-0 opacity-20">
            <div class="absolute top-20 right-20 w-64 h-64 bg-white/10 rounded-full blur-3xl animate-float"></div>
            <div class="absolute bottom-20 left-20 w-48 h-48 bg-white/5 rounded-full blur-3xl animate-float" style="animation-delay: 3s"></div>
          </div>
        </div>

        <!-- Glass Header Card -->
        <div class="relative z-10 glass-card m-6 p-8">
          <div class="text-center">
            <!-- User Status -->
            <div v-if="authStore.isAuthenticated" class="mb-6">
              <div class="inline-flex items-center px-4 py-2 bg-white/20 text-white rounded-full text-sm font-medium backdrop-blur-sm">
                <font-awesome-icon :icon="['fas', 'user']" class="mr-2" />
                Currently on {{ currentPlanName }} plan
                <span v-if="currentPlan !== 'free'" class="ml-2 px-2 py-1 bg-green-500/20 text-green-200 rounded text-xs backdrop-blur-sm">ACTIVE</span>
              </div>
            </div>

            <h1 class="text-4xl md:text-5xl font-bold text-white mb-6 display-font">
              Simple, Transparent <span class="text-gradient">Pricing</span>
            </h1>
            <p class="text-xl text-primary-100 max-w-2xl mx-auto">
              Start free and scale as you grow. No hidden fees, no surprises.
            </p>
          </div>
        </div>
      </div>

      <!-- Pricing Cards with Glassmorphism -->
      <section class="py-20">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <!-- Free Plan -->
            <div class="card-modern interactive-card relative">
              <div class="text-center mb-6">
                <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">Free</h3>
                <div class="mb-4">
                  <span class="text-5xl font-extrabold text-gray-900 dark:text-white">$0</span>
                  <span class="text-gray-600 dark:text-gray-400">/month</span>
                </div>
                <p class="text-gray-600 dark:text-gray-300 text-sm">Perfect for getting started</p>
              </div>

              <ul class="space-y-3 mb-8">
                <li class="flex items-start">
                  <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3 flex-shrink-0" />
                  <span class="text-gray-700 dark:text-gray-300 text-sm">1 book per day</span>
                </li>
                <li class="flex items-start">
                  <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3 flex-shrink-0" />
                  <span class="text-gray-700 dark:text-gray-300 text-sm">32 trending niches</span>
                </li>
                <li class="flex items-start">
                  <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3 flex-shrink-0" />
                  <span class="text-gray-700 dark:text-gray-300 text-sm">3 AI cover designs</span>
                </li>
                <li class="flex items-start">
                  <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3 flex-shrink-0" />
                  <span class="text-gray-700 dark:text-gray-300 text-sm">Up to 30 pages</span>
                </li>
                <li class="flex items-start">
                  <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3 flex-shrink-0" />
                  <span class="text-gray-700 dark:text-gray-300 text-sm">PDF downloads</span>
                </li>
              </ul>

              <button
                @click="selectPlan('free')"
                class="block w-full text-center px-6 py-3 border border-gray-300 dark:border-gray-600 text-base font-medium rounded-xl transition-all"
                :class="currentPlan === 'free' ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200 border-green-300 cursor-default' : 'text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700'"
                :disabled="currentPlan === 'free'"
              >
                {{ currentPlan === 'free' ? '✓ Current Plan' : 'Get Started Free' }}
              </button>
            </div>

            <!-- Basic Plan -->
            <div class="card-modern interactive-card relative transform scale-105 shadow-glass-lg">
              <div class="absolute -top-4 left-1/2 transform -translate-x-1/2">
                <div class="bg-gradient-to-r from-yellow-400 to-orange-500 text-gray-900 px-4 py-2 rounded-full text-sm font-bold shadow-lg">
                  MOST POPULAR
                </div>
              </div>
              <div class="text-center mb-6">
                <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">Basic</h3>
                <div class="mb-4">
                  <span class="text-5xl font-extrabold text-gray-900 dark:text-white">$15</span>
                  <span class="text-gray-600 dark:text-gray-400">/month</span>
                </div>
                <p class="text-gray-600 dark:text-gray-300 text-sm">Perfect for individual authors</p>
              </div>

              <ul class="space-y-3 mb-8">
                <li class="flex items-start">
                  <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3 flex-shrink-0" />
                  <span class="text-gray-700 dark:text-gray-300 text-sm">1 book per day</span>
                </li>
                <li class="flex items-start">
                  <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3 flex-shrink-0" />
                  <span class="text-gray-700 dark:text-gray-300 text-sm">32 trending niches</span>
                </li>
                <li class="flex items-start">
                  <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3 flex-shrink-0" />
                  <span class="text-gray-700 dark:text-gray-300 text-sm">3 AI cover designs</span>
                </li>
                <li class="flex items-start">
                  <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3 flex-shrink-0" />
                  <span class="text-gray-700 dark:text-gray-300 text-sm">Up to 30 pages</span>
                </li>
                <li class="flex items-start">
                  <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3 flex-shrink-0" />
                  <span class="text-gray-700 dark:text-gray-300 text-sm">Priority generation</span>
                </li>
                <li class="flex items-start">
                  <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3 flex-shrink-0" />
                  <span class="text-gray-700 dark:text-gray-300 text-sm">Email support</span>
                </li>
              </ul>

              <button
                @click="selectPlan('basic')"
                class="block w-full text-center px-6 py-3 btn-primary text-base font-medium rounded-xl transition-all shadow-lg hover:shadow-xl"
                :disabled="currentPlan === 'basic'"
              >
                {{ currentPlan === 'basic' ? '✓ Current Plan' : 'Start Basic Plan' }}
              </button>
            </div>

            <!-- Premium Plan -->
            <div class="card-modern interactive-card relative">
              <div class="text-center mb-6">
                <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">Premium</h3>
                <div class="mb-4">
                  <span class="text-5xl font-extrabold text-gray-900 dark:text-white">$45</span>
                  <span class="text-gray-600 dark:text-gray-400">/month</span>
                </div>
                <p class="text-gray-600 dark:text-gray-300 text-sm">For prolific authors</p>
              </div>

              <ul class="space-y-3 mb-8">
                <li class="flex items-start">
                  <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3 flex-shrink-0" />
                  <span class="text-gray-700 dark:text-gray-300 text-sm">3 books per day</span>
                </li>
                <li class="flex items-start">
                  <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3 flex-shrink-0" />
                  <span class="text-gray-700 dark:text-gray-300 text-sm">32 trending niches</span>
                </li>
                <li class="flex items-start">
                  <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3 flex-shrink-0" />
                  <span class="text-gray-700 dark:text-gray-300 text-sm">3 AI cover designs</span>
                </li>
                <li class="flex items-start">
                  <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3 flex-shrink-0" />
                  <span class="text-gray-700 dark:text-gray-300 text-sm">Up to 30 pages</span>
                </li>
                <li class="flex items-start">
                  <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3 flex-shrink-0" />
                  <span class="text-gray-700 dark:text-gray-300 text-sm">Priority generation</span>
                </li>
                <li class="flex items-start">
                  <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3 flex-shrink-0" />
                  <span class="text-gray-700 dark:text-gray-300 text-sm">Advanced customization</span>
                </li>
                <li class="flex items-start">
                  <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3 flex-shrink-0" />
                  <span class="text-gray-700 dark:text-gray-300 text-sm">Priority support</span>
                </li>
              </ul>

              <button
                @click="selectPlan('premium')"
                class="block w-full text-center px-6 py-3 border border-gray-300 dark:border-gray-600 text-base font-medium rounded-xl transition-all"
                :class="currentPlan === 'premium' ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200 border-green-300 cursor-default' : 'text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700'"
                :disabled="currentPlan === 'premium'"
              >
                {{ currentPlan === 'premium' ? '✓ Current Plan' : 'Start Premium Plan' }}
              </button>
            </div>

            <!-- Enterprise Plan -->
            <div class="card-modern interactive-card relative">
              <div class="text-center mb-6">
                <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">Enterprise</h3>
                <div class="mb-4">
                  <span class="text-5xl font-extrabold text-gray-900 dark:text-white">$60</span>
                  <span class="text-gray-600 dark:text-gray-400">/month</span>
                </div>
                <p class="text-gray-600 dark:text-gray-300 text-sm">For teams & publishers</p>
              </div>

              <ul class="space-y-3 mb-8">
                <li class="flex items-start">
                  <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3 flex-shrink-0" />
                  <span class="text-gray-700 dark:text-gray-300 text-sm">5 books per day</span>
                </li>
                <li class="flex items-start">
                  <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3 flex-shrink-0" />
                  <span class="text-gray-700 dark:text-gray-300 text-sm">Everything in Premium</span>
                </li>
                <li class="flex items-start">
                  <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3 flex-shrink-0" />
                  <span class="text-gray-700 dark:text-gray-300 text-sm">Custom niches & training</span>
                </li>
                <li class="flex items-start">
                  <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3 flex-shrink-0" />
                  <span class="text-gray-700 dark:text-gray-300 text-sm">Dedicated support</span>
                </li>
                <li class="flex items-start">
                  <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3 flex-shrink-0" />
                  <span class="text-gray-700 dark:text-gray-300 text-sm">API access</span>
                </li>
              </ul>

              <button
                @click="selectPlan('enterprise')"
                class="block w-full text-center px-6 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 text-white text-base font-medium rounded-xl transition-all shadow-lg hover:shadow-xl hover:from-purple-700 hover:to-indigo-700"
                :disabled="currentPlan === 'enterprise'"
              >
                {{ currentPlan === 'enterprise' ? '✓ Current Plan' : 'Contact Sales' }}
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- FAQ Section with Glassmorphism -->
      <section class="py-20 bg-gradient-to-b from-white to-slate-50 dark:from-slate-800 dark:to-slate-900">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="text-center mb-16">
            <h2 class="text-4xl md:text-5xl font-bold mb-4 display-font">
              <span class="text-gradient">Frequently Asked Questions</span>
            </h2>
            <p class="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
              Everything you need to know about our pricing and features
            </p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div v-for="(faq, index) in faqs" :key="index" class="card-modern interactive-card">
              <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-3">{{ faq.question }}</h3>
              <p class="text-gray-600 dark:text-gray-300 leading-relaxed">{{ faq.answer }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- CTA Section with Glassmorphism -->
      <section class="py-20 bg-gradient-to-r from-primary-600 via-primary-700 to-primary-800 relative overflow-hidden">
        <!-- Background Pattern -->
        <div class="absolute inset-0 opacity-10">
          <div class="absolute top-20 right-20 w-64 h-64 bg-white/10 rounded-full blur-3xl animate-float"></div>
          <div class="absolute bottom-20 left-20 w-48 h-48 bg-white/5 rounded-full blur-3xl animate-float" style="animation-delay: 3s"></div>
        </div>

        <div class="relative z-10 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 class="text-4xl md:text-5xl font-bold text-white mb-6 display-font">
            Ready to Start Creating?
          </h2>
          <p class="text-xl text-primary-100 mb-8 leading-relaxed">
            Join thousands of authors using AI to create professional books faster than ever before.
          </p>

          <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <router-link
              to="/auth/signup"
              class="btn-secondary inline-flex items-center justify-center group text-lg px-8 py-4"
            >
              <font-awesome-icon :icon="['fas', 'rocket']" class="mr-3 group-hover:animate-bounce" />
              Start Free Today
            </router-link>

            <router-link
              to="/profile/create"
              class="glass-button inline-flex items-center justify-center group text-lg px-8 py-4 text-white"
            >
              <font-awesome-icon :icon="['fas', 'plus']" class="mr-3 group-hover:animate-pulse" />
              Create Your First Book
            </router-link>
          </div>
        </div>
      </section>
    </div>
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

// FAQs data
const faqs = ref([
  {
    question: "Can I upgrade or downgrade my plan?",
    answer: "Yes! You can upgrade or downgrade at any time. Changes will be reflected in your next billing cycle."
  },
  {
    question: "What payment methods do you accept?",
    answer: "We accept all major credit cards, PayPal, and wire transfers for Enterprise plans."
  },
  {
    question: "Is there a free trial for paid plans?",
    answer: "Yes! All paid plans come with a 14-day free trial. No credit card required to start."
  },
  {
    question: "Can I cancel anytime?",
    answer: "Absolutely. Cancel anytime with no penalties. You'll retain access until the end of your billing period."
  },
  {
    question: "Do you offer refunds?",
    answer: "We offer a 30-day money-back guarantee if you're not satisfied with the service."
  },
  {
    question: "What happens to my books if I cancel?",
    answer: "You retain full ownership of all books created. Download them before cancellation and keep them forever."
  }
])

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

<style scoped>
/* Glassmorphism Effects */
.glass-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
}

.card-modern {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.interactive-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.interactive-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.btn-primary:hover {
  background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

.glass-button {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}

.glass-button:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

.text-gradient {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.shadow-glass-lg {
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1), 0 0 0 1px rgba(255, 255, 255, 0.2);
}

/* Floating Animation */
@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

.animate-float {
  animation: float 6s ease-in-out infinite;
}

/* Dark mode adjustments */
.dark .glass-card {
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.dark .card-modern {
  background: rgba(0, 0, 0, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  /* Mobile hero section */
  .glass-card {
    margin: 1rem;
    padding: 1.5rem;
  }

  /* Mobile pricing cards */
  .grid.grid-cols-1.md\\:grid-cols-2.lg\\:grid-cols-4 {
    gap: 1rem;
  }

  .card-modern {
    padding: 1.5rem;
  }

  .card-modern .text-5xl {
    font-size: 2.5rem;
  }

  .card-modern .text-2xl {
    font-size: 1.25rem;
  }

  .card-modern ul li {
    font-size: 0.875rem;
  }

  /* Mobile FAQ section */
  .grid.grid-cols-1.md\\:grid-cols-2 {
    gap: 1rem;
  }

  .card-modern.interactive-card {
    padding: 1.5rem;
  }

  /* Mobile CTA section */
  .flex.flex-col.sm\\:flex-row {
    gap: 1rem;
  }

  .btn-secondary, .glass-button {
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
  }
}

@media (max-width: 640px) {
  /* Extra small screens */
  .max-w-7xl.mx-auto {
    padding-left: 0.5rem;
    padding-right: 0.5rem;
  }

  .text-4xl.md\\:text-5xl {
    font-size: 2rem;
  }

  .text-3xl {
    font-size: 1.5rem;
  }

  .text-2xl {
    font-size: 1.25rem;
  }

  .text-xl {
    font-size: 1rem;
  }

  /* Stack all grids vertically on very small screens */
  .grid.grid-cols-1.md\\:grid-cols-2.lg\\:grid-cols-4 {
    grid-template-columns: 1fr;
  }

  .grid.grid-cols-1.md\\:grid-cols-2 {
    grid-template-columns: 1fr;
  }

  /* Adjust spacing */
  .py-20 {
    padding-top: 3rem;
    padding-bottom: 3rem;
  }

  .mb-16 {
    margin-bottom: 2rem;
  }

  .mb-8 {
    margin-bottom: 1.5rem;
  }

  .mb-6 {
    margin-bottom: 1rem;
  }

  /* Adjust button sizes */
  .btn-primary {
    padding: 0.75rem 1.5rem;
    font-size: 0.875rem;
  }

  .btn-secondary, .glass-button {
    padding: 0.75rem 1.5rem;
    font-size: 0.875rem;
  }

  /* Prevent zoom on iOS inputs */
  input, select, textarea {
    font-size: 16px;
  }
}
</style>
