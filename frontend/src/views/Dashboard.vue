<template>
  <Layout>
    <div class="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-100 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900">
      <!-- Dashboard Header with Glassmorphism -->
      <div class="relative overflow-hidden">
        <!-- Animated Background -->
        <div class="absolute inset-0 bg-gradient-to-r from-primary-600 via-primary-700 to-primary-800">
          <div class="absolute inset-0 opacity-20">
            <div class="absolute top-20 right-20 w-64 h-64 bg-white/10 rounded-full blur-3xl animate-float"></div>
            <div class="absolute bottom-20 left-20 w-48 h-48 bg-white/5 rounded-full blur-3xl animate-float" style="animation-delay: 3s"></div>
          </div>
        </div>

        <!-- Glass Header Card -->
        <div class="relative z-10 glass-card m-6 p-8">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-6">
              <div class="w-16 h-16 bg-gradient-to-br from-primary-500 to-primary-600 rounded-2xl flex items-center justify-center shadow-neon">
                <font-awesome-icon :icon="['fas', 'brain']" class="text-white text-2xl" />
              </div>
              <div>
                <h1 class="text-3xl font-bold text-white display-font">Welcome back, {{ user?.username }}!</h1>
                <p class="text-primary-100 text-lg">Manage your AI-powered book generation dashboard</p>
              </div>
            </div>
            <div class="text-right">
              <div class="text-3xl font-bold text-white mb-1">{{ userProfile?.subscription_tier || 'FREE' }}</div>
              <div class="text-sm text-primary-200">Current Plan</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content -->
      <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <!-- Tab Navigation -->
        <div class="mb-8">
          <div class="border-b border-gray-200 dark:border-gray-700">
            <nav class="-mb-px flex space-x-8" aria-label="Tabs">
              <button
                @click="activeTab = 'overview'"
                :class="[
                  activeTab === 'overview'
                    ? 'border-primary-500 text-primary-600 dark:text-primary-400'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300',
                  'whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm'
                ]"
              >
                <font-awesome-icon :icon="['fas', 'tachometer-alt']" class="mr-2" />
                Overview
              </button>
              <button
                @click="activeTab = 'books'"
                :class="[
                  activeTab === 'books'
                    ? 'border-primary-500 text-primary-600 dark:text-primary-400'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300',
                  'whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm'
                ]"
              >
                <font-awesome-icon :icon="['fas', 'book']" class="mr-2" />
                My Books
              </button>
              <button
                @click="activeTab = 'subscription'"
                :class="[
                  activeTab === 'subscription'
                    ? 'border-primary-500 text-primary-600 dark:text-primary-400'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300',
                  'whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm'
                ]"
              >
                <font-awesome-icon :icon="['fas', 'credit-card']" class="mr-2" />
                Subscription
              </button>
              <button
                @click="activeTab = 'profile'"
                :class="[
                  activeTab === 'profile'
                    ? 'border-primary-500 text-primary-600 dark:text-primary-400'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300',
                  'whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm'
                ]"
              >
                <font-awesome-icon :icon="['fas', 'user-cog']" class="mr-2" />
                Profile Settings
              </button>
            </nav>
          </div>
        </div>

        <!-- Tab Content -->
        <div v-show="activeTab === 'overview'">
          <!-- Stats Cards with Glassmorphism -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <!-- Books Generated -->
          <div class="card-modern interactive-card">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Books Generated</p>
                <p class="text-3xl font-bold text-gray-900 dark:text-white">{{ stats.totalBooks }}</p>
                <div class="flex items-center mt-2">
                  <div class="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></div>
                  <span class="text-xs text-green-600 dark:text-green-400">Active</span>
                </div>
              </div>
              <div class="w-14 h-14 bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl flex items-center justify-center shadow-lg">
                <font-awesome-icon :icon="['fas', 'book']" class="h-7 w-7 text-white" />
              </div>
            </div>
          </div>

          <!-- Daily Usage -->
          <div class="card-modern interactive-card">
            <div class="flex items-center justify-between">
              <div class="flex-1">
                <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Today's Usage</p>
                <p class="text-3xl font-bold text-gray-900 dark:text-white">{{ stats.dailyBooks }}</p>
                <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">{{ stats.dailyLimit }} books limit</p>

                <!-- Progress Bar -->
                <div class="mt-3">
                  <div class="progress-bar">
                    <div
                      class="progress-fill"
                      :style="{ width: `${Math.min((stats.dailyBooks / stats.dailyLimit) * 100, 100)}%` }"
                    ></div>
                  </div>
                  <div class="flex justify-between text-xs text-gray-500 dark:text-gray-400 mt-1">
                    <span>{{ Math.round((stats.dailyBooks / stats.dailyLimit) * 100) }}% used</span>
                    <span>{{ Math.max(0, stats.dailyLimit - stats.dailyBooks) }} remaining</span>
                  </div>
                </div>
              </div>
              <div class="w-14 h-14 bg-gradient-to-br from-green-500 to-green-600 rounded-2xl flex items-center justify-center shadow-lg ml-4">
                <font-awesome-icon :icon="['fas', 'calendar-day']" class="h-7 w-7 text-white" />
              </div>
            </div>
          </div>

          <!-- AI Usage Stats -->
          <div class="card-modern interactive-card">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-600 dark:text-gray-400">AI Processing</p>
                <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ aiStats.totalTokens.toLocaleString() }}</p>
                <p class="text-xs text-gray-500 dark:text-gray-400">tokens used this month</p>
                <div class="flex items-center mt-2">
                  <div class="w-2 h-2 bg-blue-500 rounded-full mr-2 animate-pulse"></div>
                  <span class="text-xs text-blue-600 dark:text-blue-400">DeepSeek R1T2</span>
                </div>
              </div>
              <div class="w-14 h-14 bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg">
                <font-awesome-icon :icon="['fas', 'robot']" class="h-7 w-7 text-white" />
              </div>
            </div>
          </div>

          <!-- Account Status -->
          <div class="card-modern interactive-card">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Account Status</p>
                <p class="text-xl font-bold" :class="getStatusColorClass(userProfile?.subscription_status)">
                  {{ userProfile?.subscription_status || 'INACTIVE' }}
                </p>
                <p class="text-xs text-gray-500 dark:text-gray-400">{{ getStatusDescription(userProfile?.subscription_status) }}</p>
                <div class="mt-2">
                  <span :class="getTierBadgeClass(userProfile?.subscription_tier)">
                    {{ userProfile?.subscription_tier || 'FREE' }}
                  </span>
                </div>
              </div>
              <div class="w-14 h-14 rounded-2xl flex items-center justify-center shadow-lg" :class="getStatusBgClass(userProfile?.subscription_status)">
                <font-awesome-icon :icon="['fas', 'star']" class="h-7 w-7 text-white" />
              </div>
            </div>
          </div>
        </div>

        <!-- Real-time Activity Feed -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
          <!-- Activity Feed -->
          <div class="lg:col-span-2 card-modern">
            <div class="p-6 border-b border-gray-200/20 dark:border-gray-700/50">
              <div class="flex items-center justify-between">
                <h2 class="text-xl font-semibold text-gray-900 dark:text-white display-font">Recent Activity</h2>
                <div class="flex items-center space-x-2">
                  <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                  <span class="text-sm text-green-600 dark:text-green-400">Live</span>
                </div>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400">Real-time updates on your book generation</p>
            </div>
            <div class="p-6">
              <div v-if="recentActivity.length === 0" class="text-center py-8">
                <div class="w-16 h-16 bg-gradient-to-br from-gray-400 to-gray-500 rounded-2xl flex items-center justify-center mx-auto mb-4">
                  <font-awesome-icon :icon="['fas', 'clock']" class="text-white text-2xl" />
                </div>
                <p class="text-gray-600 dark:text-gray-400 mb-4">No recent activity</p>
                <p class="text-sm text-gray-500 dark:text-gray-500">Activity will appear here as you create books</p>
              </div>
              <div v-else class="space-y-4">
                <div
                  v-for="activity in recentActivity"
                  :key="activity.id"
                  class="flex items-start space-x-4 p-4 rounded-xl bg-gradient-to-r from-white/50 to-transparent dark:from-gray-800/50 dark:to-transparent border border-white/20 dark:border-gray-700/50 hover:shadow-lg transition-all duration-300"
                >
                  <div class="flex-shrink-0">
                    <div class="w-10 h-10 rounded-xl flex items-center justify-center" :class="getActivityIconClass(activity.type)">
                      <font-awesome-icon :icon="getActivityIcon(activity.type)" class="w-5 h-5 text-white" />
                    </div>
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium text-gray-900 dark:text-white">{{ activity.title }}</p>
                    <p class="text-xs text-gray-600 dark:text-gray-400 mt-1">{{ activity.description }}</p>
                    <p class="text-xs text-gray-500 dark:text-gray-500 mt-1">{{ formatTimeAgo(activity.timestamp) }}</p>
                  </div>
                  <div class="flex-shrink-0">
                    <span :class="getActivityStatusClass(activity.status)">
                      {{ activity.status }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick Actions & Subscription -->
          <div class="space-y-6">
            <!-- Quick Actions -->
            <div class="card-modern p-6">
              <div class="flex items-center space-x-3 mb-6">
                <div class="w-12 h-12 bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl flex items-center justify-center">
                  <font-awesome-icon :icon="['fas', 'zap']" class="text-white text-xl" />
                </div>
                <h2 class="text-xl font-bold text-gray-900 dark:text-white display-font">Quick Actions</h2>
              </div>

              <div class="space-y-3">
                <router-link
                  to="/profile/create"
                  class="w-full glass-button btn-primary inline-flex items-center justify-center group"
                >
                  <font-awesome-icon :icon="['fas', 'plus']" class="mr-2 group-hover:animate-bounce" />
                  Create New Book
                </router-link>

                <router-link
                  to="/profile/books"
                  class="w-full glass-button inline-flex items-center justify-center"
                >
                  <font-awesome-icon :icon="['fas', 'book']" class="mr-2" />
                  View All Books
                </router-link>

                <button
                  @click="refreshStats"
                  class="w-full glass-button inline-flex items-center justify-center"
                  :disabled="refreshing"
                >
                  <font-awesome-icon
                    :icon="['fas', 'sync']"
                    class="mr-2"
                    :class="{ 'animate-spin': refreshing }"
                  />
                  {{ refreshing ? 'Refreshing...' : 'Refresh Stats' }}
                </button>
              </div>
            </div>

            <!-- Subscription Info -->
            <div class="card-modern p-6">
              <div class="p-6 border-b border-gray-200/20 dark:border-gray-700/50">
                <h2 class="text-lg font-semibold text-gray-900 dark:text-white display-font">Subscription Details</h2>
              </div>
              <div class="p-6">
                <div class="flex items-center justify-between mb-4">
                  <div>
                    <div class="text-2xl font-bold" :class="getTierColorClass(userProfile?.subscription_tier)">
                      {{ userProfile?.subscription_tier || 'FREE' }}
                    </div>
                    <div class="text-sm text-gray-500 dark:text-gray-400">
                      {{ getTierDescription(userProfile?.subscription_tier) }}
                    </div>
                  </div>
                  <div class="text-right">
                    <div class="text-sm text-gray-500 dark:text-gray-400">Books remaining</div>
                    <div class="text-lg font-bold text-gray-900 dark:text-white">
                      {{ Math.max(0, stats.dailyLimit - stats.dailyBooks) }}
                    </div>
                  </div>
                </div>

                <div v-if="userProfile?.subscription_tier === 'free'" class="mt-4">
                  <router-link
                    to="/pricing"
                    class="w-full bg-gradient-to-r from-amber-500 to-orange-500 text-white px-4 py-3 rounded-xl font-medium hover:from-amber-600 hover:to-orange-600 transition-all duration-200 text-center block shadow-lg hover:shadow-xl transform hover:scale-105"
                  >
                    <font-awesome-icon :icon="['fas', 'crown']" class="mr-2" />
                    Upgrade Plan
                  </router-link>
                </div>

                <!-- Usage Breakdown -->
                <div class="mt-4 pt-4 border-t border-gray-200/20 dark:border-gray-700/50">
                  <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-3">Monthly Usage</h4>
                  <div class="space-y-2">
                    <div class="flex justify-between text-sm">
                      <span class="text-gray-600 dark:text-gray-400">Books Created</span>
                      <span class="text-gray-900 dark:text-white font-medium">{{ stats.monthlyBooks }}</span>
                    </div>
                    <div class="flex justify-between text-sm">
                      <span class="text-gray-600 dark:text-gray-400">AI Tokens</span>
                      <span class="text-gray-900 dark:text-white font-medium">{{ aiStats.totalTokens.toLocaleString() }}</span>
                    </div>
                    <div class="flex justify-between text-sm">
                      <span class="text-gray-600 dark:text-gray-400">Est. Cost</span>
                      <span class="text-green-600 dark:text-green-400 font-medium">${{ aiStats.estimatedCost.toFixed(2) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Books Section -->
        <div class="card-modern">
          <div class="p-6 border-b border-gray-200/20 dark:border-gray-700/50">
            <h2 class="text-xl font-semibold text-gray-900 dark:text-white display-font">Recent Books</h2>
            <p class="text-sm text-gray-600 dark:text-gray-400">Your latest generated books</p>
          </div>
          <div class="p-6">
            <div v-if="recentBooks.length === 0" class="text-center py-12">
              <div class="w-20 h-20 bg-gradient-to-br from-gray-400 to-gray-500 rounded-2xl flex items-center justify-center mx-auto mb-6">
                <font-awesome-icon :icon="['fas', 'book-open']" class="text-white text-3xl" />
              </div>
              <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">No books yet</h3>
              <p class="text-gray-600 dark:text-gray-400 mb-6">Create your first AI-powered book to get started</p>
              <router-link
                to="/profile/create"
                class="btn-primary inline-flex items-center justify-center group"
              >
                <font-awesome-icon :icon="['fas', 'plus']" class="mr-2" />
                Create Your First Book
              </router-link>
            </div>
            <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div
                v-for="book in recentBooks"
                :key="book.id"
                class="interactive-card glass p-6 rounded-xl border border-white/20 dark:border-gray-700/50 hover:shadow-glass-lg transition-all duration-300"
              >
                <div class="flex items-start justify-between mb-4">
                  <div class="w-12 h-12 bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl flex items-center justify-center shadow-lg">
                    <font-awesome-icon :icon="['fas', 'book']" class="w-6 h-6 text-white" />
                  </div>
                  <span :class="getStatusBadgeClass(book.status)">
                    {{ book.status }}
                  </span>
                </div>

                <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2 line-clamp-2">
                  {{ book.title || 'Untitled Book' }}
                </h3>

                <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
                  {{ formatDate(book.created_at) }}
                </p>

                <div class="flex items-center justify-between">
                  <div class="flex space-x-2">
                    <router-link
                      :to="`/profile/books/${book.id}`"
                      class="text-sm text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 font-medium"
                    >
                      View Details
                    </router-link>
                    <button
                      @click="confirmDeleteBook(book)"
                      class="text-sm text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300 font-medium"
                      title="Delete book"
                    >
                      Delete
                    </button>
                  </div>

                  <div v-if="book.status === 'ready'" class="flex space-x-1">
                    <button
                      @click="downloadBook(book)"
                      class="p-2 text-green-600 dark:text-green-400 hover:bg-green-50 dark:hover:bg-green-900/20 rounded-lg transition-colors"
                      title="Download PDF"
                    >
                      <font-awesome-icon :icon="['fas', 'download']" class="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- My Books Tab -->
        <div v-show="activeTab === 'books'">
          <div class="card-modern">
            <div class="p-6 border-b border-gray-200/20 dark:border-gray-700/50">
              <h2 class="text-xl font-semibold text-gray-900 dark:text-white display-font">My Books</h2>
              <p class="text-sm text-gray-600 dark:text-gray-400">Manage your generated books</p>
            </div>
            <div class="p-6">
              <div v-if="allBooks.length === 0" class="text-center py-12">
                <div class="w-20 h-20 bg-gradient-to-br from-gray-400 to-gray-500 rounded-2xl flex items-center justify-center mx-auto mb-6">
                  <font-awesome-icon :icon="['fas', 'book-open']" class="text-white text-3xl" />
                </div>
                <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">No books yet</h3>
                <p class="text-gray-600 dark:text-gray-400 mb-6">Create your first AI-powered book to get started</p>
                <router-link
                  to="/profile/create"
                  class="btn-primary inline-flex items-center justify-center group"
                >
                  <font-awesome-icon :icon="['fas', 'plus']" class="mr-2" />
                  Create Your First Book
                </router-link>
              </div>
              <div v-else class="space-y-4">
                <div
                  v-for="book in allBooks"
                  :key="book.id"
                  class="flex items-center justify-between p-6 rounded-xl bg-gradient-to-r from-white/50 to-transparent dark:from-gray-800/50 dark:to-transparent border border-white/20 dark:border-gray-700/50 hover:shadow-lg transition-all duration-300"
                >
                  <div class="flex items-center space-x-4">
                    <div class="w-12 h-12 bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl flex items-center justify-center shadow-lg">
                      <font-awesome-icon :icon="['fas', 'book']" class="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                        {{ book.title || 'Untitled Book' }}
                      </h3>
                      <p class="text-sm text-gray-600 dark:text-gray-400">
                        {{ formatDate(book.created_at) }} • {{ book.status }}
                      </p>
                    </div>
                  </div>
                  <div class="flex items-center space-x-2">
                    <router-link
                      :to="`/profile/books/${book.id}`"
                      class="px-4 py-2 text-sm font-medium text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 border border-primary-200 dark:border-primary-700 rounded-lg hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-colors"
                    >
                      View
                    </router-link>
                    <button
                      v-if="book.status === 'ready'"
                      @click="downloadBook(book)"
                      class="px-4 py-2 text-sm font-medium text-green-600 dark:text-green-400 hover:text-green-700 dark:hover:text-green-300 border border-green-200 dark:border-green-700 rounded-lg hover:bg-green-50 dark:hover:bg-green-900/20 transition-colors"
                    >
                      Download
                    </button>
                    <button
                      @click="duplicateBook(book)"
                      class="px-4 py-2 text-sm font-medium text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 border border-blue-200 dark:border-blue-700 rounded-lg hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors"
                    >
                      Duplicate
                    </button>
                    <button
                      @click="confirmDeleteBook(book)"
                      class="px-4 py-2 text-sm font-medium text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300 border border-red-200 dark:border-red-700 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Subscription Tab -->
        <div v-show="activeTab === 'subscription'">
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <!-- Current Plan -->
            <div class="card-modern p-6">
              <div class="flex items-center space-x-3 mb-6">
                <div class="w-12 h-12 bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl flex items-center justify-center">
                  <font-awesome-icon :icon="['fas', 'crown']" class="text-white text-xl" />
                </div>
                <h2 class="text-xl font-bold text-gray-900 dark:text-white display-font">Current Plan</h2>
              </div>
              <div class="text-center">
                <div class="text-4xl font-bold mb-2" :class="getTierColorClass(userProfile?.subscription_tier)">
                  {{ userProfile?.subscription_tier || 'FREE' }}
                </div>
                <div class="text-gray-600 dark:text-gray-400 mb-6">
                  {{ getTierDescription(userProfile?.subscription_tier) }}
                </div>
                <div class="bg-gradient-to-r from-primary-50 to-blue-50 dark:from-primary-900/20 dark:to-blue-900/20 rounded-lg p-4 mb-6">
                  <div class="text-sm text-gray-600 dark:text-gray-400">Books per day</div>
                  <div class="text-2xl font-bold text-gray-900 dark:text-white">{{ userProfile?.books_per_day || 1 }}</div>
                </div>
                <router-link
                  v-if="userProfile?.subscription_tier === 'free'"
                  to="/pricing"
                  class="w-full bg-gradient-to-r from-amber-500 to-orange-500 text-white px-6 py-3 rounded-xl font-medium hover:from-amber-600 hover:to-orange-600 transition-all duration-200 text-center block shadow-lg hover:shadow-xl transform hover:scale-105"
                >
                  <font-awesome-icon :icon="['fas', 'arrow-up']" class="mr-2" />
                  Upgrade Plan
                </router-link>
              </div>
            </div>

            <!-- Usage Stats -->
            <div class="card-modern p-6">
              <div class="flex items-center space-x-3 mb-6">
                <div class="w-12 h-12 bg-gradient-to-br from-green-500 to-green-600 rounded-xl flex items-center justify-center">
                  <font-awesome-icon :icon="['fas', 'chart-bar']" class="text-white text-xl" />
                </div>
                <h2 class="text-xl font-bold text-gray-900 dark:text-white display-font">Usage Statistics</h2>
              </div>
              <div class="space-y-4">
                <div class="flex justify-between items-center">
                  <span class="text-gray-600 dark:text-gray-400">Books this month</span>
                  <span class="font-semibold text-gray-900 dark:text-white">{{ stats.monthlyBooks }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-gray-600 dark:text-gray-400">Books today</span>
                  <span class="font-semibold text-gray-900 dark:text-white">{{ stats.dailyBooks }} / {{ stats.dailyLimit }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-gray-600 dark:text-gray-400">AI Tokens used</span>
                  <span class="font-semibold text-gray-900 dark:text-white">{{ aiStats.totalTokens.toLocaleString() }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-gray-600 dark:text-gray-400">Est. Cost</span>
                  <span class="font-semibold text-green-600 dark:text-green-400">${{ aiStats.estimatedCost.toFixed(2) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Profile Settings Tab -->
        <div v-show="activeTab === 'profile'">
          <div class="card-modern p-6">
            <div class="flex items-center space-x-3 mb-6">
              <div class="w-12 h-12 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl flex items-center justify-center">
                <font-awesome-icon :icon="['fas', 'user-cog']" class="text-white text-xl" />
              </div>
              <h2 class="text-xl font-bold text-gray-900 dark:text-white display-font">Profile Settings</h2>
            </div>
            <div class="max-w-md">
              <form @submit.prevent="updateProfile" class="space-y-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Username</label>
                  <input
                    v-model="profileForm.username"
                    type="text"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
                    required
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Email</label>
                  <input
                    v-model="profileForm.email"
                    type="email"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
                    required
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">First Name</label>
                  <input
                    v-model="profileForm.first_name"
                    type="text"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Last Name</label>
                  <input
                    v-model="profileForm.last_name"
                    type="text"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
                  />
                </div>
                <button
                  type="submit"
                  :disabled="updatingProfile"
                  class="w-full bg-gradient-to-r from-primary-600 to-blue-600 text-white px-6 py-3 rounded-xl font-medium hover:from-primary-700 hover:to-blue-700 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <span v-if="updatingProfile" class="flex items-center justify-center">
                    <font-awesome-icon :icon="['fas', 'spinner']" class="animate-spin mr-2" />
                    Updating...
                  </span>
                  <span v-else>Update Profile</span>
                </button>
              </form>
            </div>
          </div>
        </div>
      </main>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="glass-card max-w-md w-full p-6">
        <div class="flex items-center space-x-3 mb-4">
          <div class="w-10 h-10 bg-red-500 rounded-xl flex items-center justify-center">
            <font-awesome-icon :icon="['fas', 'exclamation-triangle']" class="w-5 h-5 text-white" />
          </div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Delete Book</h3>
        </div>

        <p class="text-gray-600 dark:text-gray-300 mb-6">
          Are you sure you want to delete <strong>"{{ bookToDelete?.title || 'Untitled Book' }}"</strong>?
          This action cannot be undone.
        </p>

        <div class="flex space-x-3">
          <button
            @click="cancelDelete"
            class="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
            :disabled="isDeleting"
          >
            Cancel
          </button>
          <button
            @click="deleteBook"
            class="flex-1 px-4 py-2 bg-red-600 text-white rounded-xl hover:bg-red-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="isDeleting"
          >
            <span v-if="isDeleting" class="flex items-center justify-center">
              <font-awesome-icon :icon="['fas', 'spinner']" class="animate-spin mr-2" />
              Deleting...
            </span>
            <span v-else>Delete Book</span>
          </button>
        </div>
      </div>
    </div>
  </Layout>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, onUnmounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useBooksStore } from '../stores/books'
import Layout from '../components/Layout.vue'
import apiClient from '../services/api'

interface Book {
  id: number
  title: string
  status: string
  created_at: string
  domain?: string
  sub_niche?: string
}

interface UserProfile {
  subscription_tier?: string
  subscription_status?: string
  books_used_today?: number
  books_per_day?: number
  total_books?: number
}

interface Activity {
  id: string
  type: 'book_created' | 'book_completed' | 'cover_generated' | 'error'
  title: string
  description: string
  status: 'success' | 'pending' | 'error'
  timestamp: Date
}

interface AIStats {
  totalTokens: number
  estimatedCost: number
  monthlyBooks: number
}

const authStore = useAuthStore()
const booksStore = useBooksStore()

// State
const stats = ref({
  totalBooks: 0,
  dailyBooks: 0,
  dailyLimit: 1,
  monthlyBooks: 0,
  revenueGenerated: 0
})

const aiStats = ref<AIStats>({
  totalTokens: 0,
  estimatedCost: 0,
  monthlyBooks: 0
})

const recentBooks = ref<Book[]>([])
const allBooks = ref<Book[]>([])
const recentActivity = ref<Activity[]>([])
const userProfile = ref<UserProfile>({})
const activeTab = ref('overview')
const refreshing = ref(false)
const activityInterval = ref<number | null>(null)

// Profile form
const profileForm = ref({
  username: '',
  email: '',
  first_name: '',
  last_name: ''
})
const updatingProfile = ref(false)

// Computed
const user = computed(() => authStore.user)

// Methods
const getTierColorClass = (tier?: string) => {
  switch (tier?.toLowerCase()) {
    case 'free': return 'text-gray-600 dark:text-gray-400'
    case 'basic': return 'text-blue-600 dark:text-blue-400'
    case 'premium': return 'text-purple-600 dark:text-purple-400'
    case 'enterprise': return 'text-amber-600 dark:text-amber-400'
    default: return 'text-gray-600 dark:text-gray-400'
  }
}

const getStatusColorClass = (status?: string) => {
  switch (status?.toLowerCase()) {
    case 'active': return 'text-green-600 dark:text-green-400'
    case 'trial': return 'text-blue-600 dark:text-blue-400'
    case 'inactive': return 'text-gray-600 dark:text-gray-400'
    case 'cancelled': return 'text-red-600 dark:text-red-400'
    default: return 'text-gray-600 dark:text-gray-400'
  }
}

const getStatusBgClass = (status?: string) => {
  switch (status?.toLowerCase()) {
    case 'active': return 'bg-green-500'
    case 'trial': return 'bg-blue-500'
    case 'inactive': return 'bg-gray-500'
    case 'cancelled': return 'bg-red-500'
    default: return 'bg-gray-500'
  }
}

const getTierBadgeClass = (tier?: string) => {
  switch (tier?.toLowerCase()) {
    case 'free': return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
    case 'basic': return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
    case 'premium': return 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200'
    case 'enterprise': return 'bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-200'
    default: return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
  }
}

const getTierDescription = (tier?: string) => {
  switch (tier?.toLowerCase()) {
    case 'free': return 'Limited access'
    case 'basic': return '1 book/day - $15'
    case 'premium': return '3 books/day - $45'
    case 'enterprise': return '5 books/day - $60'
    default: return 'No active plan'
  }
}

const getStatusDescription = (status?: string) => {
  switch (status?.toLowerCase()) {
    case 'active': return 'All features enabled'
    case 'trial': return 'Trial period active'
    case 'inactive': return 'Subscription required'
    case 'cancelled': return 'Subscription cancelled'
    default: return 'Account status unknown'
  }
}

const getStatusBadgeClass = (status: string) => {
  switch (status?.toLowerCase()) {
    case 'ready': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
    case 'content_generated': return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
    case 'generating': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
    case 'error': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
    default: return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
  }
}

const getActivityIcon = (type: string) => {
  switch (type) {
    case 'book_created': return ['fas', 'plus']
    case 'book_completed': return ['fas', 'check']
    case 'cover_generated': return ['fas', 'image']
    case 'error': return ['fas', 'exclamation-triangle']
    default: return ['fas', 'info']
  }
}

const getActivityIconClass = (type: string) => {
  switch (type) {
    case 'book_created': return 'bg-blue-500'
    case 'book_completed': return 'bg-green-500'
    case 'cover_generated': return 'bg-purple-500'
    case 'error': return 'bg-red-500'
    default: return 'bg-gray-500'
  }
}

const getActivityStatusClass = (status: string) => {
  switch (status) {
    case 'success': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
    case 'pending': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
    case 'error': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
    default: return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

const formatTimeAgo = (timestamp: Date) => {
  const now = new Date()
  const diff = now.getTime() - timestamp.getTime()
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (days > 0) return `${days} day${days > 1 ? 's' : ''} ago`
  if (hours > 0) return `${hours} hour${hours > 1 ? 's' : ''} ago`
  if (minutes > 0) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`
  return 'Just now'
}

// Real-time activity simulation
const addActivity = (activity: Omit<Activity, 'id' | 'timestamp'>) => {
  const newActivity: Activity = {
    ...activity,
    id: Date.now().toString(),
    timestamp: new Date()
  }
  recentActivity.value.unshift(newActivity)
  // Keep only last 10 activities
  if (recentActivity.value.length > 10) {
    recentActivity.value = recentActivity.value.slice(0, 10)
  }
}

// Simulate real-time updates
const simulateActivity = () => {
  // This would normally come from WebSocket or polling
  // For demo purposes, we'll add some sample activities
  const activities = [
    {
      type: 'book_created' as const,
      title: 'New book creation started',
      description: 'AI is generating content for your new book',
      status: 'pending' as const
    },
    {
      type: 'cover_generated' as const,
      title: 'Cover design completed',
      description: 'AI-generated cover with glassmorphism design',
      status: 'success' as const
    },
    {
      type: 'book_completed' as const,
      title: 'Book generation finished',
      description: 'Your book is ready for download',
      status: 'success' as const
    }
  ]

  // Add a random activity occasionally
  if (Math.random() < 0.3) {
    const randomActivity = activities[Math.floor(Math.random() * activities.length)]
    if (randomActivity) {
      addActivity(randomActivity)
    }
  }
}

// Refresh stats
const refreshStats = async () => {
  refreshing.value = true
  try {
    await loadDashboardData()
    // Add refresh activity
    addActivity({
      type: 'book_created',
      title: 'Dashboard refreshed',
      description: 'Statistics and data updated',
      status: 'success'
    })
  } catch (error) {
    console.error('Failed to refresh stats:', error)
    addActivity({
      type: 'error',
      title: 'Refresh failed',
      description: 'Could not update dashboard data',
      status: 'error'
    })
  } finally {
    refreshing.value = false
  }
}

// Download book
const downloadBook = async (book: Book) => {
  try {
    const response = await apiClient.get(`/books/${book.id}/download/`, {
      responseType: 'blob'
    })

    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `${book.title || 'book'}.pdf`)
    document.body.appendChild(link)
    link.click()
    link.remove()

    addActivity({
      type: 'book_completed',
      title: 'Book downloaded',
      description: `Downloaded "${book.title || 'Untitled Book'}"`,
      status: 'success'
    })
  } catch (error) {
    console.error('Failed to download book:', error)
    addActivity({
      type: 'error',
      title: 'Download failed',
      description: 'Could not download the book',
      status: 'error'
    })
  }
}

// Delete functionality
const bookToDelete = ref<Book | null>(null)
const showDeleteModal = ref(false)
const isDeleting = ref(false)

const confirmDeleteBook = (book: Book) => {
  bookToDelete.value = book
  showDeleteModal.value = true
}

const deleteBook = async () => {
  if (!bookToDelete.value) return

  try {
    isDeleting.value = true
    await booksStore.deleteBook(bookToDelete.value.id)

    // Remove from recent books list
    recentBooks.value = recentBooks.value.filter(b => b.id !== bookToDelete.value!.id)

    // Update stats
    stats.value.totalBooks = Math.max(0, stats.value.totalBooks - 1)
    stats.value.monthlyBooks = Math.max(0, stats.value.monthlyBooks - 1)

    // If it was created today, update daily count
    const bookDate = new Date(bookToDelete.value.created_at)
    const today = new Date()
    if (bookDate.toDateString() === today.toDateString()) {
      stats.value.dailyBooks = Math.max(0, stats.value.dailyBooks - 1)
    }

    addActivity({
      type: 'book_created',
      title: 'Book deleted',
      description: `Deleted "${bookToDelete.value.title || 'Untitled Book'}"`,
      status: 'success'
    })

    showDeleteModal.value = false
    bookToDelete.value = null
  } catch (error) {
    console.error('Failed to delete book:', error)
    addActivity({
      type: 'error',
      title: 'Delete failed',
      description: 'Could not delete the book',
      status: 'error'
    })
  } finally {
    isDeleting.value = false
  }
}

const cancelDelete = () => {
  showDeleteModal.value = false
  bookToDelete.value = null
}

// Duplicate book
const duplicateBook = async (book: Book) => {
  try {
    // Create a new book with the same configuration
    const duplicateData = {
      domain: book.domain,
      niche: book.niche,
      book_style: book.book_style,
      cover_style: book.cover_style,
      book_length: 'medium', // Default
      target_audience: 'general', // Default
      key_topics: [], // Default
      writing_preferences: 'conversational' // Default
    }

    const response = await apiClient.post('/books/create-guided/', duplicateData)
    const newBook = response.data

    // Add to books list
    allBooks.value.unshift(newBook)
    recentBooks.value.unshift(newBook)

    // Update stats
    stats.value.totalBooks += 1
    stats.value.monthlyBooks += 1
    stats.value.dailyBooks += 1

    addActivity({
      type: 'book_created',
      title: 'Book duplicated',
      description: `Created duplicate of "${book.title || 'Untitled Book'}"`,
      status: 'success'
    })
  } catch (error) {
    console.error('Failed to duplicate book:', error)
    addActivity({
      type: 'error',
      title: 'Duplicate failed',
      description: 'Could not duplicate the book',
      status: 'error'
    })
  }
}

// Update profile
const updateProfile = async () => {
  try {
    updatingProfile.value = true
    await apiClient.patch('/users/profile/', profileForm.value)
    
    // Update user data
    authStore.user.username = profileForm.value.username
    authStore.user.email = profileForm.value.email
    
    addActivity({
      type: 'book_created',
      title: 'Profile updated',
      description: 'Your profile settings have been saved',
      status: 'success'
    })
  } catch (error) {
    console.error('Failed to update profile:', error)
    addActivity({
      type: 'error',
      title: 'Update failed',
      description: 'Could not update profile settings',
      status: 'error'
    })
  } finally {
    updatingProfile.value = false
  }
}

// Load dashboard data
const loadDashboardData = async () => {
  try {
    // Fetch dashboard data
    const [dashboardResponse] = await Promise.all([
      apiClient.get('/users/dashboard/').catch(err => {
        console.warn('Dashboard API not available yet:', err)
        return { data: null }
      })
    ])

    // If dashboard API is available, use it
    if (dashboardResponse?.data) {
      userProfile.value = dashboardResponse.data.user_profile || {}
      recentBooks.value = dashboardResponse.data.recent_books || []

      // Calculate stats from profile data
      stats.value.totalBooks = userProfile.value.total_books || 0
      stats.value.dailyBooks = userProfile.value.books_used_today || 0
      stats.value.dailyLimit = userProfile.value.books_per_day || 1
      stats.value.monthlyBooks = dashboardResponse.data.monthly_books || 0

      // AI stats (mock data for now)
      aiStats.value = {
        totalTokens: dashboardResponse.data.ai_tokens_used || Math.floor(Math.random() * 50000) + 10000,
        estimatedCost: (dashboardResponse.data.ai_tokens_used || 15000) * 0.0001,
        monthlyBooks: stats.value.monthlyBooks
      }
    } else {
      // Fallback: fetch books data separately
      await booksStore.fetchBooks()
      const books = booksStore.books || []

      // Set books data
      recentBooks.value = books.slice(0, 5)
      allBooks.value = books

      // Calculate stats from books data
      stats.value.totalBooks = books.length
      stats.value.monthlyBooks = books.length // Simplified
      stats.value.dailyBooks = books.filter((book: Book) => {
        const bookDate = new Date(book.created_at)
        const today = new Date()
        return bookDate.toDateString() === today.toDateString()
      }).length

      // Fallback data based on subscription tier
      userProfile.value = {
        subscription_tier: 'free',
        subscription_status: 'active',
        books_used_today: stats.value.dailyBooks,
        books_per_day: 1
      }
      stats.value.dailyLimit = 1

      // Mock AI stats
      aiStats.value = {
        totalTokens: Math.floor(Math.random() * 50000) + 10000,
        estimatedCost: Math.random() * 10 + 5,
        monthlyBooks: stats.value.monthlyBooks
      }
    }

  } catch (error) {
    console.error('Failed to load dashboard data:', error)
    // Use fallback data
    recentBooks.value = []
    userProfile.value = {
      subscription_tier: 'free',
      subscription_status: 'inactive',
      books_used_today: 0,
      books_per_day: 1
    }
    aiStats.value = {
      totalTokens: 0,
      estimatedCost: 0,
      monthlyBooks: 0
    }
  }
}

// Lifecycle
onMounted(async () => {
  await loadDashboardData()

  // Set profile form data
  profileForm.value = {
    username: user.value?.username || '',
    email: user.value?.email || '',
    first_name: user.value?.first_name || '',
    last_name: user.value?.last_name || ''
  }

  // Start real-time activity simulation
  activityInterval.value = setInterval(simulateActivity, 30000) // Every 30 seconds

  // Add initial welcome activity
  addActivity({
    type: 'book_created',
    title: 'Welcome to your dashboard',
    description: 'Dashboard loaded successfully',
    status: 'success'
  })
})

onUnmounted(() => {
  if (activityInterval.value) {
    clearInterval(activityInterval.value)
  }
})
</script>

<style scoped>
/* Glassmorphism Effects */
.glass-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
}

.card-modern {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.interactive-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.interactive-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

.glass-button {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}

.glass-button:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.btn-primary:hover {
  background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}

/* Progress Bar */
.progress-bar {
  width: 100%;
  height: 8px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #10b981, #34d399);
  border-radius: 4px;
  transition: width 0.5s ease;
  box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
}

/* Floating Animation */
@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

.animate-float {
  animation: float 6s ease-in-out infinite;
}

/* Neon Shadow */
.shadow-neon {
  box-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
}

/* Glass Shadow */
.shadow-glass-lg {
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1), 0 0 0 1px rgba(255, 255, 255, 0.2);
}

/* Line Clamp */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Dark mode adjustments */
.dark .glass-card {
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.dark .card-modern {
  background: rgba(0, 0, 0, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .glass-card {
    margin: 0.5rem;
    padding: 1rem;
  }

  .animate-float {
    animation-duration: 8s;
  }

  /* Mobile header adjustments */
  .glass-card.m-6 {
    margin: 1rem;
    padding: 1.5rem;
  }

  .glass-card.m-6 .flex.items-center.justify-between {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .glass-card.m-6 .flex.items-center.justify-between .flex.items-center.space-x-6 {
    width: 100%;
  }

  .glass-card.m-6 .flex.items-center.justify-between .text-right {
    width: 100%;
    text-align: left;
  }

  /* Mobile stats cards */
  .grid.grid-cols-1.md\\:grid-cols-2.lg\\:grid-cols-4 {
    gap: 1rem;
  }

  .card-modern {
    padding: 1rem;
  }

  .card-modern .flex.items-center.justify-between {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .card-modern .flex.items-center.justify-between .flex-1 {
    width: 100%;
  }

  .card-modern .w-14.h-14 {
    width: 3rem;
    height: 3rem;
  }

  .card-modern .w-14.h-14 .h-7.w-7 {
    width: 1.25rem;
    height: 1.25rem;
  }

  /* Mobile activity feed */
  .grid.grid-cols-1.lg\\:grid-cols-3 {
    gap: 1.5rem;
  }

  .lg\\:col-span-2 {
    order: 2;
  }

  .space-y-6 > .card-modern {
    order: 1;
  }

  /* Mobile quick actions */
  .space-y-3 .w-full {
    padding: 0.75rem 1rem;
    font-size: 0.875rem;
  }

  /* Mobile recent books */
  .grid.grid-cols-1.md\\:grid-cols-2.lg\\:grid-cols-3 {
    gap: 1rem;
  }

  .interactive-card.glass {
    padding: 1rem;
  }

  /* Mobile modal */
  .fixed.inset-0 .glass-card {
    margin: 1rem;
    max-width: none;
  }
}

@media (max-width: 640px) {
  /* Extra small screens */
  .max-w-7xl.mx-auto {
    padding-left: 0.5rem;
    padding-right: 0.5rem;
  }

  .glass-card.m-6 {
    margin: 0.5rem;
    padding: 1rem;
  }

  .text-3xl.font-bold.display-font {
    font-size: 1.5rem;
    line-height: 2rem;
  }

  .text-xl.font-semibold.display-font {
    font-size: 1.125rem;
  }

  .text-lg.font-semibold {
    font-size: 1rem;
  }

  .card-modern .text-3xl.font-bold {
    font-size: 1.875rem;
  }

  .card-modern .text-2xl.font-bold {
    font-size: 1.5rem;
  }

  .card-modern .text-xl.font-bold {
    font-size: 1.25rem;
  }

  /* Stack activity items vertically on very small screens */
  .flex.items-start.space-x-4 {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .flex.items-start.space-x-4 .flex-shrink-0 {
    align-self: flex-start;
  }

  .flex.items-start.space-x-4 .flex-1.min-w-0 {
    width: 100%;
  }
}
</style>
