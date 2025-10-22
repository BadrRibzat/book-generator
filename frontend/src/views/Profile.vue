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

        <div class="bg-white dark:bg-gray-800 shadow-xl rounded-2xl overflow-hidden border border-gray-200 dark:border-gray-700">
          <!-- Tab Navigation -->
          <div class="border-b border-gray-200 dark:border-gray-700">
            <nav class="flex">
              <router-link
                to="/profile"
                class="flex-1 py-4 px-6 text-center border-b-2 font-medium text-sm transition-colors"
                :class="$route.path === '/profile' ? 'border-primary-500 text-primary-600 dark:text-primary-400' : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'"
              >
                <font-awesome-icon :icon="['fas', 'tachometer-alt']" class="mr-2" />
                Dashboard
              </router-link>
              
              <router-link
                to="/profile/mybooks"
                class="flex-1 py-4 px-6 text-center border-b-2 font-medium text-sm transition-colors"
                :class="$route.path === '/profile/mybooks' ? 'border-primary-500 text-primary-600 dark:text-primary-400' : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'"
              >
                <font-awesome-icon :icon="['fas', 'book']" class="mr-2" />
                My Books
              </router-link>
              
              <router-link
                to="/profile/create"
                class="flex-1 py-4 px-6 text-center border-b-2 font-medium text-sm transition-colors"
                :class="$route.path === '/profile/create' ? 'border-primary-500 text-primary-600 dark:text-primary-400' : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'"
              >
                <font-awesome-icon :icon="['fas', 'plus-circle']" class="mr-2" />
                Create Book
              </router-link>
              
              <button
                @click="handleSignOut"
                class="flex-1 py-4 px-6 text-center border-b-2 font-medium text-sm text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300 transition-colors border-transparent"
              >
                <font-awesome-icon :icon="['fas', 'sign-out-alt']" class="mr-2" />
                Sign Out
              </button>
            </nav>
          </div>

          <!-- Tab Content -->
          <div class="p-6">
            <!-- Dashboard Tab -->
            <div v-if="$route.path === '/profile'" class="space-y-6">
              <!-- Welcome Header -->
              <div class="text-center">
                <h2 class="text-2xl font-bold text-gray-900 dark:text-white">
                  Welcome back, {{ authStore.currentUser?.username }}!
                </h2>
                <p class="mt-2 text-gray-600 dark:text-gray-400">
                  Here's an overview of your book creation activity
                </p>
              </div>

              <!-- Stats Cards -->
              <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="bg-gradient-to-r from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/20 rounded-xl p-6 shadow-lg border border-blue-200 dark:border-blue-800 transform hover:scale-105 transition-transform duration-200">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 bg-blue-500 rounded-lg p-3">
                      <font-awesome-icon :icon="['fas', 'book']" class="h-6 w-6 text-white" />
                    </div>
                    <div class="ml-4">
                      <p class="text-sm font-medium text-blue-800 dark:text-blue-200">Total Books</p>
                      <p class="text-2xl font-bold text-blue-900 dark:text-blue-100">{{ totalBooks }}</p>
                    </div>
                  </div>
                </div>

                <div class="bg-gradient-to-r from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/20 rounded-xl p-6 shadow-lg border border-green-200 dark:border-green-800 transform hover:scale-105 transition-transform duration-200">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 bg-green-500 rounded-lg p-3">
                      <font-awesome-icon :icon="['fas', 'check-circle']" class="h-6 w-6 text-white" />
                    </div>
                    <div class="ml-4">
                      <p class="text-sm font-medium text-green-800 dark:text-green-200">Completed</p>
                      <p class="text-2xl font-bold text-green-900 dark:text-green-100">{{ completedBooks }}</p>
                    </div>
                  </div>
                </div>

                <div class="bg-gradient-to-r from-yellow-50 to-yellow-100 dark:from-yellow-900/20 dark:to-yellow-800/20 rounded-xl p-6 shadow-lg border border-yellow-200 dark:border-yellow-800 transform hover:scale-105 transition-transform duration-200">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 bg-yellow-500 rounded-lg p-3">
                      <font-awesome-icon :icon="['fas', 'spinner']" class="h-6 w-6 text-white" />
                    </div>
                    <div class="ml-4">
                      <p class="text-sm font-medium text-yellow-800 dark:text-yellow-200">In Progress</p>
                      <p class="text-2xl font-bold text-yellow-900 dark:text-yellow-100">{{ inProgressBooks }}</p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Quick Actions -->
              <div class="bg-gradient-to-r from-primary-50 to-blue-50 dark:from-primary-900/20 dark:to-blue-900/20 rounded-xl p-6">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Quick Actions</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <router-link
                    to="/profile/create"
                    class="flex items-center p-4 bg-white dark:bg-gray-800 rounded-lg shadow hover:shadow-lg transition-shadow"
                  >
                    <div class="w-10 h-10 bg-primary-500 rounded-lg flex items-center justify-center mr-4">
                      <font-awesome-icon :icon="['fas', 'plus']" class="text-white" />
                    </div>
                    <div>
                      <h4 class="font-medium text-gray-900 dark:text-white">Create New Book</h4>
                      <p class="text-sm text-gray-600 dark:text-gray-400">Start the guided book creation process</p>
                    </div>
                  </router-link>
                  
                  <router-link
                    to="/profile/mybooks"
                    class="flex items-center p-4 bg-white dark:bg-gray-800 rounded-lg shadow hover:shadow-lg transition-shadow"
                  >
                    <div class="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center mr-4">
                      <font-awesome-icon :icon="['fas', 'list']" class="text-white" />
                    </div>
                    <div>
                      <h4 class="font-medium text-gray-900 dark:text-white">View All Books</h4>
                      <p class="text-sm text-gray-600 dark:text-gray-400">Manage your existing books</p>
                    </div>
                  </router-link>
                </div>
              </div>

              <!-- Recent Activity or Empty State -->
              <div v-if="totalBooks === 0" class="text-center py-8">
                <div class="inline-flex items-center justify-center h-16 w-16 rounded-full bg-primary-100 dark:bg-primary-900/30 mb-4">
                  <font-awesome-icon :icon="['fas', 'book-open']" class="h-8 w-8 text-primary-600 dark:text-primary-400" />
                </div>
                <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">No books yet</h3>
                <p class="text-gray-600 dark:text-gray-400 mb-4">Create your first book to get started!</p>
                <router-link
                  to="/profile/create"
                  class="inline-flex items-center px-6 py-3 border border-transparent text-sm font-medium rounded-lg text-white bg-gradient-to-r from-primary-600 to-blue-700 hover:from-primary-700 hover:to-blue-800"
                >
                  <font-awesome-icon :icon="['fas', 'magic']" class="mr-2" />
                  Create Your First Book
                </router-link>
              </div>
            </div>

            <!-- My Books Tab -->
            <div v-else-if="$route.path === '/profile/mybooks'">
              <router-view />
            </div>

            <!-- Create Book Tab -->
            <div v-else-if="$route.path === '/profile/create'">
              <router-view />
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
