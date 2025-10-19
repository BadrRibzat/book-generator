<template>
  <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="bg-white rounded-lg shadow-xl max-w-3xl w-full p-6 relative">
      <button 
        @click="onClose" 
        class="absolute top-4 right-4 text-gray-500 hover:text-gray-700"
      >
        <font-awesome-icon :icon="['fas', 'times']" class="h-5 w-5" />
      </button>
      
      <h2 class="text-2xl font-bold text-gray-900 mb-6">Select a Cover for Your Book</h2>
      
      <div v-if="loading" class="text-center py-8">
        <font-awesome-icon :icon="['fas', 'spinner']" spin class="h-12 w-12 text-primary-600" />
        <p class="mt-4 text-gray-600">Loading covers...</p>
      </div>
      
      <div v-else-if="error" class="bg-red-50 border-l-4 border-red-400 p-4 mb-4">
        <p class="text-red-700">{{ error }}</p>
      </div>
      
      <div v-else-if="covers.length === 0" class="text-center py-8">
        <font-awesome-icon :icon="['fas', 'exclamation-circle']" class="h-12 w-12 text-yellow-500" />
        <p class="mt-4 text-gray-800">No covers are available yet.</p>
        <button 
          @click="handleGenerateCovers" 
          class="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
        >
          <font-awesome-icon :icon="['fas', 'redo']" class="mr-2" />
          Generate Covers
        </button>
      </div>
      
      <div v-else>
        <div class="grid grid-cols-3 gap-4 mb-6">
          <div 
            v-for="cover in covers" 
            :key="cover.id"
            class="border rounded-lg overflow-hidden cursor-pointer"
            :class="{ 'ring-2 ring-primary-500 ring-offset-2': selectedCoverId === cover.id }"
            @click="selectCover(cover.id)"
          >
            <img :src="cover.image_url" :alt="cover.template_style" class="w-full h-auto" />
            <div class="p-2 bg-gray-50">
              <p class="text-xs text-gray-700 capitalize">{{ cover.template_style }} Style</p>
            </div>
          </div>
        </div>
        
        <div class="flex justify-end mt-4 space-x-3">
          <button 
            @click="onClose" 
            class="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
          >
            Cancel
          </button>
          <button 
            @click="confirmSelection"
            :disabled="!selectedCoverId || submitting"
            class="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="submitting" class="flex items-center">
              <font-awesome-icon :icon="['fas', 'spinner']" spin class="mr-2" />
              Saving...
            </span>
            <span v-else>Confirm Selection</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useBooksStore } from '../stores/books';
import type { Cover } from '../types';
import apiClient from '../services/api';

const props = defineProps<{
  bookId: number;
  onClose: () => void;
  onSelect: () => void;
}>();

const booksStore = useBooksStore();
const covers = computed(() => booksStore.currentBook?.covers || []);
const selectedCoverId = ref<number | null>(null);
const loading = ref(false);
const submitting = ref(false);
const error = ref<string | null>(null);

onMounted(async () => {
  loading.value = true;
  error.value = null;
  
  try {
    await booksStore.fetchBook(props.bookId);
    if (booksStore.currentBook?.covers && booksStore.currentBook?.covers.length > 0) {
      // Auto-select first cover if available
      selectedCoverId.value = booksStore.currentBook.covers[0].id;
    }
  } catch (err) {
    error.value = 'Failed to load covers. Please try again.';
    console.error(err);
  } finally {
    loading.value = false;
  }
});

const selectCover = (coverId: number) => {
  selectedCoverId.value = coverId;
};

const confirmSelection = async () => {
  if (!selectedCoverId.value) return;
  
  submitting.value = true;
  error.value = null;
  
  try {
    const result = await booksStore.selectCover(props.bookId, {
      cover_id: selectedCoverId.value,
    });
    
    if (result.success) {
      props.onSelect();
    } else {
      error.value = result.error || 'Failed to select cover';
    }
  } catch (err: any) {
    error.value = err.message || 'An unexpected error occurred';
    console.error(err);
  } finally {
    submitting.value = false;
  }
};

const handleGenerateCovers = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    await apiClient.post(`/books/${props.bookId}/regenerate-covers/`);
    await booksStore.fetchBook(props.bookId);
  } catch (err: any) {
    error.value = err.message || 'Failed to generate covers';
    console.error(err);
  } finally {
    loading.value = false;
  }
};
</script>