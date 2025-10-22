<template>
  <Layout>
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <!-- Page Header -->
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4 animate-fade-in">
          <div>
            <h1 class="text-3xl font-bold text-gray-900 dark:text-white">My Books</h1>
            <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
              Professional AI-generated books with 15-30 pages and custom covers
            </p>
          </div>
          <router-link
            to="/profile/create"
            class="inline-flex items-center px-6 py-3 border border-transparent text-sm font-medium rounded-lg text-white bg-gradient-to-r from-primary-600 to-primary-700 hover:from-primary-700 hover:to-primary-800 transform hover:scale-[1.02] active:scale-[0.98] transition-all duration-200 shadow-lg hover:shadow-xl"
          >
            <font-awesome-icon :icon="['fas', 'plus']" class="mr-2" />
            Create New Book
          </router-link>
        </div>

        <!-- Loading State -->
        <div v-if="booksStore.loading" class="text-center py-12 animate-fade-in">
          <font-awesome-icon :icon="['fas', 'spinner']" spin class="h-12 w-12 text-primary-600 dark:text-primary-400" />
          <p class="mt-4 text-gray-600 dark:text-gray-400">Loading books...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="booksStore.error" class="rounded-lg bg-red-50 dark:bg-red-900/20 p-6 border border-red-200 dark:border-red-800 animate-scale-in">
          <div class="flex">
            <font-awesome-icon :icon="['fas', 'exclamation-circle']" class="h-5 w-5 text-red-400 dark:text-red-500 mt-0.5" />
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800 dark:text-red-400">{{ booksStore.error }}</h3>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else-if="booksStore.allBooks.length === 0" class="text-center py-16 bg-white dark:bg-gray-800 rounded-2xl shadow-xl border border-gray-200 dark:border-gray-700 animate-slide-up">
          <div class="inline-flex items-center justify-center h-20 w-20 rounded-full bg-primary-100 dark:bg-primary-900/30 mb-4">
            <font-awesome-icon :icon="['fas', 'book']" class="h-10 w-10 text-primary-600 dark:text-primary-400" />
          </div>
          <h3 class="text-xl font-medium text-gray-900 dark:text-white">No books yet</h3>
          <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">Get started by creating your first book.</p>
          <div class="mt-6">
            <router-link
              to="/profile/create"
              class="inline-flex items-center px-6 py-3 border border-transparent text-sm font-medium rounded-lg text-white bg-gradient-to-r from-primary-600 to-primary-700 hover:from-primary-700 hover:to-primary-800 transform hover:scale-[1.02] active:scale-[0.98] transition-all duration-200 shadow-lg"
            >
              <font-awesome-icon :icon="['fas', 'plus']" class="mr-2" />
              Create New Book
            </router-link>
          </div>
        </div>

        <!-- Books Grid -->
        <div v-else class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <div
            v-for="book in booksStore.allBooks"
            :key="book.id"
            class="bg-white dark:bg-gray-800 overflow-hidden shadow-xl rounded-2xl hover:shadow-2xl transition-all duration-300 border border-gray-200 dark:border-gray-700 transform hover:scale-[1.02] animate-slide-up"
          >
            <div class="p-6">
              <!-- Status Badge -->
              <div class="flex items-center justify-between mb-4">
                <span
                  :class="getStatusClass(book.status)"
                  class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium"
                >
                  <font-awesome-icon
                    :icon="['fas', getStatusIcon(book.status)]"
                    :spin="book.status === 'generating'"
                    class="mr-1.5"
                  />
                  {{ getStatusLabel(book.status) }}
                </span>
              </div>

              <!-- Book Title -->
              <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-3 line-clamp-2 min-h-[3.5rem]">
                {{ book.title }}
              </h3>

              <!-- Book Details -->
              <div class="space-y-2 text-sm text-gray-600 dark:text-gray-400 mb-4">
                <div class="flex items-center">
                  <font-awesome-icon :icon="['fas', 'book-open']" class="mr-2 text-primary-600 dark:text-primary-400 w-4" />
                  <span>{{ formatDomain(book.domain) }}</span>
                </div>
                <div class="flex items-center">
                  <font-awesome-icon :icon="['fas', 'palette']" class="mr-2 text-primary-600 dark:text-primary-400 w-4" />
                  <span>{{ formatNiche(book.sub_niche) }}</span>
                </div>
                <div class="flex items-center">
                  <font-awesome-icon :icon="['fas', 'file-pdf']" class="mr-2 text-primary-600 dark:text-primary-400 w-4" />
                  <span>{{ book.page_length }} pages</span>
                </div>
                <div class="flex items-center text-xs">
                  <font-awesome-icon :icon="['fas', 'check-circle']" class="mr-2 text-green-600 dark:text-green-400 w-4" />
                  <span>Created {{ formatDate(book.created_at) }}</span>
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="flex space-x-2 pt-4 border-t border-gray-200 dark:border-gray-700">
                <router-link
                  :to="`/profile/books/${book.id}`"
                  class="flex-1 inline-flex justify-center items-center px-3 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-lg text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 transition-all duration-200"
                >
                  <font-awesome-icon :icon="['fas', 'eye']" class="mr-1" />
                  View
                </router-link>

                <a
                  v-if="book.can_download"
                  :href="book.download_url || '#'"
                  class="flex-1 inline-flex justify-center items-center px-3 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 transition-all duration-200 shadow-md"
                >
                  <font-awesome-icon :icon="['fas', 'download']" class="mr-1" />
                  Download
                </a>

                <button
                  @click="confirmDeleteBook(book)"
                  class="inline-flex justify-center items-center px-3 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-red-600 hover:bg-red-700 transition-all duration-200"
                  title="Delete book"
                >
                  <font-awesome-icon :icon="['fas', 'trash']" class="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md w-full mx-4">
        <div class="flex items-center space-x-3 mb-4">
          <div class="w-10 h-10 bg-red-100 dark:bg-red-900 rounded-full flex items-center justify-center">
            <font-awesome-icon :icon="['fas', 'exclamation-triangle']" class="w-5 h-5 text-red-600 dark:text-red-400" />
          </div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Delete Book</h3>
        </div>
        
        <p class="text-gray-600 dark:text-gray-300 mb-6">
          Are you sure you want to delete <strong>"{{ bookToDelete?.title || 'Untitled Book' }}"</strong>? 
          This action cannot be undone.
        </p>
        
        <div class="flex space-x-3">
          <button
            @click="cancelDelete"
            class="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
            :disabled="isDeleting"
          >
            Cancel
          </button>
          <button
            @click="deleteBook"
            class="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="isDeleting"
          >
            <span v-if="isDeleting" class="flex items-center justify-center">
              <font-awesome-icon :icon="['fas', 'spinner']" class="animate-spin mr-2" />
              Deleting...
            </span>
            <span v-else>Delete Book</span>
          </button>
        </div>
      </div>
    </div>
  </Layout>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useBooksStore } from '../../stores/books';
