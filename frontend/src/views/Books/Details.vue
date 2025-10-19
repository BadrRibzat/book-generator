<template>
  <Layout>
    <div class="min-h-screen bg-gray-50 dark:bg-gray-900">

    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div v-if="booksStore.loading" class="text-center py-12">
          <font-awesome-icon :icon="['fas', 'spinner']" spin class="h-12 w-12 text-primary-600" />
          <p class="mt-2 text-gray-600">Loading book details...</p>
        </div>

        <div v-else-if="booksStore.error" class="rounded-md bg-red-50 p-4">
          <div class="flex">
            <font-awesome-icon :icon="['fas', 'exclamation-circle']" class="h-5 w-5 text-red-400" />
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800">{{ booksStore.error }}</h3>
            </div>
          </div>
        </div>

        <div v-else-if="book" class="space-y-6">
          <!-- Cover Selection Modal -->
          <CoverSelectionModal
            v-if="showCoverModal && bookId > 0"
            :bookId="bookId"
            :onClose="() => showCoverModal = false"
            :onSelect="() => showCoverModal = false"
          />
          
          <!-- Book Header Card -->
          <div class="bg-white shadow overflow-hidden sm:rounded-lg">
            <div class="px-4 py-5 sm:px-6 flex justify-between items-center">
              <div>
                <h3 class="text-lg leading-6 font-medium text-gray-900">{{ book.title }}</h3>
                <p class="mt-1 max-w-2xl text-sm text-gray-500">
                  Created {{ formatDate(book.created_at) }}
                </p>
              </div>
              <span
                :class="getStatusClass(book.status)"
                class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium"
              >
                <font-awesome-icon
                  :icon="['fas', getStatusIcon(book.status)]"
                  :spin="book.status === 'generating'"
                  class="mr-2"
                />
                {{ getStatusLabel(book.status) }}
              </span>
            </div>
            <div class="border-t border-gray-200">
              <dl>
                <div class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt class="text-sm font-medium text-gray-500">Domain</dt>
                  <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    {{ formatDomain(book.domain) }}
                  </dd>
                </div>
                <div class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt class="text-sm font-medium text-gray-500">Sub-Niche</dt>
                  <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    {{ formatNiche(book.sub_niche) }}
                  </dd>
                </div>
                <div class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt class="text-sm font-medium text-gray-500">Page Length</dt>
                  <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    {{ book.page_length }} pages
                  </dd>
                </div>
                <div class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt class="text-sm font-medium text-gray-500">Last Updated</dt>
                  <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    {{ formatDate(book.updated_at) }}
                  </dd>
                </div>
                <div v-if="book.completed_at" class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt class="text-sm font-medium text-gray-500">Completed</dt>
                  <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    {{ formatDate(book.completed_at) }}
                  </dd>
                </div>
                <div v-if="book.error_message" class="bg-red-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt class="text-sm font-medium text-red-700">Error</dt>
                  <dd class="mt-1 text-sm text-red-900 sm:mt-0 sm:col-span-2">
                    {{ book.error_message }}
                    <div class="mt-3" v-if="book.error_message.includes('Cover generation failed')">
                      <p class="text-sm text-red-700 font-medium">Missing cover selection:</p>
                      <p class="text-sm text-red-700">You need to select a cover for your book before it can be finalized.</p>
                      <div class="flex space-x-3 mt-2">
                        <button
                          @click="handleRegenerateCovers"
                          class="inline-flex items-center px-3 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700"
                        >
                          <font-awesome-icon :icon="['fas', 'redo']" class="mr-2" />
                          Regenerate Covers
                        </button>
                        <button
                          @click="showCoverModal = true"
                          class="inline-flex items-center px-3 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700"
                        >
                          <font-awesome-icon :icon="['fas', 'palette']" class="mr-2" />
                          Select Cover
                        </button>
                      </div>
                    </div>
                  </dd>
                </div>
              </dl>
            </div>
          </div>

          <!-- Generation Progress Card -->
          <div v-if="book.status === 'generating'" class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6">
            <div class="flex items-start">
              <font-awesome-icon :icon="['fas', 'spinner']" spin class="h-6 w-6 text-blue-600 dark:text-blue-400 mt-0.5" />
              <div class="ml-4">
                <h3 class="text-sm font-medium text-blue-900 dark:text-blue-100">Book Generation in Progress</h3>
                <p class="mt-2 text-sm text-blue-700 dark:text-blue-300">
                  Our AI is generating your book content. This typically takes 6-15 minutes depending on the page count. You can stay on this page and we'll update automatically.
                </p>
                <div class="mt-4 flex items-center">
                  <div class="flex-1 bg-blue-200 dark:bg-blue-800 rounded-full h-2">
                    <div class="bg-blue-600 dark:bg-blue-400 h-2 rounded-full" style="width: 50%"></div>
                  </div>
                  <span class="ml-3 text-sm font-medium text-blue-900 dark:text-blue-100">50%</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Cover Selection Card -->
          <div v-if="book.status === 'content_generated' && book.covers.length > 0" class="bg-white shadow sm:rounded-lg border-l-4 border-yellow-500">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                <font-awesome-icon :icon="['fas', 'palette']" class="mr-2 text-primary-600" />
                Action Required: Select a Cover
              </h3>
              <p class="text-sm text-gray-500 mb-6">
                <strong>Important:</strong> Your book content is ready! You must now choose one of the generated covers for your book before it can be finalized. Each design has been AI-optimized for your niche.
              </p>
              <div class="flex space-x-3">
                <router-link
                  :to="`/profile/books/${book.id}/covers`"
                  class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 shadow-md"
                >
                  <font-awesome-icon :icon="['fas', 'hand-pointer']" class="mr-2" />
                  Choose Cover Now
                </router-link>
                <button
                  @click="showCoverModal = true"
                  class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                >
                  <font-awesome-icon :icon="['fas', 'external-link']" class="mr-2" />
                  Choose in Modal
                </button>
              </div>
            </div>
          </div>

          <!-- Pending Cover Generation -->
          <div v-else-if="book.status === 'cover_pending'" class="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-6">
            <div class="flex items-start">
              <font-awesome-icon :icon="['fas', 'spinner']" spin class="h-6 w-6 text-yellow-600 dark:text-yellow-400 mt-0.5" />
              <div class="ml-4">
                <h3 class="text-sm font-medium text-yellow-900 dark:text-yellow-100">Generating Cover Options</h3>
                <p class="mt-2 text-sm text-yellow-700 dark:text-yellow-300">
                  We're creating 3 professional cover designs for your book. This usually takes 2-5 minutes.
                </p>
              </div>
            </div>
          </div>

          <!-- Selected Cover Card -->
          <div v-if="book.selected_cover" class="bg-white shadow sm:rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                <font-awesome-icon :icon="['fas', 'check-circle']" class="mr-2 text-green-600" />
                Selected Cover
              </h3>
              <div class="flex items-center">
                <img
                  :src="book.selected_cover.image_url"
                  :alt="`${book.title} cover`"
                  class="max-w-sm rounded-lg shadow-lg"
                />
                <div class="ml-6">
                  <p class="text-sm text-gray-600">
                    <strong>Style:</strong> {{ book.selected_cover.template_style }}
                  </p>
                  <p class="text-sm text-gray-600 mt-2">
                    <strong>Selected:</strong> {{ formatDate(book.selected_cover.created_at) }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex space-x-4">
            <a
              v-if="book.can_download"
              :href="book.download_url || '#'"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700"
            >
              <font-awesome-icon :icon="['fas', 'download']" class="mr-2" />
              Download PDF
            </a>

            <button
              v-if="book.status === 'error' || book.status === 'ready'"
              @click="handleDelete"
              :disabled="deleting"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <font-awesome-icon :icon="['fas', 'trash']" class="mr-2" />
              <span v-if="!deleting">Delete Book</span>
              <span v-else>Deleting...</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  </Layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import { useBooksStore } from '../../stores/books';
import Layout from '../../components/Layout.vue';
import apiClient from '../../services/api';
import CoverSelectionModal from '../../components/CoverSelectionModal.vue';
import type { BookStatus, Domain, SubNiche } from '../../types';

interface Props {
  id: string;
}

const props = defineProps<Props>();
const router = useRouter();
const booksStore = useBooksStore();

const deleting = ref(false);
const book = computed(() => booksStore.currentBook);
const pollingInterval = ref<number | null>(null);
const showCoverModal = ref(false);

// Convert string ID to number safely
const bookId = computed(() => {
  const id = parseInt(props.id);
  return isNaN(id) ? 0 : id;
});

onMounted(async () => {
  if (bookId.value === 0) {
    router.push('/profile/books');
    return;
  }
  
  await booksStore.fetchBook(bookId.value);
  
  // Start polling if book is generating
  if (booksStore.currentBook?.status === 'generating') {
    startPolling();
  }
});

onBeforeUnmount(() => {
  if (pollingInterval.value) {
    clearInterval(pollingInterval.value);
  }
});

const startPolling = () => {
  if (pollingInterval.value) {
    clearInterval(pollingInterval.value);
  }
  
  pollingInterval.value = window.setInterval(async () => {
    if (bookId.value > 0) {
      await booksStore.fetchBook(bookId.value);
      
      // Get current status
      const status = booksStore.currentBook?.status;
      
      // Show cover selection when content is generated
      if (status === 'content_generated' && booksStore.currentBook?.covers.length > 0) {
        clearInterval(pollingInterval.value);
        pollingInterval.value = null;
        // Show cover selection modal instead of redirecting
        showCoverModal.value = true;
        return;
      }
      
      // Stop polling for other non-generating statuses
      if (status !== 'generating' && pollingInterval.value) {
        clearInterval(pollingInterval.value);
        pollingInterval.value = null;
      }
    }
  }, 2000); // Poll every 2 seconds
};

const getStatusClass = (status: BookStatus) => {
  const classes: Record<BookStatus, string> = {
    draft: 'bg-gray-100 text-gray-800',
    generating: 'bg-blue-100 text-blue-800',
    content_generated: 'bg-yellow-100 text-yellow-800',
    cover_pending: 'bg-purple-100 text-purple-800',
    ready: 'bg-green-100 text-green-800',
    error: 'bg-red-100 text-red-800',
  };
  return classes[status];
};

const getStatusIcon = (status: BookStatus) => {
  const icons: Record<BookStatus, string> = {
    draft: 'exclamation-circle',
    generating: 'spinner',
    content_generated: 'check-circle',
    cover_pending: 'exclamation-circle',
    ready: 'check-circle',
    error: 'exclamation-circle',
  };
  return icons[status];
};

const getStatusLabel = (status: BookStatus) => {
  const labels: Record<BookStatus, string> = {
    draft: 'Draft',
    generating: 'Generating Content',
    content_generated: 'Content Ready',
    cover_pending: 'Select Cover',
    ready: 'Ready to Download',
    error: 'Error',
  };
  return labels[status];
};

const formatDomain = (domain: Domain) => {
  return domain.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase());
};

const formatNiche = (niche: SubNiche) => {
  return niche.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase());
};

const formatDate = (date: string) => {
  return new Date(date).toLocaleString();
};

const handleRegenerateCovers = async () => {
  if (!bookId.value) return;
  
  try {
    booksStore.loading = true;
    const response = await apiClient.post(`/books/${bookId.value}/regenerate-covers/`);
    
    // Refresh book data
    await booksStore.fetchBook(bookId.value);
    
    // Redirect to cover selection if covers are ready
    if (booksStore.currentBook?.covers.length > 0) {
      router.push(`/profile/books/${bookId.value}/covers`);
    }
  } catch (error) {
    console.error('Failed to regenerate covers:', error);
  } finally {
    booksStore.loading = false;
  }
};

const handleDelete = async () => {
  if (!confirm('Are you sure you want to delete this book? This action cannot be undone.')) {
    return;
  }

  deleting.value = true;
  const result = await booksStore.deleteBook(parseInt(props.id));
  deleting.value = false;

  if (result.success) {
    router.push('/profile/books');
  }
};
</script>
