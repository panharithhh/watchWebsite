<template>
  <div class="slides-view">
    <header class="slides-header">
      <div class="brand">TOURBILLON10</div>
      <div class="meta">
        <span class="hint">Use  /  or Space</span>
        <span class="counter">{{ activeIndex + 1 }} / {{ slides.length }}</span>
      </div>
    </header>

    <main class="slides-stage">
      <div class="slide-card">
        <div class="slide-flag">Slide {{ activeIndex + 1 }}</div>
        <h1>{{ activeSlide.title }}</h1>
        <p v-if="activeSlide.subtitle" class="subtitle">
          {{ activeSlide.subtitle }}
        </p>
        <ul v-if="activeSlide.bullets" class="bullets">
          <li v-for="bullet in activeSlide.bullets" :key="bullet">
            {{ bullet }}
          </li>
        </ul>
        <div v-if="activeSlide.chips" class="chips">
          <span v-for="chip in activeSlide.chips" :key="chip">{{ chip }}</span>
        </div>
        <div v-if="activeSlide.note" class="note">
          {{ activeSlide.note }}
        </div>
      </div>
    </main>

    <footer class="slides-footer">
      <button class="nav-btn" type="button" @click="prev" :disabled="activeIndex === 0">
        Previous
      </button>
      <div class="dots">
        <button
          v-for="(slide, index) in slides"
          :key="slide.title"
          class="dot"
          :class="{ active: index === activeIndex }"
          type="button"
          @click="goTo(index)"
          :aria-label="`Go to slide ${index + 1}`"
        />
      </div>
      <button
        class="nav-btn"
        type="button"
        @click="next"
        :disabled="activeIndex === slides.length - 1"
      >
        Next
      </button>
    </footer>
    <div class="progress">
      <span :style="{ width: `${progress}%` }" />
    </div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from "vue"

const slides = [
  {
    title: "Tourbillon10 Watch Marketplace",
    subtitle: "A buyer + seller marketplace for luxury watches",
    bullets: [
      "Browse verified listings",
      "Filter by brand and search",
      "Wishlist and seller inventory",
    ],
  },
  {
    title: "Problem",
    subtitle: "Buying and selling watches online is fragmented",
    bullets: [
      "Hard to compare listings",
      "Unclear seller identity",
      "Scattered inventory and promotions",
    ],
  },
  {
    title: "Solution",
    subtitle: "One place to list, browse, and buy",
    bullets: [
      "Unified watch cards across the app",
      "Seller identity shown on every listing",
      "Deals tab with automatic discount pricing",
    ],
  },
  {
    title: "How It Works",
    bullets: [
      "Sellers create listings",
      "Listings appear in buyer view and brand filters",
      "Wishlist saves items for later",
      "Admin can remove listings when needed",
    ],
  },
  {
    title: "Key Features",
    bullets: [
      "Search bar shared across pages",
      "Brand filter based on actual data",
      "Consistent card layout and images",
    ],
    chips: ["Search", "Filters", "Wishlist", "Deals", "Admin"],
  },
  {
    title: "Roles & Views",
    bullets: [
      "Buyer: browse + wishlist",
      "Seller: manage inventory",
      "Admin: manage all listings",
    ],
  },
  {
    title: "Data Flow",
    bullets: [
      "PostgreSQL stores users, watches, wishlist",
      "FastAPI serves search, listings, and auth",
      "Vue app renders shared components",
    ],
  },
  {
    title: "Tech Stack",
    bullets: [
      "Frontend: Vue 3 + Vite",
      "Backend: FastAPI + PostgreSQL",
      "Auth: JWT",
    ],
  },
  {
    title: "Demo Flow",
    bullets: [
      "Login",
      "Home + Search",
      "Brand filter",
      "Wishlist",
      "Admin dashboard",
    ],
  },
  {
    title: "Future Work",
    bullets: [
      "Payments integration",
      "Shipping + tracking",
      "Messaging between buyer and seller",
    ],
    note: "No Stripe used in this build.",
  },
  {
    title: "Thank You",
    subtitle: "Questions?",
  },
]

const activeIndex = ref(0)

const activeSlide = computed(() => slides[activeIndex.value])
const progress = computed(() => ((activeIndex.value + 1) / slides.length) * 100)

const goTo = (index) => {
  if (index < 0 || index >= slides.length) return
  activeIndex.value = index
}

const next = () => {
  if (activeIndex.value < slides.length - 1) activeIndex.value += 1
}

const prev = () => {
  if (activeIndex.value > 0) activeIndex.value -= 1
}

const onKeyDown = (event) => {
  if (event.key === "ArrowRight" || event.key === " ") {
    event.preventDefault()
    next()
  }
  if (event.key === "ArrowLeft") {
    event.preventDefault()
    prev()
  }
}

onMounted(() => {
  window.addEventListener("keydown", onKeyDown)
})

onBeforeUnmount(() => {
  window.removeEventListener("keydown", onKeyDown)
})
</script>

<style scoped>
.slides-view {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: radial-gradient(circle at top, #f4f5f8 0%, #e8eaef 45%, #e1e4ea 100%);
  color: #10131a;
  padding: 32px 32px 48px;
  gap: 24px;
}

.slides-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand {
  font-weight: 600;
  letter-spacing: 0.3em;
  font-size: 14px;
  text-transform: uppercase;
}

.meta {
  display: flex;
  gap: 16px;
  align-items: center;
  font-size: 14px;
  color: #4a5160;
}

.hint {
  background: #ffffff;
  padding: 8px 14px;
  border-radius: 999px;
  border: 1px solid #d4d9e0;
}

.counter {
  font-weight: 600;
}

.slides-stage {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.slide-card {
  width: min(920px, 100%);
  background: #ffffff;
  border-radius: 28px;
  padding: 48px 56px;
  box-shadow: 0 30px 80px rgba(16, 19, 26, 0.12);
  display: grid;
  gap: 18px;
}

.slide-flag {
  text-transform: uppercase;
  font-size: 12px;
  letter-spacing: 0.2em;
  color: #7a8291;
}

h1 {
  font-size: clamp(28px, 4vw, 44px);
  margin: 0;
}

.subtitle {
  font-size: 18px;
  color: #4a5160;
  margin: 0;
}

.bullets {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 10px;
  font-size: 18px;
}

.bullets li::before {
  content: "•";
  color: #1f2937;
  display: inline-block;
  width: 16px;
}

.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.chips span {
  padding: 8px 14px;
  border-radius: 999px;
  background: #10131a;
  color: #ffffff;
  font-size: 13px;
  letter-spacing: 0.04em;
}

.note {
  font-size: 14px;
  color: #7a8291;
}

.slides-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.nav-btn {
  padding: 12px 20px;
  border-radius: 999px;
  border: 1px solid #c8ced8;
  background: #ffffff;
  font-weight: 600;
  cursor: pointer;
}

.nav-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.dots {
  display: flex;
  gap: 8px;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
  border: none;
  background: #c7cdd7;
  cursor: pointer;
}

.dot.active {
  background: #10131a;
  width: 24px;
}

.progress {
  position: relative;
  height: 6px;
  background: rgba(16, 19, 26, 0.08);
  border-radius: 999px;
  overflow: hidden;
}

.progress span {
  display: block;
  height: 100%;
  background: #10131a;
  transition: width 0.25s ease;
}

@media (max-width: 720px) {
  .slides-view {
    padding: 20px;
  }

  .slides-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .slide-card {
    padding: 32px;
  }

  .slides-footer {
    flex-direction: column;
  }
}
</style>