import Layout from '../../components/Layout.vue';
import type { BookStatus, Domain, SubNiche } from '../../types';

const router = useRouter();
const booksStore = useBooksStore();

// Delete functionality
const showDeleteModal = ref(false);
const bookToDelete = ref<any>(null);
const isDeleting = ref(false);

const confirmDeleteBook = (book: any) => {
  bookToDelete.value = book;
  showDeleteModal.value = true;
};

const deleteBook = async () => {
  if (!bookToDelete.value) return;
  
  try {
    isDeleting.value = true;
    await booksStore.deleteBook(bookToDelete.value.id);
    
    showDeleteModal.value = false;
    bookToDelete.value = null;
  } catch (error) {
    console.error('Failed to delete book:', error);
    alert('Failed to delete book. Please try again.');
  } finally {
    isDeleting.value = false;
  }
};

const cancelDelete = () => {
  showDeleteModal.value = false;
  bookToDelete.value = null;
};

onMounted(async () => {
  const result = await booksStore.fetchBooks();
  
  // If user has no books, redirect to create page to encourage first book
  if (result.success && booksStore.allBooks.length === 0) {
    router.push('/profile/create');
  }
});

const getStatusClass = (status: BookStatus) => {
  const classes: Record<BookStatus, string> = {
    draft: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300',
    generating: 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400',
    content_generated: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
    cover_pending: 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-400',
    ready: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
    error: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400',
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
    generating: 'Generating',
    content_generated: 'Content Ready',
    cover_pending: 'Select Cover',
    ready: 'Ready',
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
  return new Date(date).toLocaleDateString();
};
</script>
