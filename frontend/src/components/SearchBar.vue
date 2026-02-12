<template>
  <label class="search-bar" :class="variant">
    <button
      class="search-btn"
      type="button"
      :disabled="disabled"
      @click="emitSearch"
    >
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path
          d="M15.5 14h-.8l-.3-.3a6 6 0 1 0-.7.7l.3.3v.8L20 20.5 21.5 19l-6-5zM5.5 10a4.5 4.5 0 1 1 9 0 4.5 4.5 0 0 1-9 0z"
        />
      </svg>
    </button>
    <input
      :value="modelValue"
      type="search"
      :placeholder="placeholder"
      :disabled="disabled"
      @input="onInput"
      @keyup.enter="emitSearch"
    />
  </label>
</template>

<script setup lang="ts">
type Variant = "default" | "admin"

const props = withDefaults(
  defineProps<{
    modelValue: string
    placeholder?: string
    disabled?: boolean
    variant?: Variant
  }>(),
  {
    placeholder: "Search",
    disabled: false,
    variant: "default",
  }
)

const emit = defineEmits<{
  (e: "update:modelValue", value: string): void
  (e: "search"): void
}>()

const onInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  emit("update:modelValue", target.value)
}

const emitSearch = () => {
  if (props.disabled) return
  emit("search")
}
</script>

<style scoped>
.search-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #f5f5f5;
  padding: 8px 12px;
  border-radius: 12px;
}

.search-bar.admin {
  background: #f5f5f4;
  border-radius: 999px;
  padding: 10px 14px;
  border: 1px solid #ecebe7;
}

.search-btn {
  border: none;
  background: transparent;
  padding: 0;
  cursor: pointer;
  display: grid;
  place-items: center;
}

.search-btn:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.search-bar svg {
  width: 18px;
  height: 18px;
  fill: #6b7280;
}

.search-bar input {
  border: none;
  background: transparent;
  outline: none;
  width: 100%;
  font-size: 13px;
  color: #111827;
}

.search-bar.admin input {
  font-size: 14px;
  color: #6b7280;
}

.search-bar input:disabled {
  cursor: not-allowed;
  color: #9ca3af;
}
</style>
