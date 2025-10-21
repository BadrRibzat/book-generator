<template>
  <Layout>
    <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
      <!-- Dashboard Header with Logo -->
      <div class="bg-gradient-to-r from-amber-500 to-orange-600 text-white py-8">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-4">
              <img src="/logo.svg" alt="BookAI Logo" class="h-12 w-auto" />
              <div>
                <h1 class="text-3xl font-bold">Welcome back, {{ user?.username }}!</h1>
                <p class="text-amber-100">Manage your AI-powered book generation dashboard</p>
              </div>
            </div>
            <div class="text-right">
              <div class="text-2xl font-bold">{{ userProfile?.subscription_tier || 'FREE' }}</div>
              <div class="text-sm text-amber-100">Current Plan</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content -->
      <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <!-- Books Generated -->
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6 border border-gray-200 dark:border-gray-700">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Books Generated</p>
                <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ stats.totalBooks }}</p>
              </div>
              <div class="w-12 h-12 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center">
                <font-awesome-icon :icon="['fas', 'book']" class="h-6 w-6 text-blue-600 dark:text-blue-400" />
              </div>
            </div>
          </div>

          <!-- This Month -->
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6 border border-gray-200 dark:border-gray-700">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Today</p>
                <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ stats.dailyBooks }}</p>
                <p class="text-xs text-gray-500 dark:text-gray-400">{{ stats.dailyLimit }} limit</p>
              </div>
              <div class="w-12 h-12 bg-green-100 dark:bg-green-900 rounded-lg flex items-center justify-center">
                <font-awesome-icon :icon="['fas', 'calendar-day']" class="h-6 w-6 text-green-600 dark:text-green-400" />
              </div>
            </div>
          </div>

          <!-- Usage Progress -->
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6 border border-gray-200 dark:border-gray-700">
            <div class="flex items-center justify-between">
              <div class="flex-1">
                <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Usage Progress</p>
                <div class="mt-2">
                  <div class="flex justify-between text-sm">
                    <span class="text-gray-900 dark:text-white">{{ stats.dailyBooks }}</span>
                    <span class="text-gray-500 dark:text-gray-400">{{ stats.dailyLimit }}</span>
                  </div>
                  <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mt-1">
                    <div 
                      class="bg-gradient-to-r from-amber-500 to-orange-500 h-2 rounded-full transition-all duration-500"
                      :style="{ width: `${Math.min((stats.dailyBooks / stats.dailyLimit) * 100, 100)}%` }"
                    ></div>
                  </div>
                </div>
              </div>
              <div class="w-12 h-12 bg-amber-100 dark:bg-amber-900 rounded-lg flex items-center justify-center ml-4">
                <font-awesome-icon :icon="['fas', 'chart-line']" class="h-6 w-6 text-amber-600 dark:text-amber-400" />
              </div>
            </div>
          </div>

          <!-- Account Status -->
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6 border border-gray-200 dark:border-gray-700">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Account Status</p>
                <p class="text-lg font-bold" :class="getStatusColorClass(userProfile?.subscription_status)">
                  {{ userProfile?.subscription_status || 'INACTIVE' }}
                </p>
                <p class="text-xs text-gray-500 dark:text-gray-400">{{ getStatusDescription(userProfile?.subscription_status) }}</p>
              </div>
              <div class="w-12 h-12 rounded-lg flex items-center justify-center" :class="getStatusBgClass(userProfile?.subscription_status)">
                <font-awesome-icon :icon="['fas', 'star']" class="h-6 w-6 text-white" />
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Activity -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <!-- Recent Books -->
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
            <div class="p-6 border-b border-gray-200 dark:border-gray-700">
              <h2 class="text-lg font-semibold text-gray-900 dark:text-white">Recent Books</h2>
              <p class="text-sm text-gray-600 dark:text-gray-400">Your latest generated books</p>
            </div>
            <div class="p-6">
              <div v-if="recentBooks.length === 0" class="text-center py-8">
                <img src="/logo.svg" alt="BookAI Logo" class="mx-auto h-16 w-auto opacity-20 mb-4" />
                <p class="text-gray-600 dark:text-gray-400 mb-4">No books generated yet</p>
                <router-link
                  to="/profile/create"
                  class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 transition-all duration-200"
                >
                  <font-awesome-icon :icon="['fas', 'plus']" class="mr-2" />
                  Create Your First Book
                </router-link>
              </div>
              <div v-else class="space-y-4">
                <div
                  v-for="book in recentBooks"
                  :key="book.id"
                  class="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                >
                  <div class="flex items-center space-x-3">
                    <div class="w-10 h-10 bg-gradient-to-br from-amber-500 to-orange-500 rounded-lg flex items-center justify-center">
                      <font-awesome-icon :icon="['fas', 'book']" class="w-5 h-5 text-white" />
                    </div>
                    <div>
                      <h3 class="text-sm font-medium text-gray-900 dark:text-white">{{ book.title || 'Untitled Book' }}</h3>
                      <p class="text-xs text-gray-500 dark:text-gray-400">{{ formatDate(book.created_at) }}</p>
                    </div>
                  </div>
                  <div class="flex items-center space-x-2">
                    <span
                      class="px-2 py-1 text-xs font-medium rounded-full"
                      :class="getStatusBadgeClass(book.status)"
                    >
                      {{ book.status }}
                    </span>
                    <router-link
                      :to="`/profile/books/${book.id}`"
                      class="text-sm text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 px-2 py-1 rounded"
                    >
                      View
                    </router-link>
                    <button
                      @click="confirmDeleteBook(book)"
                      class="text-sm text-red-600 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300 px-2 py-1 rounded hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
                      title="Delete book"
                    >
                      <font-awesome-icon :icon="['fas', 'trash']" class="w-3 h-3" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick Actions & Subscription -->
          <div class="space-y-8">
            <!-- Quick Actions -->
            <div class="bg-gradient-to-r from-amber-500 to-orange-500 rounded-lg p-6 text-white">
              <div class="flex items-center space-x-3 mb-4">
                <img src="/logo.svg" alt="BookAI Logo" class="h-8 w-auto" />
                <h2 class="text-xl font-bold">Ready to create?</h2>
              </div>
              <p class="text-amber-100 mb-4">Generate professional books with AI-powered content and covers</p>
              <div class="flex flex-col sm:flex-row gap-3">
                <router-link
                  to="/profile/create"
                  class="bg-white text-orange-600 px-6 py-3 rounded-lg font-medium hover:bg-gray-50 transition-colors text-center flex items-center justify-center"
                >
                  <font-awesome-icon :icon="['fas', 'plus']" class="mr-2" />
                  Create New Book
                </router-link>
                <router-link
                  to="/profile/books"
                  class="bg-white/20 backdrop-blur-sm text-white px-6 py-3 rounded-lg font-medium hover:bg-white/30 transition-colors text-center flex items-center justify-center"
                >
                  <font-awesome-icon :icon="['fas', 'book']" class="mr-2" />
                  View All Books
                </router-link>
              </div>
            </div>

            <!-- Subscription Info -->
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
              <div class="p-6 border-b border-gray-200 dark:border-gray-700">
                <h2 class="text-lg font-semibold text-gray-900 dark:text-white">Subscription Details</h2>
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
                    class="w-full bg-gradient-to-r from-amber-500 to-orange-500 text-white px-4 py-2 rounded-lg font-medium hover:from-amber-600 hover:to-orange-600 transition-all duration-200 text-center block"
                  >
                    Upgrade Plan
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md w-full mx-4">
        <div class="flex items-center space-x-3 mb-4">
          <div class="w-10 h-10 bg-red-100 dark:bg-red-900 rounded-full flex items-center justify-center">
            <font-awesome-icon :icon="['fas', 'exclamation-triangle']" class="w-5 h-5 text-red-600 dark:text-red-400" />
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
            class="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
            :disabled="isDeleting"
          >
            Cancel
          </button>
          <button
            @click="deleteBook"
            class="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
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
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useBooksStore } from '../stores/books'
import Layout from '../components/Layout.vue'
import apiClient from '../services/api'

