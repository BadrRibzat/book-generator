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
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <!-- Free Plan -->
            <div class="card-modern interactive-card relative">
              <div class="text-center mb-6">
                <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">Free Tier</h3>
                <div class="mb-4">
                  <span class="text-5xl font-extrabold text-gray-900 dark:text-white">$0</span>
                  <span class="text-gray-600 dark:text-gray-400">/month</span>
                </div>
                <p class="text-gray-600 dark:text-gray-300 text-sm">Everyone starts here</p>
              </div>

              <ul class="space-y-3 mb-8">
                <li class="flex items-start">
                  <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3 flex-shrink-0" />
                  <span class="text-gray-700 dark:text-gray-300 text-sm">2 books per month</span>
                </li>
                <li class="flex items-start">
                  <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3 flex-shrink-0" />
                  <span class="text-gray-700 dark:text-gray-300 text-sm">15 pages max per book</span>
                </li>
                <li class="flex items-start">
                  <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3 flex-shrink-0" />
                  <span class="text-gray-700 dark:text-gray-300 text-sm">5 limited niches</span>
                </li>
                <li class="flex items-start">
                  <font-awesome-icon :icon="['fas', 'xmark']" class="text-red-500 mt-1 mr-3 flex-shrink-0" />
                  <span class="text-gray-700 dark:text-gray-300 text-sm line-through">Commercial license</span>
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

            <!-- Dynamic Paid Plans -->
            <div
              v-for="(plan, index) in subscriptionPlans"
              :key="plan.id"
              class="card-modern interactive-card relative transform"
              :class="index === 0 ? 'scale-105 shadow-glass-lg' : ''"
            >
              <div v-if="index === 0" class="absolute -top-4 left-1/2 transform -translate-x-1/2">
                <div class="bg-gradient-to-r from-yellow-400 to-orange-500 text-gray-900 px-4 py-2 rounded-full text-sm font-bold shadow-lg">
                  MOST POPULAR
                </div>
              </div>
              <div class="text-center mb-6">
                <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">{{ plan.name }}</h3>
                <div class="mb-4">
                  <span class="text-5xl font-extrabold text-gray-900 dark:text-white">${{ plan.price }}</span>
                  <span class="text-gray-600 dark:text-gray-400">/{{ plan.interval }}</span>
                </div>
                <p class="text-gray-600 dark:text-gray-300 text-sm">{{ plan.description || 'Perfect for creators' }}</p>
              </div>

              <ul class="space-y-3 mb-8">
                <li class="flex items-start">
                  <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3 flex-shrink-0" />
                  <span class="text-gray-700 dark:text-gray-300 text-sm">{{ plan.max_books_per_month }} books per month</span>
                </li>
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
              </ul>

              <button
                @click="selectPlan(plan.name.toLowerCase().replace(/\s+/g, '_'))"
                class="block w-full text-center px-6 py-3 btn-primary text-base font-medium rounded-xl transition-all shadow-lg hover:shadow-xl"
                :disabled="currentPlan === plan.name.toLowerCase().replace(/\s+/g, '_')"
              >
                {{ currentPlan === plan.name.toLowerCase().replace(/\s+/g, '_') ? '✓ Current Plan' : `Subscribe to ${plan.name}` }}
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Referral CTA Section -->
      <section class="py-20 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div class="glass-card p-8">
            <h2 class="text-4xl md:text-5xl font-bold mb-6 display-font">
              <span class="text-gradient">Refer a friend → Get 15% off</span>
            </h2>
            <p class="text-xl text-gray-600 dark:text-gray-300 mb-8 leading-relaxed">
              When subscriptions launch, you'll get 15% off your first year for every friend who signs up using your referral link.
            </p>

            <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <button
                @click="generateReferralCode"
                class="btn-primary inline-flex items-center justify-center group text-lg px-8 py-4"
              >
                <font-awesome-icon :icon="['fas', 'gift']" class="mr-3 group-hover:animate-bounce" />
                Get My Referral Code
              </button>

              <div v-if="referralCode" class="glass-card p-4">
                <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">Your referral code:</p>
                <div class="flex items-center gap-2">
                  <code class="bg-gray-100 dark:bg-gray-800 px-3 py-2 rounded text-lg font-mono">{{ referralCode }}</code>
                  <button @click="copyReferralCode" class="text-blue-600 hover:text-blue-800">
                    <font-awesome-icon :icon="['fas', 'copy']" />
                  </button>
                </div>
              </div>
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

    <!-- Stripe Checkout Modal -->
    <StripeCheckoutModal
      v-if="showCheckoutModal && selectedPlan"
      :plan="selectedPlan"
      @close="showCheckoutModal = false; selectedPlan = null"
      @success="handleCheckoutSuccess"
    />
  </Layout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { usePaymentStore } from '../stores/payment'
import Layout from '../components/Layout.vue'
import StripeCheckoutModal from '../components/StripeCheckoutModal.vue'
import apiClient from '../services/api'

const authStore = useAuthStore()
const paymentStore = usePaymentStore()
const router = useRouter()

// State
const subscriptionPlans = ref<any[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const referralCode = ref<string | null>(null)
const showCheckoutModal = ref(false)
const selectedPlan = ref<any>(null)

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
  if (!paymentStore.currentSubscription) return 'free'
  return paymentStore.currentSubscription.plan.name.toLowerCase().replace(/\s+/g, '_')
})

// Get current plan display name
const currentPlanName = computed(() => {
  if (!paymentStore.currentSubscription) return 'Free'
  return paymentStore.currentSubscription.plan.name
})

// Methods
async function fetchSubscriptionPlans() {
  try {
    loading.value = true
    await paymentStore.fetchSubscriptionPlans()
    subscriptionPlans.value = paymentStore.subscriptionPlans
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

  // Find the plan
  const plan = subscriptionPlans.value.find(p => p.name.toLowerCase().replace(' ', '_') === planTier)
  if (!plan) {
    console.error('Plan not found:', planTier)
    return
  }

  // Open checkout modal
  selectedPlan.value = plan
  showCheckoutModal.value = true
}

async function handleCheckoutSuccess(subscription: any) {
  console.log('Subscription created:', subscription)
  // Refresh subscription data
  await paymentStore.fetchCurrentSubscription()

  // Close modal
  showCheckoutModal.value = false
  selectedPlan.value = null
}

async function generateReferralCode() {
  if (!authStore.isAuthenticated) {
    router.push('/auth/login')
    return
  }

  try {
    const response = await apiClient.get('/users/referrals/generate_code/')
    referralCode.value = response.data.referral_code
  } catch (err: any) {
    console.error('Failed to generate referral code:', err)
    alert('Failed to generate referral code. Please try again.')
  }
}

async function copyReferralCode() {
  if (referralCode.value) {
    await navigator.clipboard.writeText(referralCode.value)
    alert('Referral code copied to clipboard!')
  }
}

// Lifecycle
onMounted(async () => {
  await fetchSubscriptionPlans()

  // Fetch current subscription if authenticated
  if (authStore.isAuthenticated) {
    try {
      await paymentStore.fetchCurrentSubscription()
    } catch (err) {
      console.log('No active subscription found')
    }
  }
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
