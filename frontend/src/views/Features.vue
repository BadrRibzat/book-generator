<template>
  <Layout>
    <!-- Hero Section -->
    <section class="bg-gradient-to-br from-primary-50 to-white py-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h1 class="text-4xl md:text-5xl font-extrabold text-gray-900 mb-6">
          Powerful Features for Book Creation
        </h1>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto">
          Everything you need to create, customize, and publish professional books with AI assistance
        </p>
      </div>
    </section>

    <!-- Main Features -->
    <section class="py-20 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center mb-20">
          <div>
            <div class="inline-block bg-primary-100 text-primary-600 px-4 py-1 rounded-full text-sm font-semibold mb-4">
              AI-Powered
            </div>
            <h2 class="text-3xl font-bold text-gray-900 mb-4">
              Advanced Content Generation
            </h2>
            <p class="text-lg text-gray-600 mb-6">
              Powered by Groq's Llama 3.1 70B, our AI generates high-quality, engaging content that reads naturally and provides real value to readers.
            </p>
            <ul class="space-y-3">
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check-circle']" class="text-green-500 mt-1 mr-3" />
                <span class="text-gray-700">45 market-optimized title templates across all niches</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check-circle']" class="text-green-500 mt-1 mr-3" />
                <span class="text-gray-700">Coherent chapter structure with logical flow</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check-circle']" class="text-green-500 mt-1 mr-3" />
                <span class="text-gray-700">15-30 pages of valuable, actionable content</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check-circle']" class="text-green-500 mt-1 mr-3" />
                <span class="text-gray-700">Niche-specific terminology and examples</span>
              </li>
            </ul>
          </div>
          <div class="bg-gradient-to-br from-blue-100 to-purple-100 rounded-2xl p-12 text-center">
            <font-awesome-icon :icon="['fas', 'brain']" class="text-6xl text-primary-600 mb-4" />
            <h3 class="text-2xl font-bold text-gray-900">AI Content Engine</h3>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center mb-20">
          <div class="order-2 lg:order-1 bg-gradient-to-br from-pink-100 to-red-100 rounded-2xl p-12 text-center">
            <font-awesome-icon :icon="['fas', 'palette']" class="text-6xl text-purple-600 mb-4" />
            <h3 class="text-2xl font-bold text-gray-900">Cover Designer</h3>
          </div>
          <div class="order-1 lg:order-2">
            <div class="inline-block bg-purple-100 text-purple-600 px-4 py-1 rounded-full text-sm font-semibold mb-4">
              Professional Design
            </div>
            <h2 class="text-3xl font-bold text-gray-900 mb-4">
              Stunning Cover Designs
            </h2>
            <p class="text-lg text-gray-600 mb-6">
              Get 3 professionally designed covers for every book, each with psychology-based color schemes optimized for your niche.
            </p>
            <ul class="space-y-3">
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check-circle']" class="text-green-500 mt-1 mr-3" />
                <span class="text-gray-700">Modern, Bold, and Elegant style options</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check-circle']" class="text-green-500 mt-1 mr-3" />
                <span class="text-gray-700">Niche-specific color palettes (15 unique schemes)</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check-circle']" class="text-green-500 mt-1 mr-3" />
                <span class="text-gray-700">Professional typography and layout</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check-circle']" class="text-green-500 mt-1 mr-3" />
                <span class="text-gray-700">Amazon KDP and POD platform ready</span>
              </li>
            </ul>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          <div>
            <div class="inline-block bg-green-100 text-green-600 px-4 py-1 rounded-full text-sm font-semibold mb-4">
              Print-Ready
            </div>
            <h2 class="text-3xl font-bold text-gray-900 mb-4">
              Professional PDF Output
            </h2>
            <p class="text-lg text-gray-600 mb-6">
              Download high-quality, professionally formatted PDFs ready for immediate publishing on any platform.
            </p>
            <ul class="space-y-3">
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check-circle']" class="text-green-500 mt-1 mr-3" />
                <span class="text-gray-700">Industry-standard formatting and margins</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check-circle']" class="text-green-500 mt-1 mr-3" />
                <span class="text-gray-700">Perfect cover + interior PDF merge</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check-circle']" class="text-green-500 mt-1 mr-3" />
                <span class="text-gray-700">Compatible with Amazon KDP, IngramSpark, Lulu</span>
              </li>
              <li class="flex items-start">
                <font-awesome-icon :icon="['fas', 'check-circle']" class="text-green-500 mt-1 mr-3" />
                <span class="text-gray-700">One-click download after generation</span>
              </li>
            </ul>
          </div>
          <div class="bg-gradient-to-br from-green-100 to-teal-100 rounded-2xl p-12 text-center">
            <font-awesome-icon :icon="['fas', 'file-pdf']" class="text-6xl text-green-600 mb-4" />
            <h3 class="text-2xl font-bold text-gray-900">PDF Generator</h3>
          </div>
        </div>
      </div>
    </section>

    <!-- Additional Features Grid -->
    <section class="py-20 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-3xl font-bold text-gray-900 mb-4">
            More Powerful Features
          </h2>
          <p class="text-xl text-gray-600">
            Everything you need in one platform
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="bg-white rounded-xl p-6 shadow-md hover:shadow-lg transition-shadow">
            <font-awesome-icon :icon="['fas', 'gauge-high']" class="text-3xl text-primary-600 mb-4" />
            <h3 class="text-lg font-bold text-gray-900 mb-2">Lightning Fast</h3>
            <p class="text-gray-600">Generate complete books in minutes, not weeks. Get to market faster than ever.</p>
          </div>

          <div class="bg-white rounded-xl p-6 shadow-md hover:shadow-lg transition-shadow">
            <font-awesome-icon :icon="['fas', 'mobile-alt']" class="text-3xl text-primary-600 mb-4" />
            <h3 class="text-lg font-bold text-gray-900 mb-2">Mobile Responsive</h3>
            <p class="text-gray-600">Access and manage your books from any device - desktop, tablet, or mobile.</p>
          </div>

          <div class="bg-white rounded-xl p-6 shadow-md hover:shadow-lg transition-shadow">
            <font-awesome-icon :icon="['fas', 'database']" class="text-3xl text-primary-600 mb-4" />
            <h3 class="text-lg font-bold text-gray-900 mb-2">Cloud Storage</h3>
            <p class="text-gray-600">All your books stored securely in the cloud. Access them anytime, anywhere.</p>
          </div>

          <div class="bg-white rounded-xl p-6 shadow-md hover:shadow-lg transition-shadow">
            <font-awesome-icon :icon="['fas', 'chart-line']" class="text-3xl text-primary-600 mb-4" />
            <h3 class="text-lg font-bold text-gray-900 mb-2">Progress Tracking</h3>
            <p class="text-gray-600">Monitor book generation status in real-time with detailed progress indicators.</p>
          </div>

          <div class="bg-white rounded-xl p-6 shadow-md hover:shadow-lg transition-shadow">
            <font-awesome-icon :icon="['fas', 'book-open']" class="text-3xl text-primary-600 mb-4" />
            <h3 class="text-lg font-bold text-gray-900 mb-2">Book Library</h3>
            <p class="text-gray-600">Organize and manage all your generated books in one central dashboard.</p>
          </div>

          <div class="bg-white rounded-xl p-6 shadow-md hover:shadow-lg transition-shadow">
            <font-awesome-icon :icon="['fas', 'code']" class="text-3xl text-primary-600 mb-4" />
            <h3 class="text-lg font-bold text-gray-900 mb-2">REST API</h3>
            <p class="text-gray-600">Full REST API with Swagger documentation for advanced integrations.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="py-20 bg-primary-600">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-3xl md:text-4xl font-bold text-white mb-6">
          Start Creating Amazing Books Today
        </h2>
        <p class="text-xl text-primary-100 mb-8">
          All features included. No credit card required.
        </p>
        <router-link
          to="/auth/signup"
          class="inline-flex items-center justify-center px-8 py-4 border-2 border-white text-lg font-medium rounded-lg text-primary-600 bg-white hover:bg-primary-50 transition-all duration-200"
        >
          Get Started Free
          <font-awesome-icon :icon="['fas', 'arrow-right']" class="ml-2" />
        </router-link>
      </div>
    </section>
  </Layout>
</template>

<script setup lang="ts">
import Layout from '../components/Layout.vue';
</script>
