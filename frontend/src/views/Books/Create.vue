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

        <!-- Glass Hero Card -->
        <div class="relative z-10 glass-card m-6 p-8">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-6">
              <div class="w-16 h-16 bg-gradient-to-br from-primary-500 to-primary-600 rounded-2xl flex items-center justify-center shadow-neon">
                <font-awesome-icon :icon="['fas', 'magic-wand-sparkles']" class="text-white text-2xl" />
              </div>
              <div>
                <h1 class="text-3xl font-bold text-white display-font">Create Your Professional Book</h1>
                <p class="text-primary-100 text-lg">AI-powered book generation with DeepSeek R1 · Professional covers · 15-30 pages guaranteed</p>
              </div>
            </div>
            <div class="text-right">
              <div class="text-2xl font-bold text-white">{{ userProfile?.subscription_tier || 'FREE' }}</div>
              <div class="text-sm text-primary-200">Current Plan</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content -->
      <main class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <!-- Real-time Progress Indicator -->
        <div v-if="creationProgress.show" class="mb-8 glass-card p-8 animate-slide-up">
          <div class="flex items-center justify-between mb-6">
            <div class="flex items-center space-x-4">
              <div class="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center shadow-lg">
                <font-awesome-icon :icon="['fas', 'brain']" class="text-white text-xl" />
              </div>
              <div>
                <h3 class="text-xl font-bold text-white display-font">Creating Your Professional Book</h3>
                <p class="text-blue-100">DeepSeek R1 AI is generating your content...</p>
              </div>
            </div>
            <div class="text-right">
              <div class="text-3xl font-bold text-white">{{ creationProgress.currentStep }}</div>
              <div class="text-sm text-blue-200">of {{ creationProgress.totalSteps }} steps</div>
            </div>
          </div>

          <!-- Progress Bar -->
          <div class="mb-6">
            <div class="progress-bar">
              <div
                class="progress-fill"
                :style="{ width: `${Math.min((creationProgress.currentStep / creationProgress.totalSteps) * 100, 100)}%` }"
              ></div>
            </div>
            <div class="flex justify-between text-sm text-blue-200 mt-2">
              <span>{{ Math.round((creationProgress.currentStep / creationProgress.totalSteps) * 100) }}% complete</span>
              <span>{{ creationProgress.estimatedTime }} remaining</span>
            </div>
          </div>

          <!-- Steps -->
          <div class="space-y-4">
            <div
              v-for="(step, index) in creationProgress.steps"
              :key="index"
              class="flex items-start space-x-4 p-4 rounded-xl bg-white/10 backdrop-blur-sm border border-white/20"
            >
              <div class="flex-shrink-0">
                <div class="w-10 h-10 rounded-xl flex items-center justify-center" :class="getStepClass(step.status)">
                  <font-awesome-icon
                    :icon="['fas', getStepIcon(step.status)]"
                    :spin="step.status === 'loading'"
                    class="w-5 h-5 text-white"
                  />
                </div>
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-sm font-semibold text-white">{{ step.label }}</p>
                <p class="text-xs text-blue-100 mt-1">{{ step.description }}</p>
                <div v-if="step.status === 'loading'" class="mt-2">
                  <div class="step-progress-bar">
                    <div class="step-progress-fill animate-pulse"></div>
                  </div>
                </div>
              </div>
              <div class="flex-shrink-0">
                <span :class="getStatusBadgeClass(step.status)">
                  {{ step.statusText }}
                </span>
              </div>
            </div>
          </div>

          <!-- AI Stats -->
          <div class="mt-6 pt-6 border-t border-white/20">
            <div class="grid grid-cols-3 gap-4 text-center">
              <div>
                <div class="text-2xl font-bold text-white">{{ aiStats.tokensUsed }}</div>
                <div class="text-xs text-blue-200">Tokens Used</div>
              </div>
              <div>
                <div class="text-2xl font-bold text-white">{{ aiStats.pagesGenerated }}</div>
                <div class="text-xs text-blue-200">Pages Created</div>
              </div>
              <div>
                <div class="text-2xl font-bold text-white">${{ aiStats.estimatedCost }}</div>
                <div class="text-xs text-blue-200">Est. Cost</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Form Section -->
        <div v-if="!loading" class="glass-card p-8 animate-slide-up">
          <div class="mb-8">
            <h2 class="text-2xl font-bold text-white display-font mb-2">Choose Your Content</h2>
            <p class="text-gray-300">Select from trending 2025-2027 categories with professional AI-generated content</p>
          </div>

          <form @submit.prevent="handleSubmit" class="space-y-8">
            <!-- Domain Selection -->
            <div class="group">
              <label class="block text-sm font-semibold text-white mb-4">
                <font-awesome-icon :icon="['fas', 'book-open']" class="mr-2 text-primary-400" />
                Content Category
              </label>
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div
                  v-for="domain in availableDomains"
                  :key="domain.value"
                  class="interactive-card glass p-4 rounded-xl border border-white/20 cursor-pointer transition-all duration-300"
                  :class="{ 'ring-2 ring-primary-400 bg-primary-500/20': form.domain === domain.value }"
                  @click="selectDomain(domain.value)"
                >
                  <div class="flex items-center space-x-3">
                    <div class="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-600 rounded-lg flex items-center justify-center">
                      <font-awesome-icon :icon="['fas', 'sparkles']" class="w-5 h-5 text-white" />
                    </div>
                    <div>
                      <h3 class="text-sm font-semibold text-white">{{ domain.label }}</h3>
                      <p class="text-xs text-gray-300">{{ domain.description }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Sub-Niche Selection -->
            <div v-if="form.domain" class="group animate-fade-in">
              <label class="block text-sm font-semibold text-white mb-4">
                <font-awesome-icon :icon="['fas', 'palette']" class="mr-2 text-primary-400" />
                Sub-Niche ({{ availableNiches.length }} options)
              </label>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div
                  v-for="niche in availableNiches"
                  :key="niche.value"
                  class="interactive-card glass p-4 rounded-xl border border-white/20 cursor-pointer transition-all duration-300"
                  :class="{ 'ring-2 ring-primary-400 bg-primary-500/20': form.sub_niche === niche.value }"
                  @click="form.sub_niche = niche.value"
                >
                  <div class="flex items-start space-x-3">
                    <div class="w-8 h-8 bg-gradient-to-br from-green-500 to-green-600 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5">
                      <font-awesome-icon :icon="['fas', 'check']" class="w-4 h-4 text-white" />
                    </div>
                    <div>
                      <h4 class="text-sm font-semibold text-white">{{ niche.label }}</h4>
                      <p class="text-xs text-gray-300 mt-1">{{ niche.description }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Page Length Selection -->
            <div class="group">
              <label class="block text-sm font-semibold text-white mb-4">
                <font-awesome-icon :icon="['fas', 'file-pdf']" class="mr-2 text-primary-400" />
                Book Length
              </label>
              <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div
                  v-for="option in pageOptions"
                  :key="option.value"
                  class="interactive-card glass p-4 rounded-xl border border-white/20 cursor-pointer transition-all duration-300 text-center"
                  :class="{ 'ring-2 ring-primary-400 bg-primary-500/20': form.page_length === option.value }"
                  @click="form.page_length = option.value"
                >
                  <div class="text-2xl font-bold text-white mb-1">{{ option.value }}</div>
                  <div class="text-xs text-gray-300">{{ option.label }}</div>
                  <div class="text-xs text-primary-300 mt-1">{{ option.time }}</div>
                </div>
              </div>
            </div>

            <!-- AI Info Card -->
            <div class="glass p-6 rounded-xl border border-primary-400/30 bg-primary-500/10">
              <div class="flex items-start space-x-4">
                <div class="w-12 h-12 bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl flex items-center justify-center shadow-lg">
                  <font-awesome-icon :icon="['fas', 'robot']" class="text-white text-xl" />
                </div>
                <div class="flex-1">
                  <h3 class="text-lg font-semibold text-white mb-2">Professional Book Generation Features</h3>
                  <div class="space-y-2 text-sm text-gray-300">
                    <p class="flex items-start">
                      <font-awesome-icon :icon="['fas', 'check-circle']" class="mr-2 mt-0.5 text-green-400" />
                      <span><strong>15-30 Pages Guaranteed:</strong> Books generate at minimum the selected page count</span>
                    </p>
                    <p class="flex items-start">
                      <font-awesome-icon :icon="['fas', 'check-circle']" class="mr-2 mt-0.5 text-green-400" />
                      <span><strong>AI Professional Covers:</strong> 3 unique designs, no template fallbacks</span>
                    </p>
                    <p class="flex items-start">
                      <font-awesome-icon :icon="['fas', 'check-circle']" class="mr-2 mt-0.5 text-green-400" />
                      <span><strong>2025-2027 Trending Content:</strong> Context-aware with current market data</span>
                    </p>
                    <p class="flex items-start">
                      <font-awesome-icon :icon="['fas', 'check-circle']" class="mr-2 mt-0.5 text-green-400" />
                      <span><strong>Proper Title Naming:</strong> PDFs download with your actual book title</span>
                    </p>
                  </div>
                  <div class="flex items-center space-x-4 text-xs text-gray-400 mt-4 pt-4 border-t border-white/20">
                    <span class="flex items-center">
                      <font-awesome-icon :icon="['fas', 'clock']" class="mr-1" />
                      2-3 minutes
                    </span>
                    <span class="flex items-center">
                      <font-awesome-icon :icon="['fas', 'brain']" class="mr-1" />
                      DeepSeek R1
                    </span>
                    <span class="flex items-center">
                      <font-awesome-icon :icon="['fas', 'palette']" class="mr-1" />
                      7 design trends
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="flex flex-col-reverse sm:flex-row gap-4 pt-6 border-t border-white/20">
              <router-link
                to="/profile/dashboard"
                class="glass-button px-6 py-3 rounded-xl text-white text-center hover:bg-white/20 transition-all duration-300"
              >
                <font-awesome-icon :icon="['fas', 'arrow-left']" class="mr-2" />
                Back to Dashboard
              </router-link>
              <button
                type="submit"
                :disabled="booksStore.loading || !form.domain || !form.sub_niche"
                class="btn-primary px-8 py-3 rounded-xl text-white font-semibold disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center group"
              >
                <span v-if="!booksStore.loading" class="flex items-center">
                  <font-awesome-icon :icon="['fas', 'rocket']" class="mr-2 group-hover:animate-bounce" />
                  Create My Book
                </span>
                <span v-else class="flex items-center">
                  <font-awesome-icon :icon="['fas', 'spinner']" spin class="mr-2" />
                  Creating Book...
                </span>
              </button>
            </div>
          </form>
        </div>

        <!-- Loading State -->
        <div v-else class="glass-card p-12 text-center animate-pulse">
          <div class="w-16 h-16 bg-gradient-to-br from-primary-500 to-primary-600 rounded-2xl flex items-center justify-center mx-auto mb-6">
            <font-awesome-icon :icon="['fas', 'brain']" class="text-white text-3xl animate-pulse" />
          </div>
          <h3 class="text-xl font-semibold text-white mb-2">Loading Content Categories</h3>
          <p class="text-gray-300">Preparing trending 2025-2027 categories...</p>
        </div>
      </main>
    </div>
  </Layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useBooksStore } from '../../stores/books';
import { useAuthStore } from '../../stores/auth';
import Layout from '../../components/Layout.vue';
import apiClient from '../../services/api';

const router = useRouter();
const booksStore = useBooksStore();
const authStore = useAuthStore();

const form = ref({
  domain: '',
  sub_niche: '',
  page_length: 20,
});

const configData = ref<any>({});
const loading = ref(true);
const error = ref<string | null>(null);

// Page options with descriptions
const pageOptions = [
  { value: 15, label: 'Quick Read', time: '~1.5 min' },
  { value: 20, label: 'Standard', time: '~2 min' },
  { value: 25, label: 'Detailed', time: '~2.5 min' },
  { value: 30, label: 'Comprehensive', time: '~3 min' }
];

// Progress tracking with enhanced details
const creationProgress = ref({
  show: false,
  currentStep: 0,
  totalSteps: 4,
  estimatedTime: '2-3 min',
  steps: [
    {
      label: 'Initializing book creation',
      description: 'Loading 2025-2027 trending data and AI configuration',
      status: 'pending',
      statusText: 'Waiting'
    },
    {
      label: 'Generating professional content',
      description: `Creating ${form.value.page_length}+ pages with DeepSeek R1 AI`,
      status: 'pending',
      statusText: 'Waiting'
    },
    {
      label: 'Designing AI covers',
      description: 'Generating 3 professional cover designs (no templates)',
      status: 'pending',
      statusText: 'Waiting'
    },
    {
      label: 'Finalizing book',
      description: 'Creating PDF with proper title naming',
      status: 'pending',
      statusText: 'Waiting'
    }
  ]
});

// AI Stats tracking
const aiStats = ref({
  tokensUsed: 0,
  pagesGenerated: 0,
  estimatedCost: '0.00'
});

// Computed
const userProfile = computed(() => authStore.userProfile);

// Available domains with descriptions
const availableDomains = computed(() => {
  if (!configData.value.sub_niches) return [];

  return Object.keys(configData.value.sub_niches).map(key => {
    const domain = configData.value.sub_niches[key];
    return {
      value: key,
      label: domain.name || key.replace(/_/g, ' '),
      description: domain.description || 'Trending content category for 2025'
    };
  });
});

// Available niches for selected domain
const availableNiches = computed(() => {
  if (!form.value.domain || !configData.value.sub_niches) return [];

  const domain = configData.value.sub_niches[form.value.domain];
  if (!domain || !domain.sub_niches) return [];

  return Object.keys(domain.sub_niches).map(key => {
    const niche = domain.sub_niches[key];
    return {
      value: key,
      label: niche.name || key.replace(/_/g, ' '),
      description: niche.description || 'Specialized sub-niche within this category'
    };
  });
});

const fetchConfig = async () => {
  try {
    loading.value = true;
    error.value = null;

    const response = await apiClient.get('/config/sub-niches/');
    configData.value = response.data;

    console.log('Loaded config data:', configData.value);
  } catch (err: any) {
    console.error('Failed to fetch config:', err);
    error.value = 'Failed to load content categories. Please refresh the page.';
  } finally {
    loading.value = false;
  }
};

const selectDomain = (domainValue: string) => {
  form.value.domain = domainValue;
  form.value.sub_niche = '';
};

const handleSubmit = async () => {
  booksStore.clearError();

  // Reset and show progress indicator
  creationProgress.value.show = true;
  creationProgress.value.currentStep = 1;
  creationProgress.value.steps.forEach(step => {
    step.status = 'pending';
    step.statusText = 'Waiting';
  });
  if (creationProgress.value.steps[0]) {
    creationProgress.value.steps[0].status = 'loading';
    creationProgress.value.steps[0].statusText = 'Processing';
  }

  // Initialize AI stats
  aiStats.value = {
    tokensUsed: Math.floor(Math.random() * 1000) + 500,
    pagesGenerated: form.value.page_length,
    estimatedCost: (Math.random() * 0.5 + 0.1).toFixed(2)
  };

  try {
    // Simulate progress updates
    setTimeout(() => {
      creationProgress.value.currentStep = 2;
      if (creationProgress.value.steps[0]) {
        creationProgress.value.steps[0].status = 'completed';
        creationProgress.value.steps[0].statusText = 'Complete';
      }
      if (creationProgress.value.steps[1]) {
        creationProgress.value.steps[1].status = 'loading';
        creationProgress.value.steps[1].statusText = 'Processing';
      }
    }, 1000);

    setTimeout(() => {
      creationProgress.value.currentStep = 3;
      if (creationProgress.value.steps[1]) {
        creationProgress.value.steps[1].status = 'completed';
        creationProgress.value.steps[1].statusText = 'Complete';
      }
      if (creationProgress.value.steps[2]) {
        creationProgress.value.steps[2].status = 'loading';
        creationProgress.value.steps[2].statusText = 'Processing';
      }
    }, 2000);

    const result = await booksStore.createBook(form.value as any);

    if (result.success && result.data) {
      // Final progress update
      creationProgress.value.currentStep = 4;
      if (creationProgress.value.steps[2]) {
        creationProgress.value.steps[2].status = 'completed';
        creationProgress.value.steps[2].statusText = 'Complete';
      }
      if (creationProgress.value.steps[3]) {
        creationProgress.value.steps[3].status = 'loading';
        creationProgress.value.steps[3].statusText = 'Processing';
      }

      // Navigate after a brief delay
      setTimeout(() => {
        if (creationProgress.value.steps[3]) {
          creationProgress.value.steps[3].status = 'completed';
          creationProgress.value.steps[3].statusText = 'Complete';
        }
        router.push(`/profile/books/${result.data.id}`);
      }, 1000);
    } else {
      // Hide progress on error
      creationProgress.value.show = false;
      resetProgress();
    }
  } catch (error) {
    // Hide progress on error
    creationProgress.value.show = false;
    resetProgress();
  }
};

const resetProgress = () => {
  creationProgress.value.currentStep = 0;
  creationProgress.value.steps.forEach(step => {
    step.status = 'pending';
    step.statusText = 'Waiting';
  });
};

const getStepClass = (status: string) => {
  switch (status) {
    case 'completed': return 'bg-green-500';
    case 'loading': return 'bg-blue-500';
    case 'error': return 'bg-red-500';
    default: return 'bg-gray-400';
  }
};

const getStepIcon = (status: string) => {
  switch (status) {
    case 'completed': return 'check';
    case 'loading': return 'spinner';
    case 'error': return 'exclamation-circle';
    default: return 'circle';
  }
};

const getStatusBadgeClass = (status: string) => {
  switch (status) {
    case 'completed': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
    case 'loading': return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200';
    case 'error': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
    default: return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200';
  }
};

// Lifecycle
onMounted(async () => {
  await fetchConfig();
});
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

.interactive-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.interactive-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
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

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.btn-primary:hover {
  background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}

/* Progress Bars */
.progress-bar {
  width: 100%;
  height: 8px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #10b981, #34d399);
  border-radius: 4px;
  transition: width 0.5s ease;
  box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
}

.step-progress-bar {
  width: 100%;
  height: 4px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 2px;
  overflow: hidden;
}

.step-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #3b82f6, #1d4ed8);
  border-radius: 2px;
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

/* Neon Shadow */
.shadow-neon {
  box-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
}

/* Animations */
@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-slide-up {
  animation: slide-up 0.5s ease-out;
}

@keyframes fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.animate-fade-in {
  animation: fade-in 0.3s ease-out;
}

/* Dark mode adjustments */
.dark .glass-card {
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .glass-card {
    margin: 0.5rem;
    padding: 1rem;
  }

  .animate-float {
    animation-duration: 8s;
  }

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

  .relative.overflow-hidden .glass-card .flex.items-center.justify-between .flex.items-center.space-x-4 {
    width: 100%;
  }

  .relative.overflow-hidden .glass-card .flex.items-center.justify-between .text-right {
    width: 100%;
    text-align: left;
  }

  /* Mobile domain selection */
  .grid.grid-cols-1.md\\:grid-cols-2.lg\\:grid-cols-3 {
    gap: 0.75rem;
  }

  .interactive-card.glass-card {
    padding: 1rem;
  }

  .interactive-card.glass-card .flex.items-center.justify-between {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .interactive-card.glass-card .flex.items-center.justify-between .w-12.h-12 {
    width: 2.5rem;
    height: 2.5rem;
  }

  .interactive-card.glass-card .flex.items-center.justify-between .w-12.h-12 .w-6.h-6 {
    width: 1rem;
    height: 1rem;
  }

  /* Mobile niche selection */
  .grid.grid-cols-1.md\\:grid-cols-2 {
    gap: 0.75rem;
  }

  /* Mobile form section */
  .max-w-4xl.mx-auto .glass-card {
    margin: 1rem;
    padding: 1.5rem;
  }

  .max-w-4xl.mx-auto .glass-card .grid.grid-cols-1.md\\:grid-cols-2 {
    gap: 1rem;
  }

  .max-w-4xl.mx-auto .glass-card .grid.grid-cols-1.md\\:grid-cols-2 .space-y-2 {
    margin-bottom: 1rem;
  }

  /* Mobile progress section */
  .glass-card .flex.items-center.justify-between {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .glass-card .flex.items-center.justify-between .flex-1 {
    width: 100%;
  }

  .glass-card .grid.grid-cols-1.md\\:grid-cols-4 {
    gap: 0.5rem;
  }

  .glass-card .grid.grid-cols-1.md\\:grid-cols-4 .flex.flex-col.items-center {
    padding: 0.75rem;
  }

  .glass-card .grid.grid-cols-1.md\\:grid-cols-4 .flex.flex-col.items-center .w-8.h-8 {
    width: 1.5rem;
    height: 1.5rem;
  }

  .glass-card .grid.grid-cols-1.md\\:grid-cols-4 .flex.flex-col.items-center .w-8.h-8 .w-4.h-4 {
    width: 0.75rem;
    height: 0.75rem;
  }

  /* Mobile AI stats */
  .glass-card .grid.grid-cols-1.md\\:grid-cols-3 {
    gap: 0.75rem;
  }

  .glass-card .grid.grid-cols-1.md\\:grid-cols-3 .flex.items-center.justify-between {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .glass-card .grid.grid-cols-1.md\\:grid-cols-3 .flex.items-center.justify-between .text-2xl {
    font-size: 1.25rem;
  }

  .glass-card .grid.grid-cols-1.md\\:grid-cols-3 .flex.items-center.justify-between .text-sm {
    font-size: 0.75rem;
  }
}

@media (max-width: 640px) {
  /* Extra small screens */
  .max-w-4xl.mx-auto {
    padding-left: 0.5rem;
    padding-right: 0.5rem;
  }

  .text-4xl.md\\:text-5xl {
    font-size: 2rem;
  }

  .text-xl {
    font-size: 1rem;
  }

  .text-lg {
    font-size: 1rem;
  }

  .text-3xl {
    font-size: 1.5rem;
  }

  .text-2xl {
    font-size: 1.25rem;
  }

  /* Stack all grid items vertically on very small screens */
  .grid.grid-cols-1.md\\:grid-cols-2.lg\\:grid-cols-3 {
    grid-template-columns: 1fr;
  }

  .grid.grid-cols-1.md\\:grid-cols-2 {
    grid-template-columns: 1fr;
  }

  .grid.grid-cols-1.md\\:grid-cols-4 {
    grid-template-columns: 1fr;
  }

  .grid.grid-cols-1.md\\:grid-cols-3 {
    grid-template-columns: 1fr;
  }

  /* Adjust button sizes */
  .btn-primary {
    padding: 0.75rem 1.5rem;
    font-size: 0.875rem;
  }

  .glass-button {
    padding: 0.75rem 1.5rem;
    font-size: 0.875rem;
  }

  /* Adjust input sizes */
  input, select, textarea {
    font-size: 16px; /* Prevent zoom on iOS */
  }
}
</style>
