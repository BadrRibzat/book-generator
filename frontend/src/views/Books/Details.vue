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
          <!-- Generation Progress Bar (only show when generating or cover_pending) -->
          <div v-if="book.status !== 'ready' && book.status !== 'error' && book.status !== 'content_generated'" class="bg-white shadow overflow-hidden sm:rounded-lg">
            <div class="px-4 py-5 sm:px-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900">Generation Progress</h3>
              <div class="mt-4">
                <div class="flex items-center justify-between text-sm text-gray-600 mb-2">
                  <span>{{ getCurrentStepText(book.status) }}</span>
                  <span>{{ getProgressPercentage(book.status) }}%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-3">
                  <div 
                    class="bg-gradient-to-r from-blue-500 to-purple-600 h-3 rounded-full transition-all duration-1000 ease-out"
                    :style="{ width: `${getProgressPercentage(book.status)}%` }"
                  ></div>
                </div>
                <div class="mt-3 flex items-center text-sm text-gray-500">
                  <font-awesome-icon :icon="['fas', 'clock']" class="mr-2" />
                  <span>{{ getEstimatedTime(book.status) }}</span>
                </div>
              </div>
            </div>
          </div>
          
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
                    {{ formatDomain(book.domain_name) }}
                  </dd>
                </div>
                <div class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt class="text-sm font-medium text-gray-500">Sub-Niche</dt>
                  <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    {{ formatNiche(book.niche_name) }}
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
                          @click="showCoverModal = true"
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
                <h3 class="text-sm font-medium text-blue-900 dark:text-blue-100">Professional Book Generation in Progress</h3>
                <p class="mt-2 text-sm text-blue-700 dark:text-blue-300">
                  DeepSeek R1 AI is generating your book with {{ book.page_length }}+ pages of professional content. 
                  This typically takes 2-3 minutes. The page will update automatically when complete.
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

          <!-- Cover Selection Card (show when covers are ready for manual books only) -->
          <div v-if="(book.status === 'content_generated' || book.status === 'cover_pending') && book.covers && book.covers.length > 0 && !book.book_style" class="bg-gradient-to-r from-yellow-50 to-orange-50 dark:from-yellow-900/20 dark:to-orange-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-6">
            <div class="flex items-start">
              <div class="flex-shrink-0">
                <font-awesome-icon :icon="['fas', 'palette']" class="h-6 w-6 text-yellow-600 dark:text-yellow-400" />
              </div>
              <div class="ml-4 flex-1">
                <h3 class="text-lg font-semibold text-yellow-900 dark:text-yellow-100 mb-2">🎨 Professional AI Covers Ready!</h3>
                <p class="text-sm text-yellow-800 dark:text-yellow-200 mb-4">
                  Your book content is complete! We've generated 3 professional AI cover designs 
                  (no template fallbacks). Choose your favorite to finalize your book.
                </p>
                <div class="grid grid-cols-3 gap-4 mb-4">
                  <div 
                    v-for="cover in book.covers.slice(0, 3)" 
                    :key="cover.id"
                    class="border-2 border-yellow-300 dark:border-yellow-600 rounded-lg overflow-hidden cursor-pointer hover:border-yellow-500 dark:hover:border-yellow-400 transition-colors"
                    @click="selectCoverFromCard(cover.id)"
                  >
                    <img :src="cover.image_url" :alt="cover.template_style" class="w-full h-32 object-cover" />
                    <div class="p-2 bg-yellow-100 dark:bg-yellow-900/50 text-center">
                      <p class="text-xs font-medium text-yellow-900 dark:text-yellow-100 capitalize">{{ cover.template_style }}</p>
                    </div>
                  </div>
                </div>
                <div class="flex space-x-3">
                  <button
                    @click="showCoverModal = true"
                    class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-gradient-to-r from-yellow-600 to-orange-600 hover:from-yellow-700 hover:to-orange-700 shadow-md"
                  >
                    <font-awesome-icon :icon="['fas', 'expand']" class="mr-2" />
                    View Larger & Select
                  </button>
                  <button
                    @click="showCoverModal = true"
                    class="inline-flex items-center px-4 py-2 border border-yellow-300 dark:border-yellow-600 text-sm font-medium rounded-md text-yellow-900 dark:text-yellow-100 bg-yellow-100 dark:bg-yellow-900/50 hover:bg-yellow-200 dark:hover:bg-yellow-900/70"
                  >
                    <font-awesome-icon :icon="['fas', 'hand-pointer']" class="mr-2" />
                    Choose Cover
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Pending Cover Generation -->
          <div v-else-if="book.status === 'cover_pending'" class="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-6">
            <div class="flex items-start">
              <font-awesome-icon :icon="['fas', 'spinner']" spin class="h-6 w-6 text-yellow-600 dark:text-yellow-400 mt-0.5" />
              <div class="ml-4">
                <h3 class="text-sm font-medium text-yellow-900 dark:text-yellow-100">Generating Professional AI Covers</h3>
                <p class="mt-2 text-sm text-yellow-700 dark:text-yellow-300">
                  Creating 3 unique professional cover designs using AI (no template fallbacks). This usually takes 1-2 minutes.
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
            <button
              v-if="book.can_download"
              @click="downloadBook"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700"
            >
              <font-awesome-icon :icon="['fas', 'download']" class="mr-2" />
              Download PDF
            </button>

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
import CoverSelectionModal from '../../components/CoverSelectionModal.vue';
import apiClient from '../../services/api';
import type { BookStatus } from '../../types';

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
  
  // Start polling if book is not in a final state
  const currentStatus = booksStore.currentBook?.status;
  if (currentStatus && ['generating', 'content_generated', 'cover_pending'].includes(currentStatus)) {
    startPolling();
  }
  
  // If covers are already available, show the modal immediately
  if (booksStore.currentBook?.covers && booksStore.currentBook.covers.length > 0 && 
      ['content_generated', 'cover_pending'].includes(currentStatus || '')) {
    showCoverModal.value = true;
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
    pollingInterval.value = null;
  }
  
  pollingInterval.value = window.setInterval(async () => {
    if (bookId.value > 0) {
      try {
        await booksStore.fetchBook(bookId.value);
        
        // Get current status
        const status = booksStore.currentBook?.status;
        
          // Show cover selection when content is generated or covers are pending selection (only for manual books)
          if ((status === 'content_generated' || status === 'cover_pending') && 
              booksStore.currentBook?.covers && booksStore.currentBook.covers.length > 0 &&
              !booksStore.currentBook.book_style) {  // Only show for manual books without book_style
            if (pollingInterval.value) {
              clearInterval(pollingInterval.value);
              pollingInterval.value = null;
            }
            // Show cover selection modal
            showCoverModal.value = true;
            return;
          }
        
        // Stop polling for final statuses
        if (status === 'ready' || status === 'error') {
          if (pollingInterval.value) {
            clearInterval(pollingInterval.value);
            pollingInterval.value = null;
          }
        }
      } catch (error: any) {
        console.error('Error during polling:', error);
        // If we get an authentication error, stop polling
        if (error.response?.status === 401 || error.response?.status === 403) {
          if (pollingInterval.value) {
            clearInterval(pollingInterval.value);
            pollingInterval.value = null;
          }
          // Redirect to login if session expired
          router.push('/auth/signin');
        }
      }
    }
  }, 3000); // Poll every 3 seconds
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

