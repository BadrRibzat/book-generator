<template>
  <Layout>
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <!-- Page Header -->
        <div class="mb-8 animate-fade-in">
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Profile Settings</h1>
          <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
            Manage your account settings and preferences
          </p>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- Profile Card -->
          <div class="lg:col-span-2">
            <div class="bg-white dark:bg-gray-800 shadow-xl rounded-2xl overflow-hidden border border-gray-200 dark:border-gray-700 animate-slide-up">
              <!-- Header with gradient -->
              <div class="bg-gradient-to-r from-primary-600 to-blue-700 px-6 py-8">
                <div class="flex items-center space-x-4">
                  <div class="h-20 w-20 rounded-full bg-white dark:bg-gray-700 flex items-center justify-center text-primary-600 dark:text-primary-400 text-3xl font-bold shadow-lg">
                    {{ authStore.currentUser?.username?.charAt(0).toUpperCase() }}
                  </div>
                  <div>
                    <h2 class="text-2xl font-bold text-white">
                      {{ authStore.currentUser?.username }}
                    </h2>
                    <p class="text-primary-100">
                      {{ authStore.currentUser?.email }}
                    </p>
                  </div>
                </div>
              </div>

              <!-- Profile Details -->
              <div class="px-6 py-6 space-y-6">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div class="group">
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      <font-awesome-icon :icon="['fas', 'user']" class="mr-2 text-primary-600 dark:text-primary-400" />
                      Username
                    </label>
                    <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg border border-gray-200 dark:border-gray-600">
                      <p class="text-gray-900 dark:text-white font-medium">
                        {{ authStore.currentUser?.username }}
                      </p>
                    </div>
                  </div>

                  <div class="group">
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      <font-awesome-icon :icon="['fas', 'at']" class="mr-2 text-primary-600 dark:text-primary-400" />
                      Email Address
                    </label>
                    <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg border border-gray-200 dark:border-gray-600">
                      <p class="text-gray-900 dark:text-white font-medium">
                        {{ authStore.currentUser?.email }}
                      </p>
                    </div>
                  </div>

                  <div class="group">
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      <font-awesome-icon :icon="['fas', 'database']" class="mr-2 text-primary-600 dark:text-primary-400" />
                      User ID
                    </label>
                    <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg border border-gray-200 dark:border-gray-600">
                      <p class="text-gray-900 dark:text-white font-mono text-sm">
                        #{{ authStore.currentUser?.id }}
                      </p>
                    </div>
                  </div>

                  <div class="group">
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      <font-awesome-icon :icon="['fas', 'check-circle']" class="mr-2 text-green-600 dark:text-green-400" />
                      Account Status
                    </label>
                    <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg border border-gray-200 dark:border-gray-600">
                      <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400">
                        <font-awesome-icon :icon="['fas', 'check-circle']" class="mr-1" />
                        Active
                      </span>
                    </div>
                  </div>
                </div>

                <!-- Action Buttons -->
                <div class="flex flex-wrap gap-3 pt-4 border-t border-gray-200 dark:border-gray-700">
                  <button
                    class="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-lg text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 transition-all duration-200"
                  >
                    <font-awesome-icon :icon="['fas', 'user']" class="mr-2" />
                    Edit Profile
                  </button>
                  <button
                    class="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-lg text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 transition-all duration-200"
                  >
                    <font-awesome-icon :icon="['fas', 'lock']" class="mr-2" />
                    Change Password
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick Actions & Theme -->
          <div class="space-y-6">
            <!-- Theme Selector -->
            <div class="bg-white dark:bg-gray-800 shadow-xl rounded-2xl p-6 border border-gray-200 dark:border-gray-700 animate-slide-up">
              <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4 flex items-center">
                <font-awesome-icon :icon="['fas', themeStore.isDark() ? 'moon' : 'sun']" class="mr-2 text-primary-600 dark:text-primary-400" />
                Appearance
              </h3>
              <div class="space-y-3">
                <button
                  @click="themeStore.setTheme('light')"
                  :class="[
                    'w-full flex items-center justify-between p-3 rounded-lg border-2 transition-all duration-200',
                    !themeStore.isDark() 
                      ? 'border-primary-600 bg-primary-50 dark:bg-primary-900/20' 
                      : 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500'
                  ]"
                >
                  <div class="flex items-center">
                    <font-awesome-icon :icon="['fas', 'sun']" class="mr-3 text-yellow-500" />
                    <span class="font-medium text-gray-900 dark:text-white">Light Mode</span>
                  </div>
                  <font-awesome-icon 
                    v-if="!themeStore.isDark()" 
                    :icon="['fas', 'check-circle']" 
                    class="text-primary-600" 
                  />
                </button>

                <button
                  @click="themeStore.setTheme('dark')"
                  :class="[
                    'w-full flex items-center justify-between p-3 rounded-lg border-2 transition-all duration-200',
                    themeStore.isDark() 
                      ? 'border-primary-600 bg-primary-50 dark:bg-primary-900/20' 
                      : 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500'
                  ]"
                >
                  <div class="flex items-center">
                    <font-awesome-icon :icon="['fas', 'moon']" class="mr-3 text-indigo-500" />
                    <span class="font-medium text-gray-900 dark:text-white">Dark Mode</span>
                  </div>
                  <font-awesome-icon 
                    v-if="themeStore.isDark()" 
                    :icon="['fas', 'check-circle']" 
                    class="text-primary-600" 
                  />
                </button>
              </div>
            </div>

            <!-- Quick Stats -->
            <div class="bg-white dark:bg-gray-800 shadow-xl rounded-2xl p-6 border border-gray-200 dark:border-gray-700">
              <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4 flex items-center">
                <font-awesome-icon :icon="['fas', 'chart-line']" class="mr-2 text-primary-600 dark:text-primary-400" />
                Quick Stats
              </h3>
              <div class="space-y-4">
                <div class="flex items-center justify-between">
                  <div class="flex items-center">
                    <div class="h-10 w-10 rounded-lg bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center mr-3">
                      <font-awesome-icon :icon="['fas', 'book']" class="text-blue-600 dark:text-blue-400" />
                    </div>
                    <span class="text-gray-700 dark:text-gray-300 font-medium">Books Created</span>
                  </div>
                  <span class="text-2xl font-bold text-gray-900 dark:text-white">0</span>
                </div>

                <div class="flex items-center justify-between">
                  <div class="flex items-center">
                    <div class="h-10 w-10 rounded-lg bg-green-100 dark:bg-green-900/30 flex items-center justify-center mr-3">
                      <font-awesome-icon :icon="['fas', 'download']" class="text-green-600 dark:text-green-400" />
                    </div>
                    <span class="text-gray-700 dark:text-gray-300 font-medium">Downloads</span>
                  </div>
                  <span class="text-2xl font-bold text-gray-900 dark:text-white">0</span>
                </div>
              </div>
            </div>

            <!-- Danger Zone -->
            <div class="bg-white dark:bg-gray-800 shadow-xl rounded-2xl p-6 border-2 border-red-200 dark:border-red-900">
              <h3 class="text-lg font-bold text-red-700 dark:text-red-400 mb-4 flex items-center">
                <font-awesome-icon :icon="['fas', 'exclamation-circle']" class="mr-2" />
                Danger Zone
              </h3>
              <button
                @click="handleSignOut"
                :disabled="authStore.loading"
                class="w-full inline-flex items-center justify-center px-4 py-3 border border-transparent text-sm font-medium rounded-lg text-white bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-[1.02] active:scale-[0.98] transition-all duration-200 shadow-lg"
              >
                <font-awesome-icon :icon="['fas', 'sign-out-alt']" class="mr-2" />
                <span v-if="!authStore.loading">Sign Out</span>
                <span v-else>Signing out...</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Layout>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { useThemeStore } from '../stores/theme';
import Layout from '../components/Layout.vue';

const router = useRouter();
const authStore = useAuthStore();
const themeStore = useThemeStore();

const handleSignOut = async () => {
  const result = await authStore.signOut();
  
  if (result.success) {
    router.push('/auth/signin');
  }
};
</script>
