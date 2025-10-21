<template>
  <Layout>
    <div class="min-h-screen bg-gradient-to-br from-primary-50 via-white to-blue-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-4xl mx-auto">
        <!-- Header -->
        <div class="text-center mb-12 animate-fade-in">
          <div class="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-primary-500 via-primary-600 to-blue-700 rounded-3xl mb-6 shadow-2xl shadow-primary-500/25">
            <font-awesome-icon :icon="['fas', 'magic']" class="h-10 w-10 text-white" />
          </div>
          <h1 class="text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-gray-900 via-primary-800 to-blue-800 dark:from-white dark:via-primary-200 dark:to-blue-200 mb-4">
            Create Your AI-Powered Book
          </h1>
          <p class="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto leading-relaxed">
            Transform your ideas into professional books with our advanced AI technology. Choose from trending niches and watch your content come to life.
          </p>
        </div>

        <!-- Progress Steps -->
        <!-- Progress Steps -->
        <div class="mb-12">
          <div class="flex items-center justify-between max-w-4xl mx-auto">
            <div v-for="(step, index) in steps" :key="index" class="flex-1">
              <div class="flex items-center" :class="index < steps.length - 1 ? 'mr-4' : ''">
                <div class="flex flex-col items-center flex-1">
                  <div 
                    class="w-12 h-12 rounded-full flex items-center justify-center font-bold transition-all duration-500 shadow-lg"
                    :class="currentStep > index ? 'bg-gradient-to-r from-green-500 to-emerald-600 text-white shadow-green-500/25' : currentStep === index ? 'bg-gradient-to-r from-primary-600 to-blue-700 text-white shadow-primary-500/25 ring-4 ring-primary-200 dark:ring-primary-900 animate-pulse' : 'bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-400 shadow-gray-200 dark:shadow-gray-800'"
                  >
                    <font-awesome-icon v-if="currentStep > index" :icon="['fas', 'check']" class="h-6 w-6" />
                    <span v-else class="text-lg">{{ index + 1 }}</span>
                  </div>
                  <span class="text-sm mt-3 font-semibold" :class="currentStep >= index ? 'text-gray-900 dark:text-white' : 'text-gray-500 dark:text-gray-400'">
                    {{ step }}
                  </span>
                </div>
                <div v-if="index < steps.length - 1" class="flex-1 h-1 mx-4 mt-[-20px]" :class="currentStep > index ? 'bg-gradient-to-r from-green-500 to-emerald-600' : 'bg-gray-300 dark:bg-gray-700'"></div>
              </div>
            </div>
          </div>
        </div>        <!-- Error Message -->
        <div v-if="error" class="rounded-lg bg-red-50 dark:bg-red-900/20 p-4 mb-6 border border-red-200 dark:border-red-800 animate-scale-in">
          <div class="flex">
            <font-awesome-icon :icon="['fas', 'exclamation-circle']" class="h-5 w-5 text-red-400 mt-0.5" />
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800 dark:text-red-300">{{ error }}</h3>
            </div>
          </div>
        </div>

        <!-- Form Card -->
        <div class="bg-white dark:bg-gray-800 shadow-2xl rounded-3xl overflow-hidden border border-gray-200 dark:border-gray-700 backdrop-blur-sm bg-white/80 dark:bg-gray-800/80 animate-slide-up">
          <form @submit.prevent="handleNext">
            <div class="p-10 sm:p-12">
              
              <!-- Step 1: Choose Domain -->
              <div v-show="currentStep === 0" class="space-y-6 animate-fade-in">
                <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                  <font-awesome-icon :icon="['fas', 'compass']" class="mr-3 text-primary-600 dark:text-primary-400" />
                  Choose Your Book Domain
                </h2>
                
                <p class="text-gray-600 dark:text-gray-400 mb-6">
                  Select the main category that best fits your book concept. We've curated 5 trending domains with proven market demand.
                </p>

                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  <label
                    v-for="domain in domains"
                    :key="domain.value"
                    class="group relative flex cursor-pointer rounded-2xl border-2 p-6 shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 backdrop-blur-sm"
                    :class="form.domain === domain.value ? 'border-primary-500 ring-2 ring-primary-500 bg-gradient-to-br from-primary-50 to-blue-50 dark:from-primary-900/20 dark:to-blue-900/20 shadow-primary-500/25' : 'border-gray-200 dark:border-gray-600 hover:border-primary-300 dark:hover:border-primary-700 bg-white/50 dark:bg-gray-800/50'"
                  >
                    <input
                      type="radio"
                      name="domain"
                      :value="domain.value"
                      v-model="form.domain"
                      class="sr-only"
                    />
                    <div class="flex flex-1 items-center">
                      <div class="flex-shrink-0 mr-4">
                        <div class="w-12 h-12 rounded-xl flex items-center justify-center transition-all duration-300" :class="form.domain === domain.value ? 'bg-primary-600 text-white shadow-lg' : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 group-hover:bg-primary-100 dark:group-hover:bg-primary-900/50'">
                          <font-awesome-icon :icon="['fas', domainIcons[domain.value] || 'book']" class="h-6 w-6" />
                        </div>
                      </div>
                      <div class="flex flex-col">
                        <span class="block text-sm font-bold mb-1" :class="form.domain === domain.value ? 'text-primary-900 dark:text-primary-100' : 'text-gray-900 dark:text-white'">
                          {{ domain.label }}
                        </span>
                        <span class="text-xs text-gray-500 dark:text-gray-400">
                          {{ getDomainDescription(domain.value) }}
                        </span>
                      </div>
                    </div>
                    <font-awesome-icon
                      v-if="form.domain === domain.value"
                      :icon="['fas', 'check-circle']"
                      class="h-6 w-6 text-primary-600 dark:text-primary-400 absolute top-4 right-4 transition-all duration-300 animate-scale-in"
                    />
                  </label>
                </div>
              </div>

              <!-- Step 2: Choose Sub-Niche -->
              <div v-show="currentStep === 1" class="space-y-6 animate-fade-in">
                <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                  <font-awesome-icon :icon="['fas', 'bullseye']" class="mr-3 text-primary-600 dark:text-primary-400" />
                  Select Your Specific Niche
                </h2>
                
                <p class="text-gray-600 dark:text-gray-400 mb-6">
                  Choose a specific sub-niche within <strong>{{ getDomainLabel(form.domain) }}</strong>. Each niche is carefully selected based on market trends and audience demand.
                </p>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <label
                    v-for="niche in availableNiches"
                    :key="niche.value"
                    class="group relative flex cursor-pointer rounded-xl border-2 p-5 shadow-md hover:shadow-lg transition-all duration-300 hover:scale-102 backdrop-blur-sm"
                    :class="form.sub_niche === niche.value ? 'border-primary-500 ring-2 ring-primary-500 bg-gradient-to-r from-primary-50 to-blue-50 dark:from-primary-900/20 dark:to-blue-900/20 shadow-primary-500/25' : 'border-gray-200 dark:border-gray-600 hover:border-primary-300 dark:hover:border-primary-700 bg-white/50 dark:bg-gray-800/50'"
                  >
                    <input
                      type="radio"
                      name="sub_niche"
                      :value="niche.value"
                      v-model="form.sub_niche"
                      class="sr-only"
                    />
                    <div class="flex flex-1 items-center">
                      <div class="flex-shrink-0 mr-4">
                        <div class="w-10 h-10 rounded-lg flex items-center justify-center transition-all duration-300" :class="form.sub_niche === niche.value ? 'bg-primary-600 text-white shadow-lg' : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 group-hover:bg-primary-100 dark:group-hover:bg-primary-900/50'">
                          <font-awesome-icon :icon="['fas', 'star']" class="h-5 w-5" />
                        </div>
                      </div>
                      <span class="block text-sm font-semibold" :class="form.sub_niche === niche.value ? 'text-primary-900 dark:text-primary-100' : 'text-gray-900 dark:text-white'">
                        {{ niche.label }}
                      </span>
                    </div>
                    <font-awesome-icon
                      v-if="form.sub_niche === niche.value"
                      :icon="['fas', 'check-circle']"
                      class="h-5 w-5 text-primary-600 dark:text-primary-400 absolute top-4 right-4 transition-all duration-300 animate-scale-in"
                    />
                  </label>
                </div>
              </div>

              <!-- Step 3: Choose Page Length -->
              <div v-show="currentStep === 2" class="space-y-6 animate-fade-in">
                <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                  <font-awesome-icon :icon="['fas', 'file-pdf']" class="mr-3 text-primary-600 dark:text-primary-400" />
                  Choose Your Book Length
                </h2>
                
                <p class="text-gray-600 dark:text-gray-400 mb-6">
                  Select how many pages you want your book to have. More pages mean more detailed content, but will take longer to generate.
                </p>

                <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
                  <label
                    v-for="length in pageLengths"
                    :key="length"
                    class="group relative flex cursor-pointer rounded-2xl border-2 p-6 shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 flex-col items-center backdrop-blur-sm"
                    :class="form.page_length === length ? 'border-primary-500 ring-2 ring-primary-500 bg-gradient-to-br from-primary-50 to-blue-50 dark:from-primary-900/20 dark:to-blue-900/20 shadow-primary-500/25' : 'border-gray-200 dark:border-gray-600 hover:border-primary-300 dark:hover:border-primary-700 bg-white/50 dark:bg-gray-800/50'"
                  >
                    <input
                      type="radio"
                      name="page_length"
                      :value="length"
                      v-model.number="form.page_length"
                      class="sr-only"
                    />
                    <div class="w-16 h-16 rounded-2xl flex items-center justify-center mb-3 transition-all duration-300" :class="form.page_length === length ? 'bg-primary-600 text-white shadow-lg' : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 group-hover:bg-primary-100 dark:group-hover:bg-primary-900/50'">
                      <font-awesome-icon :icon="['fas', 'book']" class="h-8 w-8" />
                    </div>
                    <span class="text-3xl font-bold mb-2" :class="form.page_length === length ? 'text-primary-900 dark:text-primary-100' : 'text-gray-900 dark:text-white'">
                      {{ length }}
                    </span>
                    <span class="text-sm font-medium mb-2" :class="form.page_length === length ? 'text-primary-700 dark:text-primary-300' : 'text-gray-500 dark:text-gray-400'">
                      pages
                    </span>
                    <span class="text-xs px-2 py-1 rounded-full" :class="form.page_length === length ? 'bg-primary-200 dark:bg-primary-800 text-primary-800 dark:text-primary-200' : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400'">
                      ~{{ getEstimatedTime(length) }}
                    </span>
                    <font-awesome-icon
                      v-if="form.page_length === length"
                      :icon="['fas', 'check-circle']"
                      class="h-6 w-6 text-primary-600 dark:text-primary-400 absolute top-3 right-3 transition-all duration-300 animate-scale-in"
                    />
                  </label>
                </div>

                <!-- Info about generation -->
                <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4 mt-6">
                  <div class="flex">
                    <font-awesome-icon :icon="['fas', 'info-circle']" class="h-5 w-5 text-blue-600 dark:text-blue-400 mt-0.5" />
                    <div class="ml-3">
                      <h3 class="text-sm font-medium text-blue-800 dark:text-blue-300">AI Generation Details</h3>
                      <div class="mt-2 text-sm text-blue-700 dark:text-blue-400">
                        <p>Our AI will create:</p>
                        <ul class="list-disc list-inside mt-1 space-y-1">
                          <li>Market-optimized title (non-editable)</li>
                          <li>{{ form.page_length }} pages of professional content</li>
                          <li>3 unique AI-generated cover designs</li>
                          <li>Print-ready PDF with selected cover</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Step 4: Review & Confirm -->
              <div v-show="currentStep === 3" class="space-y-6 animate-fade-in">
                <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                  <font-awesome-icon :icon="['fas', 'check-square']" class="mr-3 text-primary-600 dark:text-primary-400" />
                  Review Your Book Configuration
                </h2>
                
                <p class="text-gray-600 dark:text-gray-400 mb-6">
                  Please review your selections before we start generating your book. This process cannot be interrupted once started.
                </p>

                <div class="bg-gradient-to-r from-primary-50 to-blue-50 dark:from-primary-900/20 dark:to-blue-900/20 rounded-xl p-6 space-y-4">
                  <div class="flex items-start">
                    <div class="flex-shrink-0 w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
                      <font-awesome-icon :icon="['fas', 'compass']" class="text-white" />
                    </div>
                    <div class="ml-4">
                      <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Domain</p>
                      <p class="text-lg font-bold text-gray-900 dark:text-white">{{ getDomainLabel(form.domain) }}</p>
                    </div>
                  </div>

                  <div class="flex items-start">
                    <div class="flex-shrink-0 w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
                      <font-awesome-icon :icon="['fas', 'bullseye']" class="text-white" />
                    </div>
                    <div class="ml-4">
                      <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Sub-Niche</p>
                      <p class="text-lg font-bold text-gray-900 dark:text-white">{{ getNicheLabel(form.sub_niche) }}</p>
                    </div>
                  </div>

                  <div class="flex items-start">
                    <div class="flex-shrink-0 w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
                      <font-awesome-icon :icon="['fas', 'file-pdf']" class="text-white" />
                    </div>
                    <div class="ml-4">
                      <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Book Length</p>
                      <p class="text-lg font-bold text-gray-900 dark:text-white">{{ form.page_length }} Pages</p>
                      <p class="text-sm text-gray-600 dark:text-gray-400">Estimated generation time: {{ getEstimatedTime(form.page_length) }}</p>
                    </div>
                  </div>
                </div>

                <!-- What happens next -->
                <div class="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4">
                  <div class="flex">
                    <font-awesome-icon :icon="['fas', 'clock']" class="h-5 w-5 text-yellow-600 dark:text-yellow-400 mt-0.5" />
                    <div class="ml-3">
                      <h3 class="text-sm font-medium text-yellow-800 dark:text-yellow-300">What Happens Next?</h3>
                      <div class="mt-2 text-sm text-yellow-700 dark:text-yellow-400">
                        <ol class="list-decimal list-inside space-y-1">
                          <li>AI generates your book content ({{ getEstimatedTime(form.page_length) }})</li>
                          <li>System creates 3 professional cover options</li>
                          <li>You'll be redirected to select your favorite cover</li>
                          <li>Final PDF will be assembled and ready to download</li>
                        </ol>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

            </div>

            <!-- Action Buttons -->
            <div class="bg-gradient-to-r from-gray-50 to-blue-50 dark:from-gray-900/50 dark:to-blue-900/50 px-10 py-8 sm:px-12 flex items-center justify-between border-t border-gray-200 dark:border-gray-700">
              <button
                v-if="currentStep > 0"
                type="button"
                @click="handleBack"
                class="inline-flex items-center px-8 py-4 border-2 border-gray-300 dark:border-gray-600 text-sm font-semibold rounded-xl text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 transition-all duration-300 shadow-lg hover:shadow-xl hover:scale-105 active:scale-95"
              >
                <font-awesome-icon :icon="['fas', 'arrow-left']" class="mr-3 h-4 w-4" />
                Back
              </button>
              <div v-else></div>

              <button
                type="submit"
                :disabled="loading || !isStepValid"
                class="inline-flex items-center px-10 py-4 border border-transparent text-sm font-bold rounded-xl text-white bg-gradient-to-r from-primary-600 via-primary-700 to-blue-700 hover:from-primary-700 hover:via-primary-800 hover:to-blue-800 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105 active:scale-95 transition-all duration-300 shadow-xl shadow-primary-500/25 hover:shadow-2xl hover:shadow-primary-500/40"
              >
                <span v-if="!loading">
                  <font-awesome-icon v-if="currentStep < 3" :icon="['fas', 'arrow-right']" class="mr-3 h-4 w-4" />
                  <font-awesome-icon v-else :icon="['fas', 'magic']" class="mr-3 h-4 w-4" />
                  {{ currentStep < 3 ? 'Continue' : 'Generate My Book' }}
                </span>
                <span v-else class="flex items-center">
                  <font-awesome-icon :icon="['fas', 'spinner']" spin class="mr-3 h-4 w-4" />
                  Creating...
                </span>
              </button>
            </div>
          </form>
        </div>

        <!-- Trending Niches Info -->
        <div class="mt-12 bg-gradient-to-r from-primary-50 via-blue-50 to-indigo-50 dark:from-primary-900/20 dark:via-blue-900/20 dark:to-indigo-900/20 rounded-3xl p-8 shadow-xl border border-primary-200 dark:border-primary-800 backdrop-blur-sm">
          <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center">
            <div class="w-10 h-10 bg-gradient-to-r from-primary-600 to-blue-700 rounded-xl flex items-center justify-center mr-4 shadow-lg">
              <font-awesome-icon :icon="['fas', 'chart-line']" class="h-5 w-5 text-white" />
            </div>
            Why These Niches?
          </h3>
          <p class="text-lg text-gray-700 dark:text-gray-300 mb-6 leading-relaxed">
            Our 32 sub-niches across 4 trending domains are carefully curated based on 2025 market research and audience demand.
          </p>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="flex items-start">
              <div class="w-12 h-12 bg-green-500 rounded-xl flex items-center justify-center mr-4 shadow-lg flex-shrink-0">
                <font-awesome-icon :icon="['fas', 'search']" class="h-6 w-6 text-white" />
              </div>
              <div>
                <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">Market Research</h4>
                <p class="text-gray-600 dark:text-gray-400">2025 Google Trends analysis and audience demand data drive our selections.</p>
              </div>
            </div>
            <div class="flex items-start">
              <div class="w-12 h-12 bg-blue-500 rounded-xl flex items-center justify-center mr-4 shadow-lg flex-shrink-0">
                <font-awesome-icon :icon="['fas', 'users']" class="h-6 w-6 text-white" />
              </div>
              <div>
                <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">Proven Demand</h4>
                <p class="text-gray-600 dark:text-gray-400">Active communities and high search volumes ensure market viability.</p>
              </div>
            </div>
            <div class="flex items-start">
              <div class="w-12 h-12 bg-purple-500 rounded-xl flex items-center justify-center mr-4 shadow-lg flex-shrink-0">
                <font-awesome-icon :icon="['fas', 'dollar-sign']" class="h-6 w-6 text-white" />
              </div>
              <div>
                <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">Monetization Potential</h4>
                <p class="text-gray-600 dark:text-gray-400">Strong buyer intent and evergreen topics maximize earning potential.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../../stores/auth';
