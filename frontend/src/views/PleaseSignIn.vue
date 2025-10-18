<template>
  <Layout>
    <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-md w-full space-y-8">
        <div class="text-center">
          <!-- Lock Icon -->
          <div class="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-primary-100 dark:bg-primary-900/30 mb-6">
            <font-awesome-icon :icon="['fas', 'lock']" class="h-8 w-8 text-primary-600 dark:text-primary-400" />
          </div>
          
          <!-- Heading -->
          <h2 class="text-3xl font-extrabold text-gray-900 dark:text-white mb-4">
            Access Your Book Generator Profile
          </h2>
          
          <!-- Message -->
          <p class="text-lg text-gray-600 dark:text-gray-400 mb-8">
            Please sign in to your account to access your books, create new content, and manage your profile.
          </p>
        </div>

        <!-- Action Buttons -->
        <div class="space-y-4">
          <!-- Sign In Button -->
          <router-link
            to="/auth/signin"
            class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 dark:focus:ring-offset-gray-900 transition-all duration-200 transform hover:scale-105"
          >
            <font-awesome-icon :icon="['fas', 'sign-in-alt']" class="mr-2" />
            Sign In to Your Account
          </router-link>

          <!-- Sign Up Button -->
          <router-link
            to="/auth/signup"
            class="group relative w-full flex justify-center py-3 px-4 border-2 border-primary-600 text-sm font-medium rounded-lg text-primary-600 bg-transparent hover:bg-primary-50 dark:hover:bg-primary-900/20 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 dark:focus:ring-offset-gray-900 transition-all duration-200"
          >
            <font-awesome-icon :icon="['fas', 'user-plus']" class="mr-2" />
            Create New Account
          </router-link>
        </div>

        <!-- Additional Info -->
        <div class="text-center">
          <p class="text-sm text-gray-500 dark:text-gray-400">
            New to Book Generator? 
            <router-link to="/features" class="font-medium text-primary-600 hover:text-primary-500 dark:text-primary-400 dark:hover:text-primary-300">
              Learn about our features
            </router-link>
          </p>
        </div>
      </div>
    </div>
  </Layout>
</template>

<script setup lang="ts">
import Layout from '../components/Layout.vue';
</script>