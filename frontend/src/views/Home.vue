<template>
  <Layout>
    <!-- Hero Section with Glassmorphism -->
    <section class="relative min-h-screen flex items-center justify-center overflow-hidden">
      <!-- Animated Background -->
      <div class="absolute inset-0 bg-gradient-to-br from-primary-50 via-white to-primary-100 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900">
        <div class="absolute inset-0">
          <div class="absolute top-20 left-20 w-72 h-72 bg-primary-200/30 dark:bg-primary-800/20 rounded-full blur-3xl animate-float"></div>
          <div class="absolute bottom-20 right-20 w-96 h-96 bg-secondary-200/20 dark:bg-secondary-800/10 rounded-full blur-3xl animate-float" style="animation-delay: 2s"></div>
          <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-accent-200/25 dark:bg-accent-800/15 rounded-full blur-3xl animate-float" style="animation-delay: 4s"></div>
        </div>
      </div>

      <!-- Glass Hero Card -->
      <div class="relative z-10 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="glass-card p-12 md:p-16 text-center animate-fade-in">
          <div class="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-primary-500 to-primary-600 rounded-2xl mb-8 shadow-neon">
            <font-awesome-icon :icon="['fas', 'brain']" class="text-white text-3xl" />
          </div>

          <h1 class="text-5xl md:text-7xl font-bold mb-6 display-font">
            <span class="text-gradient">AI-Powered</span>
            <br>
            <span class="text-gray-900 dark:text-white">Book Generator</span>
          </h1>

          <p class="text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto leading-relaxed">
            Create professional, market-ready books in minutes with our advanced AI technology.
            Choose from trending 2025 niches and get stunning covers automatically.
          </p>

          <!-- Interactive Stats -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-6 mb-10">
            <div class="glass p-4 rounded-xl border border-white/20">
              <div class="text-3xl font-bold text-primary-600 dark:text-primary-400 mb-1">4</div>
              <div class="text-sm text-gray-600 dark:text-gray-400">Trending Categories</div>
            </div>
            <div class="glass p-4 rounded-xl border border-white/20">
              <div class="text-3xl font-bold text-secondary-600 dark:text-secondary-400 mb-1">32</div>
              <div class="text-sm text-gray-600 dark:text-gray-400">Sub-Niches</div>
            </div>
            <div class="glass p-4 rounded-xl border border-white/20">
              <div class="text-3xl font-bold text-accent-600 dark:text-accent-400 mb-1">3</div>
              <div class="text-sm text-gray-600 dark:text-gray-400">Cover Styles</div>
            </div>
            <div class="glass p-4 rounded-xl border border-white/20">
              <div class="text-3xl font-bold text-green-600 dark:text-green-400 mb-1">AI</div>
              <div class="text-sm text-gray-600 dark:text-gray-400">DeepSeek R1T2</div>
            </div>
          </div>

          <!-- CTA Buttons -->
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <router-link
              to="/auth/signup"
              class="btn-primary inline-flex items-center justify-center group"
            >
              <font-awesome-icon :icon="['fas', 'rocket']" class="mr-2 group-hover:animate-bounce" />
              Start Creating Free
            </router-link>
            <router-link
              to="/features"
              class="btn-secondary inline-flex items-center justify-center"
            >
              <font-awesome-icon :icon="['fas', 'play-circle']" class="mr-2" />
              See How It Works
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section with Interactive Cards -->
    <section class="py-20 bg-gradient-to-b from-white to-slate-50 dark:from-slate-900 dark:to-slate-800">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-4xl md:text-5xl font-bold mb-4 display-font">
            <span class="text-gradient">Everything You Need</span>
          </h2>
          <p class="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Our AI-powered platform handles content generation, cover design, and PDF creation automatically.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <!-- Feature Card 1 -->
          <div class="interactive-card card-modern group">
            <div class="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl flex items-center justify-center mb-6 shadow-lg group-hover:shadow-neon transition-all duration-300">
              <font-awesome-icon :icon="['fas', 'brain']" class="text-white text-2xl" />
            </div>
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">DeepSeek R1T2 AI</h3>
            <p class="text-gray-600 dark:text-gray-300 leading-relaxed">
              Leveraging OpenRouter's most advanced AI model for creating engaging, well-structured content tailored to your chosen niche.
            </p>
            <div class="mt-4 flex items-center text-sm text-primary-600 dark:text-primary-400 font-medium">
              <span>Learn more</span>
              <font-awesome-icon :icon="['fas', 'arrow-right']" class="ml-2 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>

          <!-- Feature Card 2 -->
          <div class="interactive-card card-modern group">
            <div class="w-16 h-16 bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl flex items-center justify-center mb-6 shadow-lg group-hover:shadow-neon transition-all duration-300">
              <font-awesome-icon :icon="['fas', 'palette']" class="text-white text-2xl" />
            </div>
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">AI Cover Design</h3>
            <p class="text-gray-600 dark:text-gray-300 leading-relaxed">
              Choose from 7 modern 2025 design trends automatically generated with niche-specific color schemes and typography.
            </p>
            <div class="mt-4 flex items-center text-sm text-primary-600 dark:text-primary-400 font-medium">
              <span>View styles</span>
              <font-awesome-icon :icon="['fas', 'arrow-right']" class="ml-2 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>

          <!-- Feature Card 3 -->
          <div class="interactive-card card-modern group">
            <div class="w-16 h-16 bg-gradient-to-br from-green-500 to-green-600 rounded-2xl flex items-center justify-center mb-6 shadow-lg group-hover:shadow-neon transition-all duration-300">
              <font-awesome-icon :icon="['fas', 'file-pdf']" class="text-white text-2xl" />
            </div>
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">Print-Ready PDFs</h3>
            <p class="text-gray-600 dark:text-gray-300 leading-relaxed">
              Get perfectly formatted, high-quality PDFs ready for publishing on Amazon KDP, IngramSpark, or print-on-demand platforms.
            </p>
            <div class="mt-4 flex items-center text-sm text-primary-600 dark:text-primary-400 font-medium">
              <span>Download sample</span>
              <font-awesome-icon :icon="['fas', 'arrow-right']" class="ml-2 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Trending Niches Section -->
    <section class="py-20 bg-gradient-to-b from-slate-50 to-white dark:from-slate-800 dark:to-slate-900">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-4xl md:text-5xl font-bold mb-4 display-font">
            <span class="text-gradient">2025 Trending Categories</span>
          </h2>
          <p class="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            We've curated the most profitable and trending book categories aligned with current market demands
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <!-- Category 1: AI & Digital Transformation -->
          <div class="interactive-card card-modern p-6">
            <div class="w-12 h-12 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-xl flex items-center justify-center mb-4">
              <font-awesome-icon :icon="['fas', 'robot']" class="text-white text-xl" />
            </div>
            <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-2">AI & Digital Transformation</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">8 specialized niches covering AI business automation, machine learning, and digital strategy</p>
            <div class="space-y-2">
              <div class="text-xs bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 px-2 py-1 rounded-full inline-block">AI Business Automation</div>
              <div class="text-xs bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 px-2 py-1 rounded-full inline-block">Machine Learning Basics</div>
            </div>
          </div>

          <!-- Category 2: Sustainability & Green Tech -->
          <div class="interactive-card card-modern p-6">
            <div class="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-500 rounded-xl flex items-center justify-center mb-4">
              <font-awesome-icon :icon="['fas', 'leaf']" class="text-white text-xl" />
            </div>
            <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-2">Sustainability & Green Tech</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">8 eco-friendly niches from renewable energy to circular economy principles</p>
            <div class="space-y-2">
              <div class="text-xs bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-300 px-2 py-1 rounded-full inline-block">Renewable Energy</div>
              <div class="text-xs bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-300 px-2 py-1 rounded-full inline-block">Circular Economy</div>
            </div>
          </div>

          <!-- Category 3: Mental Health Tech -->
          <div class="interactive-card card-modern p-6">
            <div class="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center mb-4">
              <font-awesome-icon :icon="['fas', 'heart']" class="text-white text-xl" />
            </div>
            <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-2">Mental Health Technology</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">8 digital wellness niches combining technology with mental health solutions</p>
            <div class="space-y-2">
              <div class="text-xs bg-purple-50 dark:bg-purple-900/20 text-purple-700 dark:text-purple-300 px-2 py-1 rounded-full inline-block">AI Mental Health Apps</div>
              <div class="text-xs bg-purple-50 dark:bg-purple-900/20 text-purple-700 dark:text-purple-300 px-2 py-1 rounded-full inline-block">Digital Wellness Tools</div>
            </div>
          </div>

          <!-- Category 4: Future Skills -->
          <div class="interactive-card card-modern p-6">
            <div class="w-12 h-12 bg-gradient-to-br from-orange-500 to-red-500 rounded-xl flex items-center justify-center mb-4">
              <font-awesome-icon :icon="['fas', 'rocket']" class="text-white text-xl" />
            </div>
            <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-2">Future Skills & Digital Economy</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">8 essential skills for the digital economy including blockchain and metaverse</p>
            <div class="space-y-2">
              <div class="text-xs bg-orange-50 dark:bg-orange-900/20 text-orange-700 dark:text-orange-300 px-2 py-1 rounded-full inline-block">Remote Work Mastery</div>
              <div class="text-xs bg-orange-50 dark:bg-orange-900/20 text-orange-700 dark:text-orange-300 px-2 py-1 rounded-full inline-block">Blockchain Fundamentals</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section class="py-20 bg-gradient-to-b from-white to-slate-50 dark:from-slate-900 dark:to-slate-800">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-4xl md:text-5xl font-bold mb-4 display-font">
            <span class="text-gradient">How It Works</span>
          </h2>
          <p class="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Create your book in just 3 simple steps with real-time progress tracking
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <!-- Step 1 -->
          <div class="text-center group">
            <div class="relative mb-8">
              <div class="w-20 h-20 bg-gradient-to-br from-primary-500 to-primary-600 rounded-2xl flex items-center justify-center mx-auto shadow-lg group-hover:shadow-neon transition-all duration-300 status-bounce">
                <span class="text-2xl font-bold text-white">1</span>
              </div>
              <div class="absolute -top-2 -right-2 w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                <font-awesome-icon :icon="['fas', 'check']" class="text-white text-xs" />
              </div>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">Choose Your Niche</h3>
            <p class="text-gray-600 dark:text-gray-300 leading-relaxed">
              Select from 32 trending sub-niches across 4 major categories spanning technology, wellness, and future skills.
            </p>
          </div>

          <!-- Step 2 -->
          <div class="text-center group">
            <div class="relative mb-8">
              <div class="w-20 h-20 bg-gradient-to-br from-secondary-500 to-secondary-600 rounded-2xl flex items-center justify-center mx-auto shadow-lg group-hover:shadow-neon transition-all duration-300 status-bounce" style="animation-delay: 0.5s">
                <span class="text-2xl font-bold text-white">2</span>
              </div>
              <div class="absolute -top-2 -right-2 w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center animate-pulse">
                <font-awesome-icon :icon="['fas', 'brain']" class="text-white text-xs" />
              </div>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">AI Generates Content</h3>
            <p class="text-gray-600 dark:text-gray-300 leading-relaxed">
              Our DeepSeek R1T2 AI creates compelling content and generates 3 unique cover designs automatically with real-time progress updates.
            </p>
          </div>

          <!-- Step 3 -->
          <div class="text-center group">
            <div class="relative mb-8">
              <div class="w-20 h-20 bg-gradient-to-br from-accent-500 to-accent-600 rounded-2xl flex items-center justify-center mx-auto shadow-lg group-hover:shadow-neon transition-all duration-300 status-bounce" style="animation-delay: 1s">
                <span class="text-2xl font-bold text-white">3</span>
              </div>
              <div class="absolute -top-2 -right-2 w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center">
                <font-awesome-icon :icon="['fas', 'download']" class="text-white text-xs" />
              </div>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">Download & Publish</h3>
            <p class="text-gray-600 dark:text-gray-300 leading-relaxed">
              Select your favorite cover and download a complete PDF ready for publishing on Amazon KDP or any print-on-demand platform.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-20 bg-gradient-to-r from-primary-600 via-primary-700 to-primary-800 relative overflow-hidden">
      <!-- Background Pattern -->
      <div class="absolute inset-0 opacity-10">
        <div class="absolute top-20 right-20 w-64 h-64 bg-white/10 rounded-full blur-3xl animate-float"></div>
        <div class="absolute bottom-20 left-20 w-48 h-48 bg-white/5 rounded-full blur-3xl animate-float" style="animation-delay: 3s"></div>
      </div>

      <div class="relative z-10 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-4xl md:text-5xl font-bold text-white mb-6 display-font">
          Ready to Create Your First AI Book?
        </h2>
        <p class="text-xl text-primary-100 mb-8 leading-relaxed">
          Join thousands of authors using AI to create professional books faster than ever before.
          Start with our free tier and upgrade as you grow.
        </p>

        <!-- Feature Highlights -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
          <div class="glass p-4 rounded-xl">
            <font-awesome-icon :icon="['fas', 'infinity']" class="text-white text-2xl mb-2" />
            <div class="text-white font-semibold">Free Forever Plan</div>
            <div class="text-primary-200 text-sm">Create 1 book per day</div>
          </div>
          <div class="glass p-4 rounded-xl">
            <font-awesome-icon :icon="['fas', 'zap']" class="text-white text-2xl mb-2" />
            <div class="text-white font-semibold">Lightning Fast</div>
            <div class="text-primary-200 text-sm">Books ready in 2-3 minutes</div>
          </div>
          <div class="glass p-4 rounded-xl">
            <font-awesome-icon :icon="['fas', 'crown']" class="text-white text-2xl mb-2" />
            <div class="text-white font-semibold">Pro Features</div>
            <div class="text-primary-200 text-sm">Advanced AI & premium covers</div>
          </div>
        </div>

        <router-link
          to="/auth/signup"
          class="btn-secondary inline-flex items-center justify-center group text-lg px-8 py-4"
        >
          <font-awesome-icon :icon="['fas', 'rocket']" class="mr-3 group-hover:animate-bounce" />
          Get Started Now - It's Free
        </router-link>
      </div>
    </section>
  </Layout>
