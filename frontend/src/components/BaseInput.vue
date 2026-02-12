<template>
    <div class="field">
      <label class="label">{{ label }}</label>
      <input
        class="input"
        :type="type"
        :placeholder="placeholder"
        v-model="model"
      />
    </div>
  </template>
  
  <script setup lang="ts">
  const model = defineModel<string>({ default: "" })
  defineProps<{ label: string; type?: string; placeholder?: string }>()
  </script>