const formatDomain = (domain: string) => {
  return domain.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase());
};

const formatNiche = (niche: string) => {
  return niche.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase());
};

const formatDate = (date: string) => {
  return new Date(date).toLocaleString();
};

const getCurrentStepText = (status: BookStatus) => {
  // Use the real current_step from the book if available, otherwise fall back to status-based text
  if (book.value?.current_step) {
    return book.value.current_step;
  }
  
  const steps: Record<BookStatus, string> = {
    draft: 'Initializing...',
    generating: 'Generating AI content',
    content_generated: 'Content ready - generating covers',
    cover_pending: 'Covers ready - select your favorite',
    ready: 'Book completed and ready to download',
    error: 'Generation failed'
  };
  return steps[status] || 'Processing...';
};

const getProgressPercentage = (status: BookStatus) => {
  // Use the real progress_percentage from the book if available, otherwise fall back to status-based percentages
  if (book.value?.progress_percentage !== undefined && book.value.progress_percentage !== null) {
    return book.value.progress_percentage;
  }
  
  const percentages: Record<BookStatus, number> = {
    draft: 10,
    generating: 40,
    content_generated: 70,
    cover_pending: 85,
    ready: 100,
    error: 0
  };
  return percentages[status] || 0;
};

const getEstimatedTime = (status: BookStatus) => {
  const times: Record<BookStatus, string> = {
    draft: 'Starting soon...',
    generating: '2-3 minutes remaining',
    content_generated: '1-2 minutes remaining',
    cover_pending: 'Almost done!',
    ready: 'Completed',
    error: 'Please try again'
  };
  return times[status] || 'Processing...';
};

const selectCoverFromCard = async (coverId: number) => {
  if (!bookId.value) return;
  
  try {
    const result = await booksStore.selectCover(bookId.value, { cover_id: coverId });
    if (result.success) {
      // Refresh book data
      await booksStore.fetchBook(bookId.value);
      // Show success message
      if (typeof window !== 'undefined' && (window as any).$toast) {
        (window as any).$toast.success('Cover Selected!', 'Your book is now being finalized with the selected cover.');
      }
    }
  } catch (error) {
    console.error('Failed to select cover:', error);
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

const downloadBook = async () => {
  if (!book.value) return;

  try {
    // Use apiClient instead of fetch for proper session authentication
    const response = await apiClient.get(`/books/${book.value.id}/download/`, {
      responseType: 'blob', // Important for file downloads
    });

    // Create blob URL and trigger download
    const blob = new Blob([response.data], { type: 'application/pdf' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `${book.value.title || 'book'}.pdf`);
    document.body.appendChild(link);
    link.click();
    link.remove();

    // Clean up blob URL
    window.URL.revokeObjectURL(url);

    // Show success message
    if (typeof window !== 'undefined' && (window as any).$toast) {
      (window as any).$toast.success('Book downloaded!', `Downloaded "${book.value.title || 'Untitled Book'}"`);
    }
  } catch (error: any) {
    console.error('Failed to download book:', error);
    
    let errorMessage = 'Could not download the book';
    if (error.response?.data?.error) {
      errorMessage = error.response.data.error;
    }
    
    // Show error message
    if (typeof window !== 'undefined' && (window as any).$toast) {
      (window as any).$toast.error('Download failed', errorMessage);
    }
  }
};
</script>
