<template>
  <div
    v-if="message"
    :class="[
      'rounded-lg p-4 flex items-start gap-3 border animate-scale-in',
      variantClasses.border,
      variantClasses.bg,
      variantClasses.text,
    ]"
    role="alert"
  >
    <font-awesome-icon :icon="icon" :class="['h-5 w-5 mt-0.5', variantClasses.icon]" />
    <div class="text-sm leading-6">
      <slot>
        {{ message }}
      </slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  message?: string | null
  variant?: 'error' | 'success' | 'warning' | 'info'
}

const props = withDefaults(defineProps<Props>(), {
  message: null,
  variant: 'info',
});

const icon = computed(() => {
  switch (props.variant) {
    case 'error':
      return ['fas', 'exclamation-circle'];
    case 'success':
      return ['fas', 'check-circle'];
    case 'warning':
      return ['fas', 'exclamation-triangle'];
    default:
      return ['fas', 'info-circle'];
  }
});

const variantClasses = computed(() => {
  switch (props.variant) {
    case 'error':
      return { bg: 'bg-danger-100/60 dark:bg-red-900/30', border: 'border-red-200 dark:border-red-800', text: 'text-red-800 dark:text-red-300', icon: 'text-red-500' };
    case 'success':
      return { bg: 'bg-success-100/60 dark:bg-green-900/30', border: 'border-green-200 dark:border-green-800', text: 'text-green-800 dark:text-green-300', icon: 'text-green-500' };
    case 'warning':
      return { bg: 'bg-warning-100/60 dark:bg-yellow-900/30', border: 'border-yellow-200 dark:border-yellow-800', text: 'text-yellow-800 dark:text-yellow-300', icon: 'text-yellow-500' };
    default:
      return { bg: 'bg-blue-50 dark:bg-blue-900/30', border: 'border-blue-200 dark:border-blue-800', text: 'text-blue-800 dark:text-blue-300', icon: 'text-blue-500' };
  }
});
</script>
