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

        <!-- Error Message -->
        <div v-if="booksStore.error" class="rounded-lg bg-red-50 dark:bg-red-900/20 p-6 mb-6 border border-red-200 dark:border-red-800 animate-scale-in">
          <div class="flex">
            <font-awesome-icon :icon="['fas', 'exclamation-circle']" class="h-5 w-5 text-red-400 dark:text-red-500 mt-0.5" />
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800 dark:text-red-400">{{ booksStore.error }}</h3>
            </div>
          </div>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="bg-white dark:bg-gray-800 shadow-xl rounded-2xl border border-gray-200 dark:border-gray-700 overflow-hidden animate-slide-up">
          <div class="px-6 py-8 space-y-6">
            <!-- Domain Select -->
            <div class="group">
              <label for="domain" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                <font-awesome-icon :icon="['fas', 'book-open']" class="mr-2 text-primary-600 dark:text-primary-400" />
                Domain
              </label>
              <select
                id="domain"
                v-model="form.domain"
                @change="handleDomainChange"
                required
                class="mt-1 block w-full pl-4 pr-10 py-3 text-base border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500 dark:focus:ring-primary-400 focus:border-transparent rounded-lg transition-all duration-200"
              >
                <option value="">Select a domain</option>
                <option value="language_kids">Language & Kids</option>
                <option value="tech_ai">Technology & AI</option>
                <option value="nutrition">Nutrition & Wellness</option>
                <option value="meditation">Meditation & Mindfulness</option>
                <option value="home_workout">Home Workout & Fitness</option>
              </select>
              <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">Choose the main category for your book</p>
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
              to="/books"
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
import { reactive, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useBooksStore } from '../../stores/books';
import Layout from '../../components/Layout.vue';
import type { BookCreate, Domain } from '../../types';

const router = useRouter();
const booksStore = useBooksStore();

const form = reactive<BookCreate>({
  domain: '' as Domain,
  sub_niche: '' as any,
  page_length: 20,
});

const nichesByDomain: Record<Domain, Array<{ value: string; label: string }>> = {
  language_kids: [
    { value: 'ai_learning_stories', label: 'AI Learning Stories' },
    { value: 'multilingual_coloring', label: 'Multilingual Coloring Books' },
    { value: 'kids_mindful_journals', label: 'Kids Mindfulness Journals' },
  ],
  tech_ai: [
    { value: 'ai_ethics', label: 'AI Ethics & Responsibility' },
    { value: 'nocode_guides', label: 'No-Code Development Guides' },
    { value: 'smart_home_diy', label: 'Smart Home DIY' },
  ],
  nutrition: [
    { value: 'specialty_diet', label: 'Specialty Diet Cookbooks' },
    { value: 'plant_based_cooking', label: 'Plant-Based Cooking' },
    { value: 'nutrition_mental_health', label: 'Nutrition for Mental Health' },
  ],
  meditation: [
    { value: 'mindfulness_anxiety', label: 'Mindfulness for Anxiety' },
    { value: 'sleep_meditation', label: 'Sleep Meditation Guides' },
    { value: 'gratitude_journals', label: 'Gratitude Journals' },
  ],
  home_workout: [
    { value: 'equipment_free', label: 'Equipment-Free Workouts' },
    { value: 'yoga_remote_workers', label: 'Yoga for Remote Workers' },
    { value: 'mobility_training', label: 'Mobility Training' },
  ],
};

const availableNiches = computed(() => {
  if (!form.domain) return [];
  return nichesByDomain[form.domain] || [];
});

const handleDomainChange = () => {
  form.sub_niche = '' as any;
};

const handleSubmit = async () => {
  booksStore.clearError();
  
  const result = await booksStore.createBook(form);
  
  if (result.success && result.data) {
    router.push(`/books/${result.data.id}`);
  }
};
</script>
