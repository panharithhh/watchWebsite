<template>
  <div class="home">
    <header class="topbar">
      <div class="topbar-row">
        <div class="brand">TOURBILLON10</div>
        <SearchBar
          v-model="searchQuery"
          placeholder="Search wishlist"
          @search="applySearch"
        />
        <div class="auth-links">
          <span class="user-text">Hi, {{ username }}</span>
          <button class="logout-btn" @click="logout">Logout</button>
        </div>
      </div>
      <nav class="nav">
        <button class="nav-link" @click="router.push('/home')">Home</button>
        <span class="nav-pill">Wishlist</span>
      </nav>
    </header>

    <section class="section">
      <h2>Wishlist</h2>
      <div v-if="loading" class="search-state">Loading wishlist...</div>
      <div v-else-if="error" class="search-state error">{{ error }}</div>
      <div v-else-if="!items.length" class="search-state">Your wishlist is empty.</div>
      <div v-else-if="!filteredItems.length" class="search-state">No matching items.</div>
      <div v-else class="search-grid">
        <div v-for="item in filteredItems" :key="item.id" class="search-card">
          <div
            class="search-photo"
            :style="{ backgroundImage: `url(${item.images[0]})` }"
          ></div>
          <div class="search-meta">
            <strong>{{ item.brand }} {{ item.name }}</strong>
            <span>{{ item.description }}</span>
            <span class="seller-line">Seller: {{ sellerLabel(item) }}</span>
            <span class="price">{{ formatPrice(item.price) }}</span>
          </div>
          <div class="search-actions">
            <button class="primary dark" @click="buyNow(item)">Checkout</button>
            <button class="ghost dark" @click="removeItem(item.id)">Remove</button>
          </div>
        </div>
      </div>
    </section>

    <section v-if="checkoutItems.length" class="section">
      <h2>Checkout</h2>
      <div class="cart-panel">
        <div class="cart-head">
          <h3>Wishlist checkout</h3>
          <span>{{ checkoutItems.length }} items</span>
        </div>
        <div class="cart-list">
          <div v-for="item in checkoutItems" :key="item.id" class="cart-item">
            <div>
              <strong>{{ item.brand }} {{ item.name }}</strong>
              <span>{{ formatPrice(item.price) }}</span>
            </div>
          </div>
          <div class="cart-total">
            Total: <strong>{{ formatPrice(checkoutTotal) }}</strong>
          </div>
        </div>
        <p class="cart-note">Demo checkout only — no payment is processed.</p>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue"
import { useRouter } from "vue-router"
import { api } from "@/lib/api"
import SearchBar from "@/components/SearchBar.vue"

type WatchResult = {
  id: number
  name: string
  brand: string
  price: number
  description: string
  image_url?: string
  imageUrl?: string
  seller_name?: string
  sellerName?: string
  images: string[]
}

const router = useRouter()
const username = ref(
  localStorage.getItem("username") ||
    sessionStorage.getItem("username") ||
    "User"
)
const items = ref<WatchResult[]>([])
const loading = ref(false)
const error = ref("")
const checkoutItems = ref<WatchResult[]>([])
const searchQuery = ref("")

const formatPrice = (price: number) => {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(price)
}

const mapImages = (watch: any, idx: number) => {
  const remote = watch.image_url || watch.imageUrl
  const images = remote ? [remote, remote] : [""]
  return { ...watch, images }
}

const sellerLabel = (watch: WatchResult) => {
  return watch.seller_name || watch.sellerName || "Unknown seller"
}

const applySearch = () => {
  searchQuery.value = searchQuery.value.trim()
}

const filteredItems = computed(() => {
  const term = searchQuery.value.trim().toLowerCase()
  if (!term) return items.value
  return items.value.filter((item) => {
    const seller = sellerLabel(item)
    return `${item.brand} ${item.name} ${item.description} ${seller}`
      .toLowerCase()
      .includes(term)
  })
})

const loadWishlist = async () => {
  loading.value = true
  error.value = ""
  try {
    const res = await api<{ wishlist: WatchResult[] }>(
      "http://localhost:8000/wishlist"
    )
    items.value = res.wishlist.map(mapImages)
  } catch (e: any) {
    error.value = e?.message || "Failed to load wishlist"
  } finally {
    loading.value = false
  }
}

const removeItem = async (id: number) => {
  try {
    await api(`http://localhost:8000/wishlist/${id}`, { method: "DELETE" })
    items.value = items.value.filter((item) => item.id !== id)
    checkoutItems.value = checkoutItems.value.filter((item) => item.id !== id)
  } catch (e: any) {
    error.value = e?.message || "Failed to remove"
  }
}

