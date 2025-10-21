<template>
  <div v-if="toasts.length > 0" class="fixed top-4 right-4 z-50 space-y-2">
    <TransitionGroup name="toast">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="max-w-sm w-full bg-white dark:bg-gray-800 shadow-lg rounded-lg pointer-events-auto ring-1 ring-black ring-opacity-5 border border-gray-200 dark:border-gray-700"
      >
        <div class="p-4">
          <div class="flex items-start">
            <div class="flex-shrink-0">
              <font-awesome-icon
                :icon="['fas', getToastIcon(toast.type)]"
                :class="getToastIconClass(toast.type)"
                class="h-5 w-5"
              />
            </div>
            <div class="ml-3 w-0 flex-1 pt-0.5">
              <p class="text-sm font-medium text-gray-900 dark:text-white">
                {{ toast.title }}
              </p>
              <p v-if="toast.message" class="mt-1 text-sm text-gray-500 dark:text-gray-400">
                {{ toast.message }}
              </p>
            </div>
            <div class="ml-4 flex-shrink-0 flex">
              <button
                @click="removeToast(toast.id)"
                class="bg-white dark:bg-gray-800 rounded-md inline-flex text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                <span class="sr-only">Close</span>
                <font-awesome-icon :icon="['fas', 'times']" class="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Toast {
  id: number
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message?: string
  duration?: number
}

const toasts = ref<Toast[]>([])
let toastId = 0

const addToast = (toast: Omit<Toast, 'id'>) => {
  const id = ++toastId
  const newToast: Toast = {
    id,
    duration: 5000,
    ...toast
  }

  toasts.value.push(newToast)

  // Auto remove after duration
  if (newToast.duration && newToast.duration > 0) {
    setTimeout(() => {
      removeToast(id)
    }, newToast.duration)
  }
}

const removeToast = (id: number) => {
  const index = toasts.value.findIndex(t => t.id === id)
  if (index > -1) {
    toasts.value.splice(index, 1)
  }
}

const getToastIcon = (type: string) => {
  switch (type) {
    case 'success': return 'check-circle'
    case 'error': return 'exclamation-circle'
    case 'warning': return 'exclamation-triangle'
    case 'info': return 'info-circle'
    default: return 'info-circle'
  }
}

const getToastIconClass = (type: string) => {
  switch (type) {
    case 'success': return 'text-green-400'
    case 'error': return 'text-red-400'
    case 'warning': return 'text-yellow-400'
    case 'info': return 'text-blue-400'
    default: return 'text-blue-400'
  }
}

// Global toast function
const toast = {
  success: (title: string, message?: string) => addToast({ type: 'success', title, message }),
  error: (title: string, message?: string) => addToast({ type: 'error', title, message }),
  warning: (title: string, message?: string) => addToast({ type: 'warning', title, message }),
  info: (title: string, message?: string) => addToast({ type: 'info', title, message })
}

// Make toast available globally
if (typeof window !== 'undefined') {
  (window as any).$toast = toast
}

defineExpose({
  addToast,
  removeToast,
  toast
})
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

.toast-move {
  transition: transform 0.3s ease;
}
</style>