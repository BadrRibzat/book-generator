<template>
  <Layout>
    <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <!-- Page Header -->
        <div class="mb-8 animate-fade-in">
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
            Welcome back, {{ authStore.currentUser?.username }}!
          </h1>
          <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
            Manage your books and create amazing content
          </p>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
          <!-- Sidebar -->
          <div class="lg:col-span-1">
            <div class="bg-white dark:bg-gray-800 shadow-xl rounded-2xl overflow-hidden border border-gray-200 dark:border-gray-700 sticky top-6">
              <!-- Profile Summary -->
              <div class="bg-gradient-to-r from-primary-600 to-blue-700 px-6 py-8">
                <div class="flex flex-col items-center text-center">
                  <div class="h-20 w-20 rounded-full bg-white dark:bg-gray-700 flex items-center justify-center text-primary-600 dark:text-primary-400 text-3xl font-bold shadow-lg mb-3">
                    {{ authStore.currentUser?.username?.charAt(0).toUpperCase() }}
                  </div>
                  <h2 class="text-xl font-bold text-white">
                    {{ authStore.currentUser?.username }}
                  </h2>
                  <p class="text-primary-100 text-sm">
                    {{ authStore.currentUser?.email }}
                  </p>
                </div>
              </div>

              <!-- Navigation -->
              <nav class="p-4 space-y-2">
                <router-link
                  to="/profile"
                  class="flex items-center px-4 py-3 text-gray-700 dark:text-gray-300 hover:bg-primary-50 dark:hover:bg-primary-900/20 rounded-lg transition-colors"
                  :class="$route.path === '/profile' ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400 font-medium' : ''"
                >
                  <font-awesome-icon :icon="['fas', 'user']" class="mr-3" />
                  Dashboard
                </router-link>
                
                <router-link
                  to="/profile/mybooks"
                  class="flex items-center px-4 py-3 text-gray-700 dark:text-gray-300 hover:bg-primary-50 dark:hover:bg-primary-900/20 rounded-lg transition-colors"
                >
                  <font-awesome-icon :icon="['fas', 'book']" class="mr-3" />
                  My Books
                </router-link>
                
                <router-link
                  to="/profile/create"
                  class="flex items-center px-4 py-3 text-gray-700 dark:text-gray-300 hover:bg-primary-50 dark:hover:bg-primary-900/20 rounded-lg transition-colors"
                >
                  <font-awesome-icon :icon="['fas', 'plus-circle']" class="mr-3" />
                  Create Book
                </router-link>
                
                <button
                  @click="handleSignOut"
                  class="w-full flex items-center px-4 py-3 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
                >
                  <font-awesome-icon :icon="['fas', 'sign-out-alt']" class="mr-3" />
                  Sign Out
                </button>
              </nav>
            </div>
          </div>

          <!-- Main Content -->
          <div class="lg:col-span-3">
            <!-- Stats Cards -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
              <div class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-200 dark:border-gray-700 transform hover:scale-105 transition-transform duration-200">
                <div class="flex items-center">
                  <div class="flex-shrink-0 bg-primary-100 dark:bg-primary-900/30 rounded-lg p-3">
                    <font-awesome-icon :icon="['fas', 'book']" class="h-6 w-6 text-primary-600 dark:text-primary-400" />
                  </div>
                  <div class="ml-4">
                    <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Total Books</p>
                    <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ totalBooks }}</p>
                  </div>
                </div>
              </div>

              <div class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-200 dark:border-gray-700 transform hover:scale-105 transition-transform duration-200">
                <div class="flex items-center">
                  <div class="flex-shrink-0 bg-green-100 dark:bg-green-900/30 rounded-lg p-3">
                    <font-awesome-icon :icon="['fas', 'check-circle']" class="h-6 w-6 text-green-600 dark:text-green-400" />
                  </div>
                  <div class="ml-4">
                    <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Completed</p>
                    <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ completedBooks }}</p>
                  </div>
                </div>
              </div>

              <div class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-200 dark:border-gray-700 transform hover:scale-105 transition-transform duration-200">
                <div class="flex items-center">
                  <div class="flex-shrink-0 bg-yellow-100 dark:bg-yellow-900/30 rounded-lg p-3">
                    <font-awesome-icon :icon="['fas', 'spinner']" class="h-6 w-6 text-yellow-600 dark:text-yellow-400" />
                  </div>
                  <div class="ml-4">
                    <p class="text-sm font-medium text-gray-600 dark:text-gray-400">In Progress</p>
                    <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ inProgressBooks }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Empty State or Recent Books -->
            <div v-if="totalBooks === 0" class="bg-white dark:bg-gray-800 rounded-2xl p-12 shadow-xl border border-gray-200 dark:border-gray-700 text-center animate-fade-in">
              <div class="max-w-md mx-auto">
                <div class="mx-auto flex items-center justify-center h-24 w-24 rounded-full bg-primary-100 dark:bg-primary-900/30 mb-6">
                  <font-awesome-icon :icon="['fas', 'book-open']" class="h-12 w-12 text-primary-600 dark:text-primary-400" />
                </div>
                <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                  Start Creating Your First Book!
                </h3>
                <p class="text-gray-600 dark:text-gray-400 mb-8">
                  Choose from 15 trending niches and let AI generate professional content for you in minutes.
                </p>
                
                <!-- Quick Start Guide -->
                <div class="bg-gradient-to-r from-primary-50 to-blue-50 dark:from-primary-900/20 dark:to-blue-900/20 rounded-xl p-6 mb-8 text-left">
                  <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
                    <font-awesome-icon :icon="['fas', 'route']" class="mr-2 text-primary-600 dark:text-primary-400" />
                    How It Works
                  </h4>
                  <ol class="space-y-3">
                    <li class="flex items-start">
                      <span class="flex-shrink-0 flex items-center justify-center w-6 h-6 rounded-full bg-primary-600 text-white text-sm font-bold mr-3">1</span>
                      <span class="text-gray-700 dark:text-gray-300">
                        <strong>Choose</strong> your niche & book length (15-30 pages)
                      </span>
                    </li>
                    <li class="flex items-start">
                      <span class="flex-shrink-0 flex items-center justify-center w-6 h-6 rounded-full bg-primary-600 text-white text-sm font-bold mr-3">2</span>
                      <span class="text-gray-700 dark:text-gray-300">
                        <strong>AI generates</strong> market-optimized title & content
                      </span>
                    </li>
                    <li class="flex items-start">
                      <span class="flex-shrink-0 flex items-center justify-center w-6 h-6 rounded-full bg-primary-600 text-white text-sm font-bold mr-3">3</span>
                      <span class="text-gray-700 dark:text-gray-300">
                        <strong>Select</strong> from 3 AI-generated professional covers
                      </span>
                    </li>
                    <li class="flex items-start">
                      <span class="flex-shrink-0 flex items-center justify-center w-6 h-6 rounded-full bg-primary-600 text-white text-sm font-bold mr-3">4</span>
                      <span class="text-gray-700 dark:text-gray-300">
                        <strong>Download</strong> your print-ready PDF book
                      </span>
                    </li>
                  </ol>
                </div>

                <router-link
                  to="/profile/create"
                  class="inline-flex items-center px-8 py-4 border border-transparent text-base font-medium rounded-lg text-white bg-gradient-to-r from-primary-600 to-blue-700 hover:from-primary-700 hover:to-blue-800 transform hover:scale-105 transition-all duration-200 shadow-lg"
                >
                  <font-awesome-icon :icon="['fas', 'magic']" class="mr-2" />
                  Create Your First Book
                </router-link>
              </div>
            </div>

            <!-- Recent Books (if user has books) -->
            <div v-else class="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-xl border border-gray-200 dark:border-gray-700">
              <div class="flex items-center justify-between mb-6">
                <h2 class="text-xl font-bold text-gray-900 dark:text-white">Recent Books</h2>
                <router-link
                  to="/profile/mybooks"
                  class="text-sm text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 font-medium"
                >
                  View All →
                </router-link>
              </div>
              
              <!-- Recent books list will go here -->
              <p class="text-gray-600 dark:text-gray-400 text-center py-8">
                Your recent books will appear here
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Layout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import Layout from '../components/Layout.vue';
import apiClient from '../services/api';

const router = useRouter();
const authStore = useAuthStore();

// Stats
const totalBooks = ref(0);
const completedBooks = ref(0);
const inProgressBooks = ref(0);
const loading = ref(false);

// Load user's books on mount
onMounted(async () => {
  try {
    loading.value = true;
    const response = await apiClient.get('/books/');
    const books = response.data;
    
    totalBooks.value = books.length;
    completedBooks.value = books.filter((b: any) => b.status === 'ready').length;
    inProgressBooks.value = books.filter((b: any) => ['generating', 'content_generated', 'cover_pending'].includes(b.status)).length;
  } catch (error) {
    console.error('Failed to load books:', error);
  } finally {
    loading.value = false;
  }
});

const handleSignOut = async () => {
  const result = await authStore.signOut();
  if (result.success) {
    router.push('/auth/signin');
  }
};
</script>
