<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <router-link to="/books" class="flex items-center">
              <font-awesome-icon :icon="['fas', 'book']" class="h-6 w-6 text-primary-600" />
              <span class="ml-2 text-xl font-bold text-gray-900">Book Generator</span>
            </router-link>
          </div>
          <div class="flex items-center space-x-4">
            <router-link
              to="/books"
              class="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium"
            >
              <font-awesome-icon :icon="['fas', 'book']" class="mr-1" />
              My Books
            </router-link>
            <router-link
              to="/profile"
              class="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium"
            >
              <font-awesome-icon :icon="['fas', 'user']" class="mr-1" />
              Profile
            </router-link>
          </div>
        </div>
      </div>
    </nav>

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
                  </dd>
                </div>
              </dl>
            </div>
          </div>

          <div v-if="book.status === 'content_generated' && book.covers.length > 0" class="bg-white shadow sm:rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                Select a Cover
              </h3>
              <p class="text-sm text-gray-500 mb-6">
                Choose one of the generated covers for your book.
              </p>
              <router-link
                :to="`/books/${book.id}/covers`"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
              >
                Select Cover
              </router-link>
            </div>
          </div>

          <div v-if="book.selected_cover" class="bg-white shadow sm:rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                Selected Cover
              </h3>
              <img
                :src="book.selected_cover.image_url"
                :alt="`${book.title} cover`"
                class="max-w-sm rounded-lg shadow-lg"
              />
            </div>
          </div>

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
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useBooksStore } from '../../stores/books';
import type { BookStatus, Domain, SubNiche } from '../../types';

interface Props {
  id: string;
}

const props = defineProps<Props>();
const router = useRouter();
const booksStore = useBooksStore();

const deleting = ref(false);
const book = computed(() => booksStore.currentBook);

onMounted(async () => {
  await booksStore.fetchBook(parseInt(props.id));
});

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

const handleDelete = async () => {
  if (!confirm('Are you sure you want to delete this book? This action cannot be undone.')) {
    return;
  }

  deleting.value = true;
  const result = await booksStore.deleteBook(parseInt(props.id));
  deleting.value = false;

  if (result.success) {
    router.push('/books');
  }
};
</script>
