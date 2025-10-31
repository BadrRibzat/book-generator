<template>
  <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="bg-white rounded-lg shadow-xl max-w-3xl w-full p-6 relative">
      <button 
        @click="onClose" 
        class="absolute top-4 right-4 text-gray-500 hover:text-gray-700"
      >
        <font-awesome-icon :icon="['fas', 'times']" class="h-5 w-5" />
      </button>
      
      <h2 class="text-2xl font-bold text-gray-900 mb-6">Choose Your Professional AI Cover</h2>
      
      <div v-if="loading" class="text-center py-8">
        <font-awesome-icon :icon="['fas', 'spinner']" spin class="h-12 w-12 text-primary-600" />
        <p class="mt-4 text-gray-600">Loading AI-generated covers...</p>
      </div>
      
      <div v-else-if="error" class="bg-red-50 border-l-4 border-red-400 p-4 mb-4">
        <p class="text-red-700">{{ error }}</p>
      </div>
      
      <div v-else-if="covers.length === 0" class="text-center py-8">
        <font-awesome-icon :icon="['fas', 'exclamation-circle']" class="h-12 w-12 text-yellow-500" />
        <p class="mt-4 text-gray-800">No AI covers are available yet.</p>
        <p class="mt-2 text-sm text-gray-600">Professional AI covers are being generated...</p>
        <button 
          @click="handleGenerateCovers" 
          class="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
        >
          <font-awesome-icon :icon="['fas', 'redo']" class="mr-2" />
          Regenerate AI Covers
        </button>
      </div>
      
      <div v-else>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
          <div 
            v-for="cover in covers" 
            :key="cover.id"
            class="border rounded-lg overflow-hidden cursor-pointer bg-white shadow-sm transition ring-offset-2"
            :class="{ 'ring-2 ring-primary-500 shadow-lg': selectedCoverId === cover.id }"
            @click="selectCover(cover.id)"
          >
            <div class="aspect-[3/4] bg-gray-100 flex items-center justify-center relative">
              <img 
                v-if="!isPdf(cover.image_url)"
                :src="cover.image_url" 
                :alt="cover.template_style" 
                class="w-full h-full object-cover"
              />
              <object 
                v-else
                :data="cover.image_url"
                type="application/pdf"
                class="w-full h-full"
              >
                <div class="flex items-center justify-center w-full h-full text-xs text-gray-600 px-4 text-center">
                  PDF preview unavailable. Use the preview button to open this cover in a new tab.
                </div>
              </object>
              <div v-if="selectedCoverId === cover.id" class="absolute inset-0 bg-primary-500/10"></div>
            </div>
            <div class="p-3 bg-gray-50 flex items-center justify-between">
              <div>
                <p class="text-xs font-semibold text-gray-700 uppercase tracking-wide">{{ cover.template_style }} Style</p>
                <p class="text-[11px] text-gray-500 mt-1" v-if="cover.generation_params?.features?.length">
                  {{ formatFeatures(cover.generation_params.features) }}
                </p>
              </div>
              <button 
                type="button"
                class="text-xs font-medium text-primary-600 hover:text-primary-700"
                @click.stop="previewCover(cover)"
              >
                Preview
              </button>
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
import apiClient from '../services/api';
import type { Cover } from '../types';

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
  // Only fetch if we don't already have covers
  if (!booksStore.currentBook || booksStore.currentBook.id !== props.bookId || !booksStore.currentBook.covers?.length) {
    loading.value = true;
    error.value = null;
    
    try {
      await booksStore.fetchBook(props.bookId);
      if (booksStore.currentBook?.covers && booksStore.currentBook.covers.length > 0 && booksStore.currentBook.covers[0]) {
        // Auto-select first cover if available
        selectedCoverId.value = booksStore.currentBook.covers[0].id;
      }
    } catch (err: any) {
      error.value = err.message || 'Failed to load covers';
    } finally {
      loading.value = false;
    }
  } else if (booksStore.currentBook.covers && booksStore.currentBook.covers.length > 0 && booksStore.currentBook.covers[0]) {
    // Use existing covers
    selectedCoverId.value = booksStore.currentBook.covers[0].id;
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

const isPdf = (url: string | undefined | null) => {
  if (!url) return false;
  return url.toLowerCase().endsWith('.pdf');
};

const previewCover = (cover: Cover) => {
  if (typeof window !== 'undefined') {
    window.open(cover.image_url, '_blank', 'noopener');
  }
};

const formatFeatures = (features: unknown) => {
  if (!Array.isArray(features) || features.length === 0) {
    return '';
  }
  return (features as string[]).slice(0, 3).join(', ');
};
</script>