</template>

<script setup lang="ts">
import Layout from '../components/Layout.vue';
</script>

<style scoped>
/* Glassmorphism Effects */
.glass {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
}

.glass-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
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

.text-gradient {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.shadow-neon {
  box-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
}

.status-bounce {
  animation: status-bounce 2s ease-in-out infinite;
}

@keyframes status-bounce {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

.animate-float {
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

/* Dark mode adjustments */
.dark .glass {
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.dark .glass-card {
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  /* Mobile hero section */
  .relative.overflow-hidden .glass-card {
    margin: 1rem;
    padding: 1.5rem;
  }

  .relative.overflow-hidden .glass-card .flex.items-center.justify-between {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .relative.overflow-hidden .glass-card .flex.items-center.justify-between .flex.items-center.space-x-6 {
    width: 100%;
  }

  .relative.overflow-hidden .glass-card .flex.items-center.justify-between .text-right {
    width: 100%;
    text-align: left;
  }

  /* Mobile features grid */
  .grid.grid-cols-1.md\\:grid-cols-2.lg\\:grid-cols-4 {
    gap: 1rem;
  }

  .grid.grid-cols-1.md\\:grid-cols-2.lg\\:grid-cols-4 .glass-card {
    padding: 1rem;
  }

  .grid.grid-cols-1.md\\:grid-cols-2.lg\\:grid-cols-4 .glass-card .flex.items-center.justify-between {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .grid.grid-cols-1.md\\:grid-cols-2.lg\\:grid-cols-4 .glass-card .flex.items-center.justify-between .w-16.h-16 {
    width: 3rem;
    height: 3rem;
  }

  .grid.grid-cols-1.md\\:grid-cols-2.lg\\:grid-cols-4 .glass-card .flex.items-center.justify-between .w-16.h-16 .text-2xl {
    font-size: 1.25rem;
  }

  /* Mobile how it works section */
  .grid.grid-cols-1.md\\:grid-cols-3 {
    gap: 2rem;
  }

  .grid.grid-cols-1.md\\:grid-cols-3 .text-center.group {
    margin-bottom: 2rem;
  }

  .grid.grid-cols-1.md\\:grid-cols-3 .text-center.group .w-20.h-20 {
    width: 4rem;
    height: 4rem;
  }

  .grid.grid-cols-1.md\\:grid-cols-3 .text-center.group .w-20.h-20 .text-2xl {
    font-size: 1.5rem;
  }

  .grid.grid-cols-1.md\\:grid-cols-3 .text-center.group .text-2xl {
    font-size: 1.5rem;
  }

  /* Mobile CTA section */
  .relative.z-10.max-w-4xl.mx-auto .grid.grid-cols-1.md\\:grid-cols-3 {
    gap: 1rem;
  }

  .relative.z-10.max-w-4xl.mx-auto .grid.grid-cols-1.md\\:grid-cols-3 .glass {
    padding: 1rem;
  }

  .relative.z-10.max-w-4xl.mx-auto .grid.grid-cols-1.md\\:grid-cols-3 .glass .text-2xl {
    font-size: 1.25rem;
  }

  .relative.z-10.max-w-4xl.mx-auto .btn-secondary {
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
  }

  .relative.z-10.max-w-4xl.mx-auto .btn-secondary .mr-3 {
    margin-right: 0.5rem;
  }
}

@media (max-width: 640px) {
  /* Extra small screens */
  .max-w-7xl.mx-auto {
    padding-left: 0.5rem;
    padding-right: 0.5rem;
  }

  .text-6xl {
    font-size: 3rem;
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

  .text-lg {
    font-size: 1rem;
  }

  /* Stack all grids vertically on very small screens */
  .grid.grid-cols-1.md\\:grid-cols-2.lg\\:grid-cols-4 {
    grid-template-columns: 1fr;
  }

  .grid.grid-cols-1.md\\:grid-cols-3 {
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

  .mb-4 {
    margin-bottom: 0.75rem;
  }

  .mb-3 {
    margin-bottom: 0.5rem;
  }

  /* Adjust button sizes */
  .btn-primary {
    padding: 0.75rem 1.5rem;
    font-size: 0.875rem;
  }

  .btn-secondary {
    padding: 0.75rem 1.5rem;
    font-size: 0.875rem;
  }

  /* Prevent zoom on iOS inputs */
  input, select, textarea {
    font-size: 16px;
  }
}
</style>
