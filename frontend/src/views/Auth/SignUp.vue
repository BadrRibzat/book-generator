<template>
  <Layout>
    <div class="min-h-[calc(100vh-4rem)] flex items-center justify-center bg-gradient-to-br from-primary-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 py-12 px-4 sm:px-6 lg:px-8 transition-colors duration-200">
      <div class="max-w-md w-full space-y-8 animate-fade-in">
      <!-- Logo and Title -->
      <div class="text-center">
        <div class="flex justify-center mb-6">
          <div class="bg-gradient-to-br from-primary-500 to-primary-700 p-4 rounded-2xl shadow-lg transform hover:scale-105 transition-transform duration-200">
            <font-awesome-icon :icon="['fas', 'user-plus']" class="h-10 w-10 text-white" />
          </div>
        </div>
        <h2 class="text-3xl font-extrabold text-gray-900 dark:text-white mb-2">
          Create your account
        </h2>
        <p class="text-sm text-gray-600 dark:text-gray-400">
          Already have an account?
          <router-link to="/auth/signin" class="font-medium text-primary-600 dark:text-primary-400 hover:text-primary-500 transition-colors">
            Sign in
          </router-link>
        </p>
      </div>

      <!-- Form Card -->
      <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 space-y-6 backdrop-blur-sm bg-opacity-90 dark:bg-opacity-90 border border-gray-200 dark:border-gray-700 animate-slide-up">
        <!-- Error Message -->
        <div v-if="authStore.error" class="rounded-lg bg-red-50 dark:bg-red-900/30 p-4 animate-scale-in">
          <div class="flex">
            <font-awesome-icon :icon="['fas', 'exclamation-circle']" class="h-5 w-5 text-red-400" />
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800 dark:text-red-300">{{ authStore.error }}</h3>
            </div>
          </div>
        </div>

        <form class="space-y-5" @submit.prevent="handleSubmit">
          <!-- Username Field -->
          <div class="group">
            <label for="username" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Username
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <font-awesome-icon :icon="['fas', 'user']" class="h-5 w-5 text-gray-400 dark:text-gray-500 group-focus-within:text-primary-500 transition-colors" />
              </div>
              <input
                id="username"
                v-model="form.username"
                name="username"
                type="text"
                required
                class="appearance-none block w-full pl-10 pr-3 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200"
                placeholder="Choose a username"
              />
            </div>
          </div>

          <!-- Email Field -->
          <div class="group">
            <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Email address
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <font-awesome-icon :icon="['fas', 'at']" class="h-5 w-5 text-gray-400 dark:text-gray-500 group-focus-within:text-primary-500 transition-colors" />
              </div>
              <input
                id="email"
                v-model="form.email"
                name="email"
                type="email"
                required
                class="appearance-none block w-full pl-10 pr-3 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200"
                placeholder="you@example.com"
              />
            </div>
          </div>

          <!-- Password Field -->
          <div class="group">
            <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Password
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <font-awesome-icon :icon="['fas', 'lock']" class="h-5 w-5 text-gray-400 dark:text-gray-500 group-focus-within:text-primary-500 transition-colors" />
              </div>
              <input
                id="password"
                v-model="form.password"
                name="password"
                :type="showPassword ? 'text' : 'password'"
                required
                class="appearance-none block w-full pl-10 pr-10 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200"
                placeholder="••••••••"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute inset-y-0 right-0 pr-3 flex items-center"
              >
                <font-awesome-icon 
                  :icon="['fas', showPassword ? 'eye-slash' : 'eye']" 
                  class="h-5 w-5 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300 transition-colors cursor-pointer" 
                />
              </button>
            </div>
          </div>

          <!-- Confirm Password Field -->
          <div class="group">
            <label for="password2" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Confirm Password
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <font-awesome-icon :icon="['fas', 'lock']" class="h-5 w-5 text-gray-400 dark:text-gray-500 group-focus-within:text-primary-500 transition-colors" />
              </div>
              <input
                id="password2"
                v-model="form.password2"
                name="password2"
                :type="showPassword2 ? 'text' : 'password'"
                required
                class="appearance-none block w-full pl-10 pr-10 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200"
                placeholder="••••••••"
              />
              <button
                type="button"
                @click="showPassword2 = !showPassword2"
                class="absolute inset-y-0 right-0 pr-3 flex items-center"
              >
                <font-awesome-icon 
                  :icon="['fas', showPassword2 ? 'eye-slash' : 'eye']" 
                  class="h-5 w-5 text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300 transition-colors cursor-pointer" 
                />
              </button>
            </div>
          </div>

          <!-- Submit Button -->
          <div>
            <button
              type="submit"
              :disabled="authStore.loading"
              class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-gradient-to-r from-primary-600 to-primary-700 hover:from-primary-700 hover:to-primary-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-[1.02] active:scale-[0.98] transition-all duration-200 shadow-lg hover:shadow-xl"
            >
              <span v-if="!authStore.loading" class="flex items-center">
                <font-awesome-icon :icon="['fas', 'user-plus']" class="mr-2" />
                Create Account
              </span>
              <span v-else class="flex items-center">
                <font-awesome-icon :icon="['fas', 'spinner']" spin class="mr-2" />
                Creating account...
              </span>
            </button>
          </div>
        </form>

        <!-- Divider -->
        <div class="relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-300 dark:border-gray-600"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-2 bg-white dark:bg-gray-800 text-gray-500 dark:text-gray-400">
              Free to start, upgrade anytime
            </span>
          </div>
        </div>

        <!-- Benefits -->
        <div class="grid grid-cols-2 gap-4 text-xs text-gray-600 dark:text-gray-400">
          <div class="flex items-center">
            <font-awesome-icon :icon="['fas', 'check-circle']" class="text-green-500 mr-2" />
            <span>No credit card</span>
          </div>
          <div class="flex items-center">
            <font-awesome-icon :icon="['fas', 'check-circle']" class="text-green-500 mr-2" />
            <span>3 books free</span>
          </div>
          <div class="flex items-center">
            <font-awesome-icon :icon="['fas', 'check-circle']" class="text-green-500 mr-2" />
            <span>AI-powered</span>
          </div>
          <div class="flex items-center">
            <font-awesome-icon :icon="['fas', 'check-circle']" class="text-green-500 mr-2" />
            <span>Cancel anytime</span>
          </div>
        </div>
      </div>
    </div>
  </Layout>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../../stores/auth';
import Layout from '../../components/Layout.vue';
import type { UserRegistration } from '../../types';

const router = useRouter();
const authStore = useAuthStore();

const showPassword = ref(false);
const showPassword2 = ref(false);

const form = reactive<UserRegistration>({
  username: '',
  email: '',
  password: '',
  password2: '',
});

const handleSubmit = async () => {
  authStore.clearError();
  
  if (form.password !== form.password2) {
    authStore.error = 'Passwords do not match';
    return;
  }

  const result = await authStore.signUp(form);
  
  if (result.success) {
    router.push('/books');
  }
};
</script>
