<template>
  <Layout>
    <div class="min-h-screen bg-gradient-to-br from-primary-50 via-white to-blue-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-4xl mx-auto">
        <!-- Header -->
        <div class="text-center mb-12 animate-fade-in">
          <div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-primary-600 to-blue-700 rounded-2xl mb-4 shadow-lg">
            <font-awesome-icon :icon="['fas', 'magic']" class="h-8 w-8 text-white" />
          </div>
          <h1 class="text-4xl font-extrabold text-gray-900 dark:text-white mb-2">
            Create Your AI-Powered Book
          </h1>
          <p class="text-lg text-gray-600 dark:text-gray-400">
            Follow these simple steps to generate your professional book
          </p>
        </div>

        <!-- Progress Steps -->
        <div class="mb-12">
          <div class="flex items-center justify-between">
            <div v-for="(step, index) in steps" :key="index" class="flex-1">
              <div class="flex items-center" :class="index < steps.length - 1 ? 'mr-4' : ''">
                <div class="flex flex-col items-center flex-1">
                  <div 
                    class="w-10 h-10 rounded-full flex items-center justify-center font-bold transition-all duration-300"
                    :class="currentStep > index ? 'bg-green-500 text-white' : currentStep === index ? 'bg-primary-600 text-white ring-4 ring-primary-200 dark:ring-primary-900' : 'bg-gray-300 dark:bg-gray-700 text-gray-600 dark:text-gray-400'"
                  >
                    <font-awesome-icon v-if="currentStep > index" :icon="['fas', 'check']" />
                    <span v-else>{{ index + 1 }}</span>
                  </div>
                  <span class="text-xs mt-2 font-medium" :class="currentStep >= index ? 'text-gray-900 dark:text-white' : 'text-gray-500 dark:text-gray-400'">
                    {{ step }}
                  </span>
                </div>
                <div v-if="index < steps.length - 1" class="flex-1 h-1 mx-2" :class="currentStep > index ? 'bg-green-500' : 'bg-gray-300 dark:bg-gray-700'"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="rounded-lg bg-red-50 dark:bg-red-900/20 p-4 mb-6 border border-red-200 dark:border-red-800 animate-scale-in">
          <div class="flex">
            <font-awesome-icon :icon="['fas', 'exclamation-circle']" class="h-5 w-5 text-red-400 mt-0.5" />
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800 dark:text-red-300">{{ error }}</h3>
            </div>
          </div>
        </div>

        <!-- Form Card -->
        <div class="bg-white dark:bg-gray-800 shadow-2xl rounded-3xl overflow-hidden border border-gray-200 dark:border-gray-700 animate-slide-up">
          <form @submit.prevent="handleNext">
            <div class="p-8 sm:p-12">
              
              <!-- Step 1: Choose Domain -->
              <div v-show="currentStep === 0" class="space-y-6 animate-fade-in">
                <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                  <font-awesome-icon :icon="['fas', 'compass']" class="mr-3 text-primary-600 dark:text-primary-400" />
                  Choose Your Book Domain
                </h2>
                
                <p class="text-gray-600 dark:text-gray-400 mb-6">
                  Select the main category that best fits your book concept. We've curated 5 trending domains with proven market demand.
                </p>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <label
                    v-for="domain in domains"
                    :key="domain.value"
                    class="relative flex cursor-pointer rounded-xl border p-6 shadow-sm focus:outline-none transition-all duration-200 hover:shadow-lg"
                    :class="form.domain === domain.value ? 'border-primary-600 ring-2 ring-primary-600 bg-primary-50 dark:bg-primary-900/20' : 'border-gray-300 dark:border-gray-600 hover:border-primary-300 dark:hover:border-primary-700'"
                  >
                    <input
                      type="radio"
                      name="domain"
                      :value="domain.value"
                      v-model="form.domain"
                      class="sr-only"
                    />
                    <div class="flex flex-1">
                      <div class="flex-shrink-0">
                        <font-awesome-icon :icon="['fas', domainIcons[domain.value] || 'book']" class="h-6 w-6" :class="form.domain === domain.value ? 'text-primary-600 dark:text-primary-400' : 'text-gray-400'" />
                      </div>
                      <div class="ml-4 flex flex-col">
                        <span class="block text-sm font-medium" :class="form.domain === domain.value ? 'text-primary-900 dark:text-primary-100' : 'text-gray-900 dark:text-white'">
                          {{ domain.label }}
                        </span>
                      </div>
                    </div>
                    <font-awesome-icon
                      v-if="form.domain === domain.value"
                      :icon="['fas', 'check-circle']"
                      class="h-5 w-5 text-primary-600 dark:text-primary-400 absolute top-4 right-4"
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

                <div class="space-y-3">
                  <label
                    v-for="niche in availableNiches"
                    :key="niche.value"
                    class="relative flex cursor-pointer rounded-lg border p-4 shadow-sm focus:outline-none transition-all duration-200 hover:shadow-md"
                    :class="form.sub_niche === niche.value ? 'border-primary-600 ring-2 ring-primary-600 bg-primary-50 dark:bg-primary-900/20' : 'border-gray-300 dark:border-gray-600 hover:border-primary-300'"
                  >
                    <input
                      type="radio"
                      name="sub_niche"
                      :value="niche.value"
                      v-model="form.sub_niche"
                      class="sr-only"
                    />
                    <div class="flex flex-1 items-center">
                      <div class="flex-shrink-0">
                        <div class="w-10 h-10 rounded-lg flex items-center justify-center" :class="form.sub_niche === niche.value ? 'bg-primary-600 text-white' : 'bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-400'">
                          <font-awesome-icon :icon="['fas', 'star']" />
                        </div>
                      </div>
                      <span class="ml-4 block text-sm font-medium" :class="form.sub_niche === niche.value ? 'text-primary-900 dark:text-primary-100' : 'text-gray-900 dark:text-white'">
                        {{ niche.label }}
                      </span>
                    </div>
                    <font-awesome-icon
                      v-if="form.sub_niche === niche.value"
                      :icon="['fas', 'check-circle']"
                      class="h-5 w-5 text-primary-600 dark:text-primary-400"
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

                <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <label
                    v-for="length in pageLengths"
                    :key="length"
                    class="relative flex cursor-pointer rounded-xl border p-6 shadow-sm focus:outline-none transition-all duration-200 hover:shadow-lg flex-col items-center"
                    :class="form.page_length === length ? 'border-primary-600 ring-2 ring-primary-600 bg-primary-50 dark:bg-primary-900/20' : 'border-gray-300 dark:border-gray-600 hover:border-primary-300'"
                  >
                    <input
                      type="radio"
                      name="page_length"
                      :value="length"
                      v-model.number="form.page_length"
                      class="sr-only"
                    />
                    <font-awesome-icon :icon="['fas', 'book']" class="h-8 w-8 mb-2" :class="form.page_length === length ? 'text-primary-600 dark:text-primary-400' : 'text-gray-400'" />
                    <span class="text-2xl font-bold" :class="form.page_length === length ? 'text-primary-900 dark:text-primary-100' : 'text-gray-900 dark:text-white'">
                      {{ length }}
                    </span>
                    <span class="text-xs" :class="form.page_length === length ? 'text-primary-700 dark:text-primary-300' : 'text-gray-500 dark:text-gray-400'">
                      pages
                    </span>
                    <span class="text-xs mt-2" :class="form.page_length === length ? 'text-primary-700 dark:text-primary-300' : 'text-gray-500 dark:text-gray-400'">
                      ~{{ getEstimatedTime(length) }}
                    </span>
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
            <div class="bg-gray-50 dark:bg-gray-900/50 px-8 py-6 sm:px-12 flex items-center justify-between border-t border-gray-200 dark:border-gray-700">
              <button
                v-if="currentStep > 0"
                type="button"
                @click="handleBack"
                class="inline-flex items-center px-6 py-3 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-lg text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 transition-all duration-200 shadow-sm"
              >
                <font-awesome-icon :icon="['fas', 'arrow-left']" class="mr-2" />
                Back
              </button>
              <div v-else></div>

              <button
                type="submit"
                :disabled="loading || !isStepValid"
                class="inline-flex items-center px-8 py-3 border border-transparent text-sm font-medium rounded-lg text-white bg-gradient-to-r from-primary-600 to-blue-700 hover:from-primary-700 hover:to-blue-800 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105 active:scale-95 transition-all duration-200 shadow-lg"
              >
                <span v-if="!loading">
                  <font-awesome-icon v-if="currentStep < 3" :icon="['fas', 'arrow-right']" class="mr-2" />
                  <font-awesome-icon v-else :icon="['fas', 'magic']" class="mr-2" />
                  {{ currentStep < 3 ? 'Next Step' : 'Generate My Book' }}
                </span>
                <span v-else class="flex items-center">
                  <font-awesome-icon :icon="['fas', 'spinner']" spin class="mr-2" />
                  Generating...
                </span>
              </button>
            </div>
          </form>
        </div>

        <!-- Trending Niches Info -->
        <div class="mt-8 bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg border border-gray-200 dark:border-gray-700">
          <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4 flex items-center">
            <font-awesome-icon :icon="['fas', 'chart-line']" class="mr-2 text-primary-600 dark:text-primary-400" />
            Why These Niches?
          </h3>
          <p class="text-sm text-gray-600 dark:text-gray-400">
            Our 15 sub-niches across 5 domains are carefully curated based on:
          </p>
          <ul class="mt-3 space-y-2 text-sm text-gray-600 dark:text-gray-400">
            <li class="flex items-start">
              <font-awesome-icon :icon="['fas', 'check']" class="h-5 w-5 text-green-500 mr-2 flex-shrink-0" />
              <span><strong>Market Research:</strong> Google Trends analysis and audience demand data</span>
            </li>
            <li class="flex items-start">
              <font-awesome-icon :icon="['fas', 'check']" class="h-5 w-5 text-green-500 mr-2 flex-shrink-0" />
              <span><strong>Proven Demand:</strong> Active communities and high search volumes</span>
            </li>
            <li class="flex items-start">
              <font-awesome-icon :icon="['fas', 'check']" class="h-5 w-5 text-green-500 mr-2 flex-shrink-0" />
              <span><strong>Monetization Potential:</strong> Strong buyer intent and evergreen topics</span>
            </li>
          </ul>
        </div>
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
  { value: 'personal_development', label: 'Personal Development and Self-Help' },
  { value: 'business_entrepreneurship', label: 'Business and Entrepreneurship' },
  { value: 'health_wellness', label: 'Health and Wellness' },
  { value: 'relationships', label: 'Relationships' },  
  { value: 'childrens_books', label: 'Children\'s Books' },
  { value: 'education_learning', label: 'Education and Learning' },
  { value: 'technology_digital', label: 'Technology and Digital Skills' },
  { value: 'finance_investment', label: 'Finance and Investment' },
  { value: 'hobbies_interests', label: 'Hobbies and Interests' },
  { value: 'travel_adventure', label: 'Travel and Adventure' },
  { value: 'productivity_time', label: 'Productivity and Time Management' },
  { value: 'creative_writing', label: 'Creative Writing and Storytelling' },
  { value: 'sustainability_eco', label: 'Sustainability and Eco-Friendly Living' },
  { value: 'ai_future_tech', label: 'AI and Future Technologies' },
  { value: 'mindfulness_meditation', label: 'Mindfulness and Meditation' }
]);

