<template>
  <div class="min-h-screen flex flex-col">
    <!-- Header/Navbar -->
    <header class="bg-white dark:bg-gray-900 shadow-sm sticky top-0 z-50 transition-colors duration-200">
      <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center">
            <router-link to="/" class="flex items-center space-x-2">
              <font-awesome-icon :icon="['fas', 'book']" class="h-8 w-8 text-primary-600 dark:text-primary-400" />
              <span class="text-2xl font-bold text-gray-900 dark:text-white">BookGen AI</span>
            </router-link>
          </div>

          <!-- Desktop Navigation -->
          <div class="hidden md:flex items-center space-x-8">
            <router-link to="/" class="text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 font-medium transition-colors">
              Home
            </router-link>
            <router-link to="/features" class="text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 font-medium transition-colors">
              Features
            </router-link>
            <router-link to="/about" class="text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 font-medium transition-colors">
              About
            </router-link>
            <router-link to="/pricing" class="text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 font-medium transition-colors">
              Pricing
            </router-link>
            
            <!-- Dark Mode Toggle -->
            <button
              @click="themeStore.toggleTheme()"
              class="p-2 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
              :title="themeStore.isDark() ? 'Switch to light mode' : 'Switch to dark mode'"
            >
              <font-awesome-icon :icon="['fas', themeStore.isDark() ? 'sun' : 'moon']" class="h-5 w-5" />
            </button>
            
            <template v-if="authStore.isAuthenticated">
              <router-link 
                to="/profile/books" 
                class="text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 font-medium flex items-center transition-colors"
              >
                <font-awesome-icon :icon="['fas', 'book']" class="mr-1" />
                My Books
              </router-link>
              <router-link 
                to="/profile"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 transition-colors"
              >
                <font-awesome-icon :icon="['fas', 'user']" class="mr-2" />
                Profile
              </router-link>
            </template>
            <template v-else>
              <router-link 
                to="/auth/signin"
                class="text-gray-700 hover:text-primary-600 font-medium"
              >
                Sign In
              </router-link>
              <router-link 
                to="/auth/signup"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
              >
                Get Started
              </router-link>
            </template>
          </div>

          <!-- Mobile menu button -->
          <div class="md:hidden">
            <button
              @click="mobileMenuOpen = !mobileMenuOpen"
              class="inline-flex items-center justify-center p-2 rounded-md text-gray-700 hover:text-primary-600 focus:outline-none"
            >
              <font-awesome-icon :icon="['fas', mobileMenuOpen ? 'times' : 'bars']" class="h-6 w-6" />
            </button>
          </div>
        </div>

        <!-- Mobile Navigation -->
        <div v-if="mobileMenuOpen" class="md:hidden py-4 space-y-2">
          <router-link to="/" @click="mobileMenuOpen = false" class="block px-3 py-2 text-gray-700 hover:bg-gray-50 rounded-md">
            Home
          </router-link>
          <router-link to="/features" @click="mobileMenuOpen = false" class="block px-3 py-2 text-gray-700 hover:bg-gray-50 rounded-md">
            Features
          </router-link>
          <router-link to="/about" @click="mobileMenuOpen = false" class="block px-3 py-2 text-gray-700 hover:bg-gray-50 rounded-md">
            About
          </router-link>
          <router-link to="/pricing" @click="mobileMenuOpen = false" class="block px-3 py-2 text-gray-700 hover:bg-gray-50 rounded-md">
            Pricing
          </router-link>
          
          <template v-if="authStore.isAuthenticated">
            <router-link to="/profile/mybooks" @click="mobileMenuOpen = false" class="block px-3 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 rounded-md transition-colors">
              My Books
            </router-link>
            <router-link to="/profile" @click="mobileMenuOpen = false" class="block px-3 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 rounded-md transition-colors">
              Profile
            </router-link>
          </template>
          <template v-else>
            <router-link to="/auth/signin" @click="mobileMenuOpen = false" class="block px-3 py-2 text-gray-700 hover:bg-gray-50 rounded-md">
              Sign In
            </router-link>
            <router-link to="/auth/signup" @click="mobileMenuOpen = false" class="block px-3 py-2 text-primary-600 font-medium hover:bg-gray-50 rounded-md">
              Get Started
            </router-link>
          </template>
        </div>
      </nav>
    </header>

    <!-- Main Content -->
    <main class="flex-grow">
      <slot />
    </main>

    <!-- Footer -->
    <footer class="bg-gray-900 text-white mt-auto">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
          <!-- Brand -->
          <div class="col-span-1">
            <div class="flex items-center space-x-2 mb-4">
              <font-awesome-icon :icon="['fas', 'book']" class="h-8 w-8 text-primary-400" />
              <span class="text-xl font-bold">BookGen AI</span>
            </div>
            <p class="text-gray-400 text-sm">
              AI-powered book generation platform. Create professional books in minutes with cutting-edge technology.
            </p>
          </div>

          <!-- Quick Links -->
          <div>
            <h3 class="font-semibold mb-4">Quick Links</h3>
            <ul class="space-y-2 text-sm">
              <li>
                <router-link to="/" class="text-gray-400 hover:text-white">Home</router-link>
              </li>
              <li>
                <router-link to="/features" class="text-gray-400 hover:text-white">Features</router-link>
              </li>
              <li>
                <router-link to="/about" class="text-gray-400 hover:text-white">About Us</router-link>
              </li>
              <li>
                <router-link to="/pricing" class="text-gray-400 hover:text-white">Pricing</router-link>
              </li>
            </ul>
          </div>

          <!-- Resources -->
          <div>
            <h3 class="font-semibold mb-4">Resources</h3>
            <ul class="space-y-2 text-sm">
              <li>
                <a href="/api/docs/" target="_blank" class="text-gray-400 hover:text-white">API Documentation</a>
              </li>
              <li>
                <router-link to="/books" class="text-gray-400 hover:text-white">My Books</router-link>
              </li>
              <li>
                <a href="#" class="text-gray-400 hover:text-white">Help Center</a>
              </li>
              <li>
                <a href="#" class="text-gray-400 hover:text-white">Contact Support</a>
              </li>
            </ul>
          </div>

          <!-- Legal -->
          <div>
            <h3 class="font-semibold mb-4">Legal</h3>
            <ul class="space-y-2 text-sm">
              <li>
                <a href="#" class="text-gray-400 hover:text-white">Privacy Policy</a>
              </li>
              <li>
                <a href="#" class="text-gray-400 hover:text-white">Terms of Service</a>
              </li>
              <li>
                <a href="#" class="text-gray-400 hover:text-white">Cookie Policy</a>
              </li>
              <li>
                <a href="#" class="text-gray-400 hover:text-white">GDPR</a>
              </li>
            </ul>
          </div>
        </div>

        <div class="border-t border-gray-800 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center">
          <p class="text-gray-400 text-sm">
            © {{ currentYear }} BookGen AI. All rights reserved.
          </p>
          <div class="flex space-x-6 mt-4 md:mt-0">
            <a href="#" class="text-gray-400 hover:text-white">
              <font-awesome-icon :icon="['fas', 'envelope']" class="h-5 w-5" />
            </a>
            <a href="https://github.com/BadrRibzat/book-generator" target="_blank" class="text-gray-400 hover:text-white">
              <font-awesome-icon :icon="['fas', 'code']" class="h-5 w-5" />
            </a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useThemeStore } from '../stores/theme';

const authStore = useAuthStore();
const themeStore = useThemeStore();
const mobileMenuOpen = ref(false);
const currentYear = computed(() => new Date().getFullYear());
</script>
