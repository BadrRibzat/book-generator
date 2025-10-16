<template>
  <Layout>
    <!-- Hero Section -->
    <section class="bg-gradient-to-br from-primary-50 to-white py-20">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
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
                <span class="text-gray-700">3 books per month</span>
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
                <span class="text-gray-700">Up to 20 pages</span>
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

            <router-link
              to="/auth/signup"
              class="block w-full text-center px-6 py-3 border border-gray-300 text-base font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 transition-all"
            >
              Get Started Free
            </router-link>
          </div>

          <!-- Pro Plan (Popular) -->
          <div class="bg-gradient-to-br from-primary-600 to-primary-700 rounded-2xl p-8 transform scale-105 shadow-2xl relative">
            <div class="absolute top-0 right-0 bg-yellow-400 text-gray-900 px-4 py-1 rounded-bl-lg rounded-tr-lg text-sm font-bold">
              POPULAR
            </div>
            <h3 class="text-2xl font-bold text-white mb-2">Pro</h3>
            <div class="mb-6">
              <span class="text-5xl font-extrabold text-white">$29</span>
              <span class="text-primary-100">/month</span>
            </div>
            <p class="text-primary-100 mb-6">For serious authors and entrepreneurs</p>
            
            <ul class="space-y-4 mb-8">
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-300 mt-1 mr-3" />
                <span class="text-white">Unlimited books</span>
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
                <span class="text-white">Advanced customization</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-300 mt-1 mr-3" />
                <span class="text-white">API access</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-300 mt-1 mr-3" />
                <span class="text-white">Email support</span>
              </li>
            </ul>

            <router-link
              to="/auth/signup"
              class="block w-full text-center px-6 py-3 border-2 border-white text-base font-medium rounded-lg text-primary-600 bg-white hover:bg-primary-50 transition-all"
            >
              Start Pro Trial
            </router-link>
          </div>

          <!-- Enterprise Plan -->
          <div class="bg-white border-2 border-gray-200 rounded-2xl p-8 hover:shadow-xl transition-shadow">
            <h3 class="text-2xl font-bold text-gray-900 mb-2">Enterprise</h3>
            <div class="mb-6">
              <span class="text-5xl font-extrabold text-gray-900">Custom</span>
            </div>
            <p class="text-gray-600 mb-6">For teams and large-scale operations</p>
            
            <ul class="space-y-4 mb-8">
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3" />
                <span class="text-gray-700">Everything in Pro</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3" />
                <span class="text-gray-700">Custom niches</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3" />
                <span class="text-gray-700">White-label options</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3" />
                <span class="text-gray-700">Custom AI training</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3" />
                <span class="text-gray-700">Dedicated support</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3" />
                <span class="text-gray-700">SLA guarantee</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3" />
                <span class="text-gray-700">On-premise deployment</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mt-1 mr-3" />
                <span class="text-gray-700">Team management</span>
              </li>
            </ul>

            <a
              href="#"
              class="block w-full text-center px-6 py-3 border border-gray-300 text-base font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 transition-all"
            >
              Contact Sales
            </a>
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
import Layout from '../components/Layout.vue';
</script>
