<template>
  <article
    class="watch-card"
    :class="{ active, clickable }"
    :role="clickable ? 'button' : undefined"
    @click="handleClick"
  >
    <div class="watch-photo" :style="{ backgroundImage: image ? `url(${image})` : '' }">
      <span v-if="badge" class="promo-badge">{{ badge }}</span>
    </div>
    <div class="watch-meta">
      <strong>{{ title }}</strong>
      <span v-if="description">{{ description }}</span>
      <span v-if="seller" class="seller-line">Seller: {{ seller }}</span>
      <span v-if="oldPrice" class="price-old">{{ oldPrice }}</span>
      <span v-if="newPrice" class="price-new">{{ newPrice }}</span>
      <span v-else-if="price">{{ price }}</span>
    </div>
    <div v-if="$slots.actions" class="watch-actions">
      <slot name="actions" />
    </div>
  </article>
</template>

<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    title: string
    image?: string
    description?: string
    seller?: string
    price?: string
    oldPrice?: string
    newPrice?: string
    badge?: string
    clickable?: boolean
    active?: boolean
  }>(),
  {
    image: "",
    description: "",
    seller: "",
    price: "",
    oldPrice: "",
    newPrice: "",
    badge: "",
    clickable: false,
    active: false,
  }
)

const emit = defineEmits<{
  (e: "click"): void
}>()

const handleClick = () => {
  if (props.clickable) {
    emit("click")
  }
}
</script>

<style scoped>
.watch-card {
  background: #ffffff;
  border-radius: 16px;
  border: 1px solid #ededed;
  padding: 12px;
  text-align: left;
  display: grid;
  gap: 10px;
  width: 100%;
  max-width: 360px;
}

.watch-card.clickable {
  cursor: pointer;
}

.watch-card.active {
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
}

.watch-photo {
  width: 100%;
  aspect-ratio: 4 / 5;
  border-radius: 14px;
  background: #e6e9ee;
  background-size: cover;
  background-position: center;
  position: relative;
}

.promo-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  background: #111827;
  color: #fff;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 10px;
  font-weight: 600;
}

.watch-meta {
  display: grid;
  gap: 6px;
  font-size: 12px;
  color: #6b7280;
}

.watch-meta strong {
  color: #111827;
  font-size: 13px;
}

.seller-line {
  color: #4b5563;
  font-size: 11px;
}

.price-old {
  color: #9ca3af;
  text-decoration: line-through;
  font-size: 11px;
}

.price-new {
  color: #111827;
  font-weight: 600;
}

.watch-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.watch-actions button:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}
</style>
