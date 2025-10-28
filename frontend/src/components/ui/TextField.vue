<template>
  <div class="group">
    <label v-if="label" :for="id" class="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2">
      {{ label }}
    </label>
    <div class="relative">
      <div v-if="icon" class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <font-awesome-icon :icon="['fas', icon]" class="h-5 w-5 text-neutral-400 dark:text-neutral-500 group-focus-within:text-primary-500 transition-colors" />
      </div>
      <input
        :id="id"
        :name="name || id"
        :type="type"
        :autocomplete="autocomplete"
        :placeholder="placeholder"
        :value="modelValue"
        @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
        :class="[
          'appearance-none block w-full',
          icon ? 'pl-10' : 'pl-3',
          'pr-3 py-3 rounded-lg',
          'border border-neutral-300 dark:border-neutral-600',
          'bg-white dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100',
          'placeholder-neutral-400 dark:placeholder-neutral-500',
          'focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent',
          'transition-all duration-200'
        ]"
      />
      <p v-if="error" class="mt-2 text-xs text-red-600 dark:text-red-400">{{ error }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  id: string
  label?: string
  name?: string
  type?: string
  placeholder?: string
  autocomplete?: string
  icon?: string
  error?: string | null
  modelValue?: string
}

withDefaults(defineProps<Props>(), {
  type: 'text',
  placeholder: '',
  autocomplete: 'off',
  error: null,
  modelValue: '',
});

defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()
</script>
