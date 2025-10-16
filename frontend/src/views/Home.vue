<template>
  <Layout>
    <!-- Hero Section -->
    <section class="bg-gradient-to-br from-primary-50 via-white to-primary-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 md:py-32">
        <div class="text-center">
          <h1 class="text-4xl md:text-6xl font-extrabold text-gray-900 mb-6">
            Create Professional Books
            <span class="text-primary-600 block mt-2">Powered by AI</span>
          </h1>
          <p class="text-xl md:text-2xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Generate high-quality, market-ready books in minutes. Choose from 15 trending niches, customize your content, and get stunning covers automatically.
          </p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <router-link
              to="/auth/signup"
              class="inline-flex items-center justify-center px-8 py-4 border border-transparent text-base font-medium rounded-lg text-white bg-primary-600 hover:bg-primary-700 shadow-lg hover:shadow-xl transition-all duration-200"
            >
              <font-awesome-icon :icon="['fas', 'rocket']" class="mr-2" />
              Start Creating Free
            </router-link>
            <router-link
              to="/features"
              class="inline-flex items-center justify-center px-8 py-4 border border-gray-300 text-base font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 shadow-lg transition-all duration-200"
            >
              <font-awesome-icon :icon="['fas', 'play-circle']" class="mr-2" />
              See How It Works
            </router-link>
          </div>

          <!-- Stats -->
          <div class="mt-16 grid grid-cols-2 md:grid-cols-4 gap-8">
            <div>
              <div class="text-4xl font-bold text-primary-600">15+</div>
              <div class="text-gray-600 mt-2">Trending Niches</div>
            </div>
            <div>
              <div class="text-4xl font-bold text-primary-600">3</div>
              <div class="text-gray-600 mt-2">Cover Styles</div>
            </div>
            <div>
              <div class="text-4xl font-bold text-primary-600">30</div>
              <div class="text-gray-600 mt-2">Max Pages</div>
            </div>
            <div>
              <div class="text-4xl font-bold text-primary-600">AI</div>
              <div class="text-gray-600 mt-2">Powered Content</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Preview -->
    <section class="py-20 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Everything You Need to Create Amazing Books
          </h2>
          <p class="text-xl text-gray-600 max-w-2xl mx-auto">
            Our AI-powered platform handles content generation, cover design, and PDF creation automatically.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-8 hover:shadow-lg transition-shadow">
            <div class="w-12 h-12 bg-blue-600 rounded-lg flex items-center justify-center mb-4">
              <font-awesome-icon :icon="['fas', 'brain']" class="text-white text-2xl" />
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-2">AI Content Generation</h3>
            <p class="text-gray-600">
              Leveraging Llama 3.1 70B to create engaging, well-structured content tailored to your chosen niche.
            </p>
          </div>

          <div class="bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl p-8 hover:shadow-lg transition-shadow">
            <div class="w-12 h-12 bg-purple-600 rounded-lg flex items-center justify-center mb-4">
              <font-awesome-icon :icon="['fas', 'palette']" class="text-white text-2xl" />
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-2">Professional Covers</h3>
            <p class="text-gray-600">
              Choose from 3 automatically generated cover designs with niche-specific color schemes and typography.
            </p>
          </div>

          <div class="bg-gradient-to-br from-green-50 to-green-100 rounded-xl p-8 hover:shadow-lg transition-shadow">
            <div class="w-12 h-12 bg-green-600 rounded-lg flex items-center justify-center mb-4">
              <font-awesome-icon :icon="['fas', 'file-pdf']" class="text-white text-2xl" />
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-2">Print-Ready PDFs</h3>
            <p class="text-gray-600">
              Get perfectly formatted, high-quality PDFs ready for publishing on Amazon KDP, IngramSpark, or print-on-demand platforms.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Trending Niches -->
    <section class="py-20 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            15 Trending Niches
          </h2>
          <p class="text-xl text-gray-600 max-w-2xl mx-auto">
            We've curated the most profitable and trending book categories for 2025
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-5 gap-6">
          <div class="bg-white rounded-lg shadow-md p-6 hover:shadow-xl transition-shadow">
            <div class="text-3xl mb-3">📚</div>
            <h3 class="font-bold text-gray-900 mb-2">Language & Kids</h3>
            <ul class="text-sm text-gray-600 space-y-1">
              <li>• AI Learning Stories</li>
              <li>• Multilingual Coloring</li>
              <li>• Mindfulness Journals</li>
            </ul>
          </div>

          <div class="bg-white rounded-lg shadow-md p-6 hover:shadow-xl transition-shadow">
            <div class="text-3xl mb-3">💻</div>
            <h3 class="font-bold text-gray-900 mb-2">Technology & AI</h3>
            <ul class="text-sm text-gray-600 space-y-1">
              <li>• AI Ethics</li>
              <li>• No-Code Guides</li>
              <li>• Smart Home DIY</li>
            </ul>
          </div>

          <div class="bg-white rounded-lg shadow-md p-6 hover:shadow-xl transition-shadow">
            <div class="text-3xl mb-3">🥗</div>
            <h3 class="font-bold text-gray-900 mb-2">Nutrition</h3>
            <ul class="text-sm text-gray-600 space-y-1">
              <li>• Specialty Diets</li>
              <li>• Plant-Based Cooking</li>
              <li>• Mental Health Nutrition</li>
            </ul>
          </div>

          <div class="bg-white rounded-lg shadow-md p-6 hover:shadow-xl transition-shadow">
            <div class="text-3xl mb-3">🧘</div>
            <h3 class="font-bold text-gray-900 mb-2">Meditation</h3>
            <ul class="text-sm text-gray-600 space-y-1">
              <li>• Anxiety Relief</li>
              <li>• Sleep Meditation</li>
              <li>• Gratitude Journals</li>
            </ul>
          </div>

          <div class="bg-white rounded-lg shadow-md p-6 hover:shadow-xl transition-shadow">
            <div class="text-3xl mb-3">💪</div>
            <h3 class="font-bold text-gray-900 mb-2">Home Workout</h3>
            <ul class="text-sm text-gray-600 space-y-1">
              <li>• Equipment-Free</li>
              <li>• Remote Worker Yoga</li>
              <li>• Mobility Training</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works -->
    <section class="py-20 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            How It Works
          </h2>
          <p class="text-xl text-gray-600 max-w-2xl mx-auto">
            Create your book in just 3 simple steps
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-12">
          <div class="text-center">
            <div class="w-16 h-16 bg-primary-600 rounded-full flex items-center justify-center mx-auto mb-4 text-white text-2xl font-bold">
              1
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-2">Choose Your Niche</h3>
            <p class="text-gray-600">
              Select from 15 trending categories spanning technology, wellness, education, and lifestyle.
            </p>
          </div>

          <div class="text-center">
            <div class="w-16 h-16 bg-primary-600 rounded-full flex items-center justify-center mx-auto mb-4 text-white text-2xl font-bold">
              2
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-2">AI Generates Content</h3>
            <p class="text-gray-600">
              Our advanced AI creates compelling content and 3 professional cover designs automatically.
            </p>
          </div>

          <div class="text-center">
            <div class="w-16 h-16 bg-primary-600 rounded-full flex items-center justify-center mx-auto mb-4 text-white text-2xl font-bold">
              3
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-2">Download & Publish</h3>
            <p class="text-gray-600">
              Select your favorite cover and download a print-ready PDF. Publish on Amazon KDP or any POD platform.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-20 bg-gradient-to-r from-primary-600 to-primary-700">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-3xl md:text-4xl font-bold text-white mb-6">
          Ready to Create Your First Book?
        </h2>
        <p class="text-xl text-primary-100 mb-8">
          Join thousands of authors using AI to create professional books faster than ever.
        </p>
        <router-link
          to="/auth/signup"
          class="inline-flex items-center justify-center px-8 py-4 border-2 border-white text-lg font-medium rounded-lg text-primary-600 bg-white hover:bg-primary-50 shadow-xl hover:shadow-2xl transition-all duration-200"
        >
          <font-awesome-icon :icon="['fas', 'rocket']" class="mr-2" />
          Get Started Now - It's Free
        </router-link>
      </div>
    </section>
  </Layout>
</template>

<script setup lang="ts">
import Layout from '../components/Layout.vue';
</script>