import Layout from '../../components/Layout.vue';
import apiClient from '../../services/api';

const router = useRouter();
const authStore = useAuthStore();

const currentStep = ref(0);
const loading = ref(false);
const error = ref('');

const steps = ['Domain', 'Sub-Niche', 'Length', 'Confirm'];

const form = ref({
  domain: '',
  sub_niche: '',
  page_length: 20,
});

const domains = ref([
  { value: 'ai_digital_transformation', label: 'AI & Digital Transformation' },
  { value: 'sustainability_green_tech', label: 'Sustainability & Green Tech' },
  { value: 'mental_health_tech', label: 'Mental Health Technology' },
  { value: 'future_skills', label: 'Future Skills & Technologies' }
]);

const domainIcons: Record<string, string> = {
  'ai_digital_transformation': 'robot',
  'sustainability_green_tech': 'leaf',
  'mental_health_tech': 'brain',
  'future_skills': 'rocket'
};

const domainDescriptions: Record<string, string> = {
  'ai_digital_transformation': 'AI automation & digital innovation',
  'sustainability_green_tech': 'Green tech & eco-innovation',
  'mental_health_tech': 'Digital mental wellness solutions',
  'future_skills': 'Emerging tech & future-ready skills'
};

const allNiches = ref<any>({});
const pageLengths = [15, 20, 25, 30];

