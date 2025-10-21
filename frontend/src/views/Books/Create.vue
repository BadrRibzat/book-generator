<template>
  <Layout>
    <div class="max-w-3xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <!-- Page Header -->
        <div class="mb-8 animate-fade-in">
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Create New Book</h1>
          <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
            Select a domain and niche for your book. We'll generate the content using AI.
          </p>
        </div>

        <!-- Progress Indicator -->
        <div v-if="creationProgress.show" class="mb-8 bg-white dark:bg-gray-800 shadow-xl rounded-2xl border border-gray-200 dark:border-gray-700 overflow-hidden animate-slide-up">
          <div class="px-6 py-4 bg-gradient-to-r from-primary-600 to-blue-700 text-white">
            <div class="flex items-center justify-between">
              <h3 class="text-lg font-semibold">Creating Your Book</h3>
              <span class="text-sm">{{ creationProgress.currentStep }} of {{ creationProgress.totalSteps }}</span>
            </div>
          </div>
          <div class="p-6">
            <div class="space-y-4">
              <div v-for="(step, index) in creationProgress.steps" :key="index" class="flex items-center">
                <div class="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center" :class="getStepClass(step.status)">
                  <font-awesome-icon 
                    :icon="['fas', getStepIcon(step.status)]" 
                    :spin="step.status === 'loading'"
                    class="w-4 h-4 text-white" 
                  />
                </div>
                <div class="ml-4 flex-1">
                  <p class="text-sm font-medium text-gray-900 dark:text-white">{{ step.label }}</p>
                  <p v-if="step.description" class="text-xs text-gray-500 dark:text-gray-400">{{ step.description }}</p>
                </div>
              </div>
            </div>
            <div class="mt-6">
              <div class="flex justify-between text-sm text-gray-600 dark:text-gray-400 mb-2">
                <span>Progress</span>
                <span>{{ Math.round((creationProgress.currentStep / creationProgress.totalSteps) * 100) }}%</span>
              </div>
              <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div 
                  class="bg-gradient-to-r from-primary-600 to-blue-700 h-2 rounded-full transition-all duration-500"
                  :style="{ width: `${(creationProgress.currentStep / creationProgress.totalSteps) * 100}%` }"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="flex justify-center items-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          <span class="ml-3 text-gray-600 dark:text-gray-400">Loading content categories...</span>
        </div>

        <!-- Form -->
        <form v-else @submit.prevent="handleSubmit" class="bg-white dark:bg-gray-800 shadow-xl rounded-2xl border border-gray-200 dark:border-gray-700 overflow-hidden animate-slide-up">
          <div class="px-6 py-8 space-y-6">
            <!-- Domain Select -->
            <div class="group">
              <label for="domain" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                <font-awesome-icon :icon="['fas', 'book-open']" class="mr-2 text-primary-600 dark:text-primary-400" />
                Content Category
              </label>
              <select
                id="domain"
                v-model="form.domain"
                @change="handleDomainChange"
                required
                class="mt-1 block w-full pl-4 pr-10 py-3 text-base border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500 dark:focus:ring-primary-400 focus:border-transparent rounded-lg transition-all duration-200"
              >
                <option value="">Select a content category</option>
                <option v-for="domain in availableDomains" :key="domain.value" :value="domain.value">
                  {{ domain.label }}
                </option>
              </select>
              <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">Choose from 15 trending content categories</p>
            </div>

            <!-- Sub-Niche Select -->
            <div v-if="form.domain" class="group animate-fade-in">
              <label for="sub_niche" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                <font-awesome-icon :icon="['fas', 'palette']" class="mr-2 text-primary-600 dark:text-primary-400" />
                Sub-Niche
              </label>
              <select
                id="sub_niche"
                v-model="form.sub_niche"
                required
                class="mt-1 block w-full pl-4 pr-10 py-3 text-base border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500 dark:focus:ring-primary-400 focus:border-transparent rounded-lg transition-all duration-200"
              >
                <option value="">Select a niche</option>
                <option v-for="niche in availableNiches" :key="niche.value" :value="niche.value">
                  {{ niche.label }}
                </option>
              </select>
              <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">Choose a specific niche within the domain</p>
            </div>

            <!-- Page Length Select -->
            <div class="group">
              <label for="page_length" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                <font-awesome-icon :icon="['fas', 'file-pdf']" class="mr-2 text-primary-600 dark:text-primary-400" />
                Page Length
              </label>
              <select
                id="page_length"
                v-model.number="form.page_length"
                required
                class="mt-1 block w-full pl-4 pr-10 py-3 text-base border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500 dark:focus:ring-primary-400 focus:border-transparent rounded-lg transition-all duration-200"
              >
                <option :value="15">15 pages</option>
                <option :value="20">20 pages</option>
                <option :value="25">25 pages</option>
                <option :value="30">30 pages</option>
              </select>
              <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
                <font-awesome-icon :icon="['fas', 'gauge-high']" class="mr-1" />
                More pages = more detailed content (longer generation time)
              </p>
            </div>

            <!-- Info Box -->
            <div class="bg-primary-50 dark:bg-primary-900/20 border border-primary-200 dark:border-primary-800 rounded-lg p-4">
              <div class="flex">
                <div class="flex-shrink-0">
                  <font-awesome-icon :icon="['fas', 'brain']" class="h-5 w-5 text-primary-600 dark:text-primary-400" />
                </div>
                <div class="ml-3">
                  <h3 class="text-sm font-medium text-primary-800 dark:text-primary-300">AI-Powered Generation</h3>
                  <div class="mt-2 text-sm text-primary-700 dark:text-primary-400">
                    <p>Your book will be generated using advanced AI. The process typically takes 2-3 minutes.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Form Actions -->
          <div class="bg-gray-50 dark:bg-gray-700/50 px-6 py-4 flex flex-col-reverse sm:flex-row sm:justify-end gap-3 border-t border-gray-200 dark:border-gray-700">
            <router-link
              to="/profile/books"
              class="inline-flex justify-center items-center px-6 py-2.5 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-lg text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 transition-all duration-200"
            >
              Cancel
            </router-link>
            <button
              type="submit"
              :disabled="booksStore.loading || !form.domain || !form.sub_niche"
              class="inline-flex justify-center items-center px-6 py-2.5 border border-transparent text-sm font-medium rounded-lg text-white bg-gradient-to-r from-primary-600 to-primary-700 hover:from-primary-700 hover:to-primary-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-[1.02] active:scale-[0.98] transition-all duration-200 shadow-lg hover:shadow-xl"
            >
              <span v-if="!booksStore.loading" class="flex items-center">
                <font-awesome-icon :icon="['fas', 'rocket']" class="mr-2" />
                Create Book
              </span>
              <span v-else class="flex items-center">
                <font-awesome-icon :icon="['fas', 'spinner']" spin class="mr-2" />
                Creating...
              </span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </Layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useBooksStore } from '../../stores/books';