interface Book {
  id: number
  title: string
  status: string
  created_at: string
}

interface UserProfile {
  subscription_tier?: string
  subscription_status?: string
  books_used_today?: number
  books_per_day?: number
  total_books?: number
}

const authStore = useAuthStore()
const booksStore = useBooksStore()

// State
const stats = ref({
  totalBooks: 0,
  dailyBooks: 0,
  dailyLimit: 1,
  revenueGenerated: 0
})

const recentBooks = ref<Book[]>([])
const userProfile = ref<UserProfile>({})

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

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
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
    
    // If it was created today, update daily count
    const bookDate = new Date(bookToDelete.value.created_at)
    const today = new Date()
    if (bookDate.toDateString() === today.toDateString()) {
      stats.value.dailyBooks = Math.max(0, stats.value.dailyBooks - 1)
    }
    
    showDeleteModal.value = false
    bookToDelete.value = null
  } catch (error) {
    console.error('Failed to delete book:', error)
    alert('Failed to delete book. Please try again.')
  } finally {
    isDeleting.value = false
  }
}

const cancelDelete = () => {
  showDeleteModal.value = false
  bookToDelete.value = null
}

// Lifecycle
onMounted(async () => {
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
    } else {
      // Fallback: fetch books data separately
      await booksStore.fetchBooks()
      const books = booksStore.books || []
      
      // Set books data
      recentBooks.value = books.slice(0, 5)

      // Calculate stats from books data
      stats.value.totalBooks = books.length
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
  }
})
</script>