const buyNow = (item: WatchResult) => {
  if (!checkoutItems.value.find((entry) => entry.id === item.id)) {
    checkoutItems.value.push(item)
  }
}

const checkoutTotal = computed(() =>
  checkoutItems.value.reduce((sum, item) => sum + item.price, 0)
)

const logout = () => {
  localStorage.removeItem("auth_token")
  localStorage.removeItem("username")
  localStorage.removeItem("role")
  sessionStorage.removeItem("auth_token")
  sessionStorage.removeItem("username")
  sessionStorage.removeItem("role")
  router.push("/login")
}

onMounted(loadWishlist)
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Manrope:wght@400;500;600&display=swap");

.home {
  min-height: 100vh;
  background: #ffffff;
  color: #121521;
  padding: 20px clamp(16px, 4vw, 48px) 60px;
  font-family: "Manrope", "Segoe UI", sans-serif;
}

.topbar {
  padding: 14px 18px 10px;
  border-radius: 12px;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  position: relative;
}

.topbar-row {
  display: grid;
  grid-template-columns: auto minmax(200px, 1fr) auto;
  gap: 18px;
  align-items: center;
}

.brand {
  font-family: "Playfair Display", serif;
  letter-spacing: 0.2em;
  font-size: 12px;
  text-transform: uppercase;
  font-style: italic;
}


.nav {
  display: flex;
  gap: 22px;
  align-items: center;
  font-size: 12px;
  padding: 10px 0 0;
}

.nav-link {
  border: none;
  background: none;
  color: #374151;
  font-size: 12px;
  cursor: pointer;
  display: inline-flex;
  gap: 6px;
  align-items: center;
}

.nav-pill {
  background: #0f172a;
  color: #fff;
  border-radius: 999px;
  padding: 4px 10px;
  font-size: 11px;
  display: inline-flex;
  gap: 6px;
  align-items: center;
  border: none;
}

.auth-links {
  font-size: 12px;
  color: #374151;
  display: flex;
  gap: 6px;
  align-items: center;
}

.user-text {
  font-size: 12px;
  color: #111827;
}

.logout-btn {
  border: none;
  background: none;
  color: #111827;
  padding: 0;
  text-decoration: underline;
  font-size: 11px;
  cursor: pointer;
}

.section {
  margin-top: 34px;
}

.search-state {
  font-size: 12px;
  color: #6b7280;
  margin-bottom: 12px;
}

.search-state.error {
  color: #b3312d;
}

.search-grid {
  margin-top: 18px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 22px;
}

.search-card {
  background: #ffffff;
  border-radius: 16px;
  border: 1px solid #ededed;
  padding: 12px;
  text-align: left;
  display: grid;
  gap: 10px;
}

.search-photo {
  height: 200px;
  border-radius: 14px;
  background: #e6e9ee;
  background-size: cover;
  background-position: center;
}

.search-meta {
  display: grid;
  gap: 6px;
  font-size: 12px;
  color: #6b7280;
}

.search-meta strong {
  color: #111827;
  font-size: 13px;
}

.search-meta .price {
  color: #111827;
  font-weight: 600;
}

.seller-line {
  color: #4b5563;
  font-size: 11px;
}

.search-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.primary.dark {
  background: #111827;
  color: #fff;
  padding: 8px 14px;
  border-radius: 10px;
  font-size: 12px;
  border: none;
  cursor: pointer;
}

.ghost.dark {
  border: 1px solid #d1d5db;
  background: #ffffff;
  color: #111827;
  padding: 8px 14px;
  border-radius: 10px;
  font-size: 12px;
  cursor: pointer;
}

.cart-panel {
  background: #ffffff;
  border-radius: 16px;
  padding: 16px;
  border: 1px solid #ededed;
  margin-bottom: 16px;
}

.cart-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: #6b7280;
  margin-bottom: 10px;
}

.cart-list {
  display: grid;
  gap: 10px;
}

.cart-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: #6b7280;
  border-bottom: 1px solid #f1f1f1;
  padding-bottom: 8px;
}

.cart-item strong {
  color: #111827;
  display: block;
}

.cart-total {
  text-align: right;
  font-size: 12px;
  color: #111827;
}

.cart-note {
  margin: 8px 0 0;
  font-size: 11px;
  color: #6b7280;
}
</style>
