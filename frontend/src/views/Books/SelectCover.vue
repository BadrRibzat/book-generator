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
        <div class="mb-6">
          <h1 class="text-3xl font-bold text-gray-900">Select a Cover</h1>
          <p class="mt-2 text-sm text-gray-600">
            Choose your favorite cover design for: <strong>{{ book?.title }}</strong>
          </p>
        </div>

        <div v-if="booksStore.loading" class="text-center py-12">
          <font-awesome-icon :icon="['fas', 'spinner']" spin class="h-12 w-12 text-primary-600" />
          <p class="mt-2 text-gray-600">Loading covers...</p>
        </div>

        <div v-else-if="booksStore.error" class="rounded-md bg-red-50 p-4">
          <div class="flex">
            <font-awesome-icon :icon="['fas', 'exclamation-circle']" class="h-5 w-5 text-red-400" />
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800">{{ booksStore.error }}</h3>
            </div>
          </div>
        </div>

        <div v-else-if="book && book.covers.length > 0" class="space-y-6">
          <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            <div
              v-for="cover in book.covers"
              :key="cover.id"
              class="bg-white overflow-hidden shadow rounded-lg hover:shadow-xl transition-shadow duration-200 cursor-pointer"
              :class="{ 'ring-4 ring-primary-500': selectedCoverId === cover.id }"
              @click="selectedCoverId = cover.id"
            >
              <div class="aspect-[3/4] relative">
                <img
                  :src="cover.image_url"
                  :alt="`Cover ${cover.template_style}`"
                  class="w-full h-full object-cover"
                />
                <div
                  v-if="selectedCoverId === cover.id"
                  class="absolute inset-0 bg-primary-600 bg-opacity-20 flex items-center justify-center"
                >
                  <font-awesome-icon
                    :icon="['fas', 'check-circle']"
                    class="h-16 w-16 text-white"
                  />
                </div>
              </div>
              <div class="p-4">
                <p class="text-sm font-medium text-gray-900 capitalize">
                  {{ cover.template_style }} Style
                </p>
                <p class="text-xs text-gray-500 mt-1">
                  Click to select this cover
                </p>
              </div>
            </div>
          </div>

          <div class="bg-white shadow sm:rounded-lg">
            <div class="px-4 py-5 sm:p-6 flex justify-between items-center">
              <div>
                <h3 class="text-lg leading-6 font-medium text-gray-900">
                  {{ selectedCoverId ? 'Cover selected' : 'No cover selected' }}
                </h3>
                <p class="mt-1 text-sm text-gray-500">
                  {{ selectedCoverId ? 'Click the button to confirm your selection' : 'Click on a cover above to select it' }}
                </p>
              </div>
              <div class="flex space-x-3">
                <router-link
                  :to="`/books/${id}`"
                  class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                >
                  Cancel
                </router-link>
                <button
                  @click="handleSelectCover"
                  :disabled="!selectedCoverId || booksStore.loading"
                  class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <span v-if="!booksStore.loading">Confirm Selection</span>
                  <span v-else class="flex items-center">
                    <font-awesome-icon :icon="['fas', 'spinner']" spin class="mr-2" />
                    Processing...
                  </span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="text-center py-12">
          <font-awesome-icon :icon="['fas', 'exclamation-circle']" class="h-16 w-16 text-gray-400" />
          <h3 class="mt-2 text-sm font-medium text-gray-900">No covers available</h3>
          <p class="mt-1 text-sm text-gray-500">
            Covers are still being generated. Please check back in a moment.
          </p>
          <div class="mt-6">
            <router-link
              :to="`/books/${id}`"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
            >
              Back to Book Details
            </router-link>
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

interface Props {
  id: string;
}

const props = defineProps<Props>();
const router = useRouter();
const booksStore = useBooksStore();

const selectedCoverId = ref<number | null>(null);
const book = computed(() => booksStore.currentBook);

onMounted(async () => {
  await booksStore.fetchBook(parseInt(props.id));
});

const handleSelectCover = async () => {
  if (!selectedCoverId.value) return;

  booksStore.clearError();
  
  const result = await booksStore.selectCover(parseInt(props.id), {
    cover_id: selectedCoverId.value,
  });

  if (result.success) {
    router.push(`/books/${props.id}`);
  }
};
</script>