const availableNiches = computed(() => {
  if (!form.value.domain || !allNiches.value[form.value.domain]) {
    return [];
  }
  
  const domainNiches = allNiches.value[form.value.domain];
  if (!Array.isArray(domainNiches)) return [];
  
  return domainNiches.map((niche: any) => ({
    value: niche.value,
    label: niche.label
  }));
});

const isStepValid = computed(() => {
  switch (currentStep.value) {
    case 0:
      return form.value.domain !== '';
    case 1:
      return form.value.sub_niche !== '';
    case 2:
      return form.value.page_length > 0;
    case 3:
      return true;
    default:
      return false;
  }
});

onMounted(async () => {
  // Check authentication
  if (!authStore.isAuthenticated) {
    router.push('/auth/signin');
    return;
  }

  try {
    const response = await apiClient.get('/config/sub-niches/');
    domains.value = response.data.domains || [];
    allNiches.value = response.data.sub_niches || {};
    console.log('Loaded niches:', allNiches.value);
  } catch (err) {
    error.value = 'Failed to load book configuration';
    console.error('Failed to load niches:', err);
  }
});

const getDomainLabel = (value: string) => {
  const domain = domains.value.find(d => d.value === value);
  return domain ? domain.label : value;
};

const getNicheLabel = (value: string) => {
  const niche = availableNiches.value.find((n: any) => n.value === value);
  return niche ? niche.label : value;
};