import Layout from '../../components/Layout.vue';
import apiClient from '../../services/api';

const router = useRouter();
const booksStore = useBooksStore();

const form = ref({
  domain: '',
  sub_niche: '',
  page_length: 20,
});

const configData = ref<any>({});
const loading = ref(true);
const error = ref<string | null>(null);

// Progress tracking
const creationProgress = ref({
  show: false,
  currentStep: 0,
  totalSteps: 4,
  steps: [
    { label: 'Initializing book creation', description: 'Setting up your book parameters', status: 'pending' },
    { label: 'Generating AI content', description: 'Creating professional content with AI', status: 'pending' },
    { label: 'Designing covers', description: 'Generating 3 unique cover options', status: 'pending' },
    { label: 'Finalizing book', description: 'Preparing your book for download', status: 'pending' }
  ]
});

// Available domains (15 trending categories)
const availableDomains = computed(() => {
  if (!configData.value.sub_niches) return [];
  
  return Object.keys(configData.value.sub_niches).map(key => ({
    value: key,
    label: configData.value.sub_niches[key].name || key.replace(/_/g, ' ')
  }));
});

// Available niches for selected domain
const availableNiches = computed(() => {
  if (!form.value.domain || !configData.value.sub_niches) return [];
  
  const domain = configData.value.sub_niches[form.value.domain];
  if (!domain || !domain.sub_niches) return [];
  
  return Object.keys(domain.sub_niches).map(key => ({
    value: key,
    label: domain.sub_niches[key].name || key.replace(/_/g, ' ')
  }));
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

const handleDomainChange = () => {
  form.value.sub_niche = '';
};

const handleSubmit = async () => {
  booksStore.clearError();
  
  // Show progress indicator
  creationProgress.value.show = true;
  creationProgress.value.currentStep = 1;
  if (creationProgress.value.steps[0]) {
    creationProgress.value.steps[0].status = 'loading';
  }
  
  try {
    const result = await booksStore.createBook(form.value as any);
    
    if (result.success && result.data) {
      // Update progress as we navigate to the book details page
      if (creationProgress.value.steps[0]) creationProgress.value.steps[0].status = 'completed';
      creationProgress.value.currentStep = 2;
      if (creationProgress.value.steps[1]) creationProgress.value.steps[1].status = 'loading';
      
      router.push(`/profile/books/${result.data.id}`);
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
  });
};

const getStepClass = (status: string) => {
  switch (status) {
    case 'completed': return 'bg-green-500';
    case 'loading': return 'bg-blue-500';
    case 'error': return 'bg-red-500';
    default: return 'bg-gray-300';
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

// Lifecycle
onMounted(async () => {
  await fetchConfig();
});
</script>
