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
        <FormAlert :message="authStore.error" variant="error" />

        <form class="space-y-5" @submit.prevent="handleSubmit">
          <TextField id="username" label="Username" icon="user" placeholder="Choose a username" v-model="form.username" autocomplete="username" />

          <TextField id="email" label="Email address" icon="at" type="email" placeholder="you@example.com" v-model="form.email" autocomplete="email" />

          <PasswordField id="password" label="Password" v-model="form.password" autocomplete="new-password" />

          <PasswordField id="password2" label="Confirm Password" v-model="form.password2" autocomplete="new-password" />

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
  </div>
  </Layout>
</template>

<script setup lang="ts">
import { reactive } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../../stores/auth';
import Layout from '../../components/Layout.vue';
import type { UserRegistration } from '../../types';
import FormAlert from '../../components/ui/FormAlert.vue';
import TextField from '../../components/ui/TextField.vue';
import PasswordField from '../../components/ui/PasswordField.vue';

const router = useRouter();
const authStore = useAuthStore();

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
    router.push('/auth/signin');
  }
};
</script>
