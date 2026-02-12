<template>
    <button class="btn" :disabled="disabled" @click="$emit('click')">
      <slot />
    </button>
  </template>
  
  <script setup lang="ts">
  defineProps<{ disabled?: boolean }>()
  defineEmits<{ (e: "click"): void }>()
  </script>