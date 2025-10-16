<template>
  <Layout>
    <!-- Hero Section -->
    <section class="bg-gradient-to-br from-primary-50 to-white py-20">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h1 class="text-4xl md:text-5xl font-extrabold text-gray-900 mb-6">
          About BookGen AI
        </h1>
        <p class="text-xl text-gray-600">
          Democratizing book publishing with the power of artificial intelligence
        </p>
      </div>
    </section>

    <!-- Mission -->
    <section class="py-20 bg-white">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-gray-900 mb-4">Our Mission</h2>
          <p class="text-lg text-gray-600 leading-relaxed">
            We believe everyone has a story to tell and knowledge to share. BookGen AI was created to remove the barriers to book publishing, making it possible for anyone to create professional, market-ready books in minutes instead of months.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16">
          <div class="text-center">
            <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <font-awesome-icon :icon="['fas', 'users']" class="text-primary-600 text-2xl" />
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-2">Accessible</h3>
            <p class="text-gray-600">No writing experience needed. Our AI handles the heavy lifting.</p>
          </div>

          <div class="text-center">
            <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <font-awesome-icon :icon="['fas', 'rocket']" class="text-primary-600 text-2xl" />
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-2">Fast</h3>
            <p class="text-gray-600">Create complete books in minutes, not months.</p>
          </div>

          <div class="text-center">
            <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <font-awesome-icon :icon="['fas', 'award']" class="text-primary-600 text-2xl" />
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-2">Professional</h3>
            <p class="text-gray-600">Market-ready quality that meets industry standards.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Technology -->
    <section class="py-20 bg-gray-50">
      <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-gray-900 mb-4">Powered by Cutting-Edge Technology</h2>
          <p class="text-lg text-gray-600">
            We leverage the latest advancements in AI and web technologies
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div class="bg-white rounded-xl p-8 shadow-md">
            <h3 class="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <font-awesome-icon :icon="['fas', 'brain']" class="text-primary-600 mr-3" />
              AI & Machine Learning
            </h3>
            <ul class="space-y-3 text-gray-600">
              <li>• <strong>Llama 3.1 70B</strong>: Advanced language model via Groq API</li>
              <li>• <strong>Smart Generation</strong>: Context-aware content creation</li>
              <li>• <strong>Niche Optimization</strong>: 45 market-tested title templates</li>
            </ul>
          </div>

          <div class="bg-white rounded-xl p-8 shadow-md">
            <h3 class="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <font-awesome-icon :icon="['fas', 'code']" class="text-primary-600 mr-3" />
              Modern Web Stack
            </h3>
            <ul class="space-y-3 text-gray-600">
              <li>• <strong>Vue 3 + TypeScript</strong>: Type-safe reactive frontend</li>
              <li>• <strong>Django REST Framework</strong>: Robust API backend</li>
              <li>• <strong>Tailwind CSS</strong>: Modern, responsive design</li>
            </ul>
          </div>

          <div class="bg-white rounded-xl p-8 shadow-md">
            <h3 class="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <font-awesome-icon :icon="['fas', 'palette']" class="text-primary-600 mr-3" />
              Design & Publishing
            </h3>
            <ul class="space-y-3 text-gray-600">
              <li>• <strong>WeasyPrint</strong>: Professional cover generation</li>
              <li>• <strong>ReportLab</strong>: High-quality interior formatting</li>
              <li>• <strong>PyPDF</strong>: Seamless PDF merging</li>
            </ul>
          </div>

          <div class="bg-white rounded-xl p-8 shadow-md">
            <h3 class="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <font-awesome-icon :icon="['fas', 'database']" class="text-primary-600 mr-3" />
              Data & Storage
            </h3>
            <ul class="space-y-3 text-gray-600">
              <li>• <strong>MongoDB Atlas</strong>: Scalable cloud storage</li>
              <li>• <strong>SQLite</strong>: Fast metadata management</li>
              <li>• <strong>RESTful API</strong>: Clean, documented endpoints</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Recap -->
    <section class="py-20 bg-white">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-gray-900 mb-4">What Makes Us Different</h2>
        </div>

        <div class="space-y-6">
          <div class="flex items-start">
            <div class="flex-shrink-0">
              <font-awesome-icon :icon="['fas', 'check-circle']" class="text-green-500 text-2xl mr-4" />
            </div>
            <div>
              <h3 class="text-lg font-bold text-gray-900 mb-1">15 Trending Niches</h3>
              <p class="text-gray-600">Carefully curated categories spanning Language Learning, Technology, Nutrition, Meditation, and Fitness - all proven profitable in 2025.</p>
            </div>
          </div>

          <div class="flex items-start">
            <div class="flex-shrink-0">
              <font-awesome-icon :icon="['fas', 'check-circle']" class="text-green-500 text-2xl mr-4" />
            </div>
            <div>
              <h3 class="text-lg font-bold text-gray-900 mb-1">Psychology-Based Design</h3>
              <p class="text-gray-600">Each niche has custom color schemes based on color psychology - playful for kids, professional for tech, calming for meditation.</p>
            </div>
          </div>

          <div class="flex items-start">
            <div class="flex-shrink-0">
              <font-awesome-icon :icon="['fas', 'check-circle']" class="text-green-500 text-2xl mr-4" />
            </div>
            <div>
              <h3 class="text-lg font-bold text-gray-900 mb-1">Complete API Documentation</h3>
              <p class="text-gray-600">Full Swagger/ReDoc documentation for developers who want to integrate or extend the platform.</p>
            </div>
          </div>

          <div class="flex items-start">
            <div class="flex-shrink-0">
              <font-awesome-icon :icon="['fas', 'check-circle']" class="text-green-500 text-2xl mr-4" />
            </div>
            <div>
              <h3 class="text-lg font-bold text-gray-900 mb-1">Open Source</h3>
              <p class="text-gray-600">Built transparently with community contribution in mind. Check our GitHub repository for the full source code.</p>
            </div>
          </div>

          <div class="flex items-start">
            <div class="flex-shrink-0">
              <font-awesome-icon :icon="['fas', 'check-circle']" class="text-green-500 text-2xl mr-4" />
            </div>
            <div>
              <h3 class="text-lg font-bold text-gray-900 mb-1">No Vendor Lock-In</h3>
              <p class="text-gray-600">Download your PDFs and publish anywhere - Amazon KDP, IngramSpark, Lulu, or any print-on-demand platform.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Team/Creator -->
    <section class="py-20 bg-gray-50">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-3xl font-bold text-gray-900 mb-6">Built with ❤️</h2>
        <p class="text-lg text-gray-600 mb-8">
          BookGen AI was created to solve a real problem: making book publishing accessible to everyone. We're constantly improving the platform based on user feedback and the latest AI advancements.
        </p>
        <div class="flex justify-center space-x-4">
          <a 
            href="https://github.com/BadrRibzat/book-generator" 
            target="_blank"
            class="inline-flex items-center px-6 py-3 border border-gray-300 text-base font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
          >
            <font-awesome-icon :icon="['fas', 'code']" class="mr-2" />
            View on GitHub
          </a>
          <a 
            href="/api/docs/" 
            target="_blank"
            class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
          >
            <font-awesome-icon :icon="['fas', 'book']" class="mr-2" />
            API Documentation
          </a>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="py-20 bg-primary-600">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-3xl font-bold text-white mb-6">
          Join the Future of Book Publishing
        </h2>
        <p class="text-xl text-primary-100 mb-8">
          Start creating professional books with AI today
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