const getDomainDescription = (value: string) => {
  return domainDescriptions[value] || 'Trending niche content';
};

const getEstimatedTime = (pages: number) => {
  const minutes = Math.ceil(pages / 5) * 2;
  return `${minutes}-${minutes + 5} min`;
};

const handleNext = async () => {
  error.value = '';
  
  if (currentStep.value < 3) {
    currentStep.value++;
  } else {
    // Submit the form
    await handleSubmit();
  }
};

const handleBack = () => {
  if (currentStep.value > 0) {
    currentStep.value--;
  }
};

const handleSubmit = async () => {
  try {
    loading.value = true;
    error.value = '';

    console.log('Submitting book creation with data:', form.value);
    const response = await apiClient.post('/books/', form.value);
    const book = response.data;

    // Validate response has book ID before redirect
    if (!book || !book.id) {
      throw new Error('Server did not return book data');
    }

    // Redirect to book details page to monitor progress
    router.push(`/profile/books/${book.id}`);
  } catch (err: any) {
    console.error('Create book error details:', err.response?.data);
    console.error('Create book error status:', err.response?.status);
    console.error('Create book error headers:', err.response?.headers);
    
    let errorMessage = 'Failed to create book';
    if (err.response?.data) {
      if (typeof err.response.data === 'string') {
        errorMessage = err.response.data;
      } else if (err.response.data.detail) {
        errorMessage = err.response.data.detail;
      } else if (err.response.data.error) {
        errorMessage = err.response.data.error;
      } else if (typeof err.response.data === 'object') {
        // Handle validation errors
        const errors = [];
        for (const [field, fieldErrors] of Object.entries(err.response.data)) {
          if (Array.isArray(fieldErrors)) {
            errors.push(`${field}: ${fieldErrors.join(', ')}`);
          } else {
            errors.push(`${field}: ${fieldErrors}`);
          }
        }
        errorMessage = errors.join('; ');
      }
    } else if (err.message) {
      errorMessage = err.message;
    }
    
    error.value = errorMessage;
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes scale-in {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes pulse-glow {
  0%, 100% {
    box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
  }
  50% {
    box-shadow: 0 0 30px rgba(59, 130, 246, 0.6);
  }
}

.animate-fade-in {
  animation: fade-in 0.6s ease-out;
}

.animate-slide-up {
  animation: slide-up 0.8s ease-out;
}

.animate-scale-in {
  animation: scale-in 0.4s ease-out;
}

.animate-pulse-glow {
  animation: pulse-glow 2s infinite;
}

/* Hover effects */
.hover\:scale-102:hover {
  transform: scale(1.02);
}

.hover\:scale-105:hover {
  transform: scale(1.05);
}

/* Gradient text */
.gradient-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Glass morphism effect */
.glass {
  backdrop-filter: blur(16px) saturate(180%);
  background-color: rgba(255, 255, 255, 0.75);
  border: 1px solid rgba(209, 213, 219, 0.3);
}

/* Custom scrollbar for the component */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #5a67d8, #6b46c1);
}
</style>
