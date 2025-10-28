<template>
  <div class="group">
    <label v-if="label" :for="id" class="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2">
      {{ label }}
    </label>
    <div class="relative">
      <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <font-awesome-icon :icon="['fas', 'lock']" class="h-5 w-5 text-neutral-400 dark:text-neutral-500 group-focus-within:text-primary-500 transition-colors" />
      </div>
      <input
        :id="id"
        :name="name || id"
        :type="show ? 'text' : 'password'"
        :autocomplete="autocomplete"
        :placeholder="placeholder"
        :value="modelValue"
        @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
        :class="[
          'appearance-none block w-full pl-10 pr-10 py-3 rounded-lg',
          'border border-neutral-300 dark:border-neutral-600',
          'bg-white dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100',
          'placeholder-neutral-400 dark:placeholder-neutral-500',
          'focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent',
          'transition-all duration-200'
        ]"
      />
      <button type="button" @click="show = !show" class="absolute inset-y-0 right-0 pr-3 flex items-center">
        <font-awesome-icon :icon="['fas', show ? 'eye-slash' : 'eye']" class="h-5 w-5 text-neutral-400 hover:text-neutral-600 dark:text-neutral-500 dark:hover:text-neutral-300 transition-colors cursor-pointer" />
      </button>
      <p v-if="error" class="mt-2 text-xs text-red-600 dark:text-red-400">{{ error }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

interface Props {
  id: string
  label?: string
  name?: string
  placeholder?: string
  autocomplete?: string
  error?: string | null
  modelValue?: string
}

const show = ref(false);

withDefaults(defineProps<Props>(), {
  placeholder: '••••••••',
  autocomplete: 'current-password',
  error: null,
  modelValue: '',
});

defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()
</script>