const domainIcons: Record<string, string> = {
  'personal_development': 'user-graduate',
  'business_entrepreneurship': 'briefcase',
  'health_wellness': 'heartbeat', 
  'relationships': 'heart',
  'childrens_books': 'child',
  'education_learning': 'graduation-cap',
  'technology_digital': 'laptop-code',
  'finance_investment': 'chart-line',
  'hobbies_interests': 'palette',
  'travel_adventure': 'plane',
  'productivity_time': 'clock',
  'creative_writing': 'pen-fancy',
  'sustainability_eco': 'leaf', 
  'ai_future_tech': 'robot',
  'mindfulness_meditation': 'spa'
};

const allNiches = ref<any>({});
const pageLengths = [15, 20, 25, 30];

const availableNiches = computed(() => {
  if (!form.value.domain || !allNiches.value[form.value.domain]) {
    return [];
  }
  
  const domain = allNiches.value[form.value.domain];
  if (!domain || !domain.sub_niches) return [];
  
  return Object.keys(domain.sub_niches).map(key => ({
    value: key,
    label: domain.sub_niches[key].name || key.replace(/_/g, ' ')
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
  try {
    const response = await apiClient.get('/config/sub-niches/');
    allNiches.value = response.data.sub_niches;
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

    const response = await apiClient.post('/books/', form.value);
    const book = response.data;

    // Validate response has book ID before redirect
    if (!book || !book.id) {
      throw new Error('Server did not return book data');
    }

    // Redirect to book details page to monitor progress
    router.push(`/profile/books/${book.id}`);
  } catch (err: any) {
    error.value = err.response?.data?.error || err.response?.data?.detail || err.message || 'Failed to create book';
    console.error('Create book error:', err);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

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

.animate-fade-in {
  animation: fade-in 0.5s ease-out;
}

.animate-slide-up {
  animation: slide-up 0.6s ease-out;
}

.animate-scale-in {
  animation: scale-in 0.3s ease-out;
}

@keyframes scale-in {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
