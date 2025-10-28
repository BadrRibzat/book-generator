<template>
  <Layout>
    <div class="min-h-[calc(100vh-4rem)] flex items-center justify-center bg-gradient-to-br from-primary-50 via-white to-blue-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 py-12 px-4 sm:px-6 lg:px-8 transition-colors duration-200">
      <div class="max-w-md w-full space-y-8 animate-fade-in">
      <!-- Logo and Title -->
      <div class="text-center">
        <div class="flex justify-center mb-6">
          <div class="bg-gradient-to-br from-primary-500 to-blue-700 p-4 rounded-2xl shadow-lg transform hover:scale-105 transition-transform duration-200">
            <font-awesome-icon :icon="['fas', 'sign-in-alt']" class="h-10 w-10 text-white" />
          </div>
        </div>
        <h2 class="text-3xl font-extrabold text-gray-900 dark:text-white mb-2">
          Welcome back
        </h2>
        <p class="text-sm text-gray-600 dark:text-gray-400">
          Don't have an account?
          <router-link to="/auth/signup" class="font-medium text-primary-600 dark:text-primary-400 hover:text-primary-500 transition-colors">
            Sign up for free
          </router-link>
        </p>
      </div>

      <!-- Form Card -->
      <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 space-y-6 backdrop-blur-sm bg-opacity-90 dark:bg-opacity-90 border border-gray-200 dark:border-gray-700 animate-slide-up">
        <FormAlert :message="authStore.error" variant="error" />

        <form class="space-y-5" @submit.prevent="handleSubmit">
          <!-- Username Field -->
          <TextField id="username" label="Username" icon="user" placeholder="Enter your username" v-model="form.username" autocomplete="username" />

          <!-- Password Field -->
          <div>
            <div class="flex items-center justify-between mb-2">
              <label for="password" class="block text-sm font-medium text-neutral-700 dark:text-neutral-300">Password</label>
              <a href="#" class="text-xs text-primary-600 dark:text-primary-400 hover:text-primary-500 transition-colors">Forgot password?</a>
            </div>
            <PasswordField id="password" placeholder="Enter your password" v-model="form.password" autocomplete="current-password" />
          </div>

          <!-- Remember Me -->
          <div class="flex items-center">
            <input
              id="remember-me"
              name="remember-me"
              type="checkbox"
              class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded cursor-pointer"
            />
            <label for="remember-me" class="ml-2 block text-sm text-gray-700 dark:text-gray-300 cursor-pointer">
              Remember me for 30 days
            </label>
          </div>

          <!-- Submit Button -->
          <div>
            <button
              type="submit"
              :disabled="authStore.loading"
              class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-gradient-to-r from-primary-600 to-blue-700 hover:from-primary-700 hover:to-blue-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-[1.02] active:scale-[0.98] transition-all duration-200 shadow-lg hover:shadow-xl"
            >
              <span v-if="!authStore.loading" class="flex items-center">
                <font-awesome-icon :icon="['fas', 'sign-in-alt']" class="mr-2" />
                Sign in to your account
              </span>
              <span v-else class="flex items-center">
                <font-awesome-icon :icon="['fas', 'spinner']" spin class="mr-2" />
                Signing in...
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
              Secure authentication
            </span>
          </div>
        </div>

        <!-- Trust Badges -->
        <div class="grid grid-cols-3 gap-4 text-center text-xs text-gray-500 dark:text-gray-400">
          <div>
            <font-awesome-icon :icon="['fas', 'lock']" class="text-green-500 mb-1" />
            <div>Encrypted</div>
          </div>
          <div>
            <font-awesome-icon :icon="['fas', 'shield-alt']" class="text-blue-500 mb-1" />
            <div>Secure</div>
          </div>
          <div>
            <font-awesome-icon :icon="['fas', 'user-check']" class="text-purple-500 mb-1" />
            <div>Private</div>
          </div>
        </div>
      </div>

      <!-- Additional Help -->
      <div class="text-center text-sm text-gray-600 dark:text-gray-400">
        <p>
          Having trouble?
          <a href="#" class="text-primary-600 dark:text-primary-400 hover:text-primary-500 transition-colors">
            Contact support
          </a>
        </p>
      </div>
    </div>
  </div>
  </Layout>
</template>

<script setup lang="ts">
import { reactive } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '../../stores/auth';
import type { UserLogin } from '../../types';
import Layout from '../../components/Layout.vue';
// Import UI components used in the template
import FormAlert from '../../components/ui/FormAlert.vue';
import TextField from '../../components/ui/TextField.vue';
import PasswordField from '../../components/ui/PasswordField.vue';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

const form = reactive<UserLogin>({
  username: '',
  password: '',
});

const handleSubmit = async () => {
  authStore.clearError();
  
  const result = await authStore.signIn(form);
  
  if (result.success) {
    // Small delay to ensure session cookie is set
    await new Promise(resolve => setTimeout(resolve, 200));
    
    // Wait for authentication state to be fully set
    await authStore.checkAuth();
    
    // Redirect to redirect param or profile page
    const redirect = route.query.redirect as string || '/profile';
    await router.replace(redirect);
  }
};
</script>
