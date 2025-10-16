import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { Book, BookCreate, CoverSelect, ConfigResponse } from '../types';
import apiClient from '../services/api';

export const useBooksStore = defineStore('books', () => {
  // State
  const books = ref<Book[]>([]);
  const currentBook = ref<Book | null>(null);
  const config = ref<ConfigResponse | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  // Getters
  const allBooks = computed(() => books.value);
  const readyBooks = computed(() => books.value.filter((b) => b.can_download));
  const pendingBooks = computed(() => 
    books.value.filter((b) => ['generating', 'content_generated', 'cover_pending'].includes(b.status))
  );

  // Actions
  async function fetchConfig() {
    try {
      loading.value = true;
      error.value = null;
      const response = await apiClient.get<ConfigResponse>('/books/config/');
      config.value = response.data;
      return { success: true };
    } catch (err: any) {
      const message = err.response?.data?.error || 'Failed to fetch configuration';
      error.value = message;
      return { success: false, error: message };
    } finally {
      loading.value = false;
    }
  }

  async function fetchBooks() {
    try {
      loading.value = true;
      error.value = null;
      const response = await apiClient.get<Book[]>('/books/');
      books.value = response.data;
      return { success: true };
    } catch (err: any) {
      const message = err.response?.data?.error || 'Failed to fetch books';
      error.value = message;
      return { success: false, error: message };
    } finally {
      loading.value = false;
    }
  }

  async function fetchBook(id: number) {
    try {
      loading.value = true;
      error.value = null;
      const response = await apiClient.get<Book>(`/books/${id}/`);
      currentBook.value = response.data;
      
      // Update in books array if exists
      const index = books.value.findIndex((b) => b.id === id);
      if (index !== -1) {
        books.value[index] = response.data;
      }
      
      return { success: true, data: response.data };
    } catch (err: any) {
      const message = err.response?.data?.error || 'Failed to fetch book';
      error.value = message;
      return { success: false, error: message };
    } finally {
      loading.value = false;
    }
  }

  async function createBook(bookData: BookCreate) {
    try {
      loading.value = true;
      error.value = null;
      const response = await apiClient.post<Book>('/books/', bookData);
      books.value.unshift(response.data);
      currentBook.value = response.data;
      return { success: true, data: response.data };
    } catch (err: any) {
      const message = err.response?.data?.error || 'Failed to create book';
      error.value = message;
      return { success: false, error: message };
    } finally {
      loading.value = false;
    }
  }

  async function selectCover(bookId: number, coverData: CoverSelect) {
    try {
      loading.value = true;
      error.value = null;
      const response = await apiClient.post<Book>(`/books/${bookId}/select-cover/`, coverData);
      
      // Update book in array
      const index = books.value.findIndex((b) => b.id === bookId);
      if (index !== -1) {
        books.value[index] = response.data;
      }
      
      if (currentBook.value?.id === bookId) {
        currentBook.value = response.data;
      }
      
      return { success: true, data: response.data };
    } catch (err: any) {
      const message = err.response?.data?.error || 'Failed to select cover';
      error.value = message;
      return { success: false, error: message };
    } finally {
      loading.value = false;
    }
  }

  async function deleteBook(id: number) {
    try {
      loading.value = true;
      error.value = null;
      await apiClient.delete(`/books/${id}/`);
      
      // Remove from array
      books.value = books.value.filter((b) => b.id !== id);
      
      if (currentBook.value?.id === id) {
        currentBook.value = null;
      }
      
      return { success: true };
    } catch (err: any) {
      const message = err.response?.data?.error || 'Failed to delete book';
      error.value = message;
      return { success: false, error: message };
    } finally {
      loading.value = false;
    }
  }

  function clearError() {
    error.value = null;
  }

  function clearCurrentBook() {
    currentBook.value = null;
  }

  return {
    // State
    books,
    currentBook,
    config,
    loading,
    error,
    // Getters
    allBooks,
    readyBooks,
    pendingBooks,
    // Actions
    fetchConfig,
    fetchBooks,
    fetchBook,
    createBook,
    selectCover,
    deleteBook,
    clearError,
    clearCurrentBook,
  };
});
