<template>
  <div class="home">
    <header class="topbar">
      <div class="topbar-row">

        <div class="brand">TOURBILLON10</div>

        <SearchBar v-model="query" placeholder="Search" @search="performSearch" />

        <div class="auth-links" v-if="!isAuthed">
          <RouterLink to="/login">Log in</RouterLink>
          <span>or</span>
          <RouterLink to="/signup">register</RouterLink>
        </div>
        <div class="auth-links" v-else>
          <span class="user-text">Hi, {{ username }}</span>
          <button class="logout-btn" @click="logout">Logout</button>
        </div>
      </div>

      <nav class="nav">
        <button
          class="nav-link"
          :class="{ active: showBuyMenu }"
          @click="toggleBuyMenu"
        >
          Buy a watch <span>▾</span>
        </button>
        <button v-if="isSeller" class="nav-link" @click="router.push('/sell')">
          Sell a watch <span>▾</span>
        </button>
        <button
          v-if="!isSeller"
          class="nav-link"
          @click="router.push('/wishlist')"
        >
          Wishlist
        </button>
      </nav>

      <section v-if="showBuyMenu" class="buy-menu">
        <div class="buy-menu-col">
          <h4>Brands</h4>
          <div class="buy-menu-list">
            <button
              v-for="brand in brandFilters"
              :key="brand"
              @click="handleBrandClick(brand)"
            >
              {{ brand }}
            </button>
            <span v-if="!brandFilters.length" class="empty-note">No brands yet.</span>
          </div>
        </div>
        <div class="buy-menu-col">
          <h4>Categories</h4>
          <div class="buy-menu-list">
            <button
              v-for="item in buyMenu.categories"
              :key="item"
              @click="handleSearchClick(item)"
            >
              {{ item }}
            </button>
          </div>
        </div>
        <div class="buy-menu-col">
          <h4>Services</h4>
          <div class="buy-menu-list">
            <button
              v-for="item in buyMenu.services"
              :key="item"
              @click="handleServiceClick"
            >
              {{ item }}
            </button>
          </div>
        </div>
      </section>
    </header>

    <div v-if="!isSearchMode">
    <section class="hero">
      <div class="hero-text">
        <h1>GET YOUR TIMEPIECES HERE</h1>
        <p>
          Curated modern classics and collector favorites. Discover verified
          listings with transparent pricing and instant support.
        </p>
        <button class="primary" @click="handleSearchClick('Featured')">Discover Now</button>
      </div>
      <div class="hero-art" aria-hidden="true">
        <div class="watch-shell"></div>
      </div>
    </section>

    <section class="section">
      <h2>Brands</h2>
      <div v-if="brandFilters.length" class="brand-grid">
        <button
          v-for="brand in brandFilters"
          :key="brand"
          class="brand-chip"
          @click="handleBrandClick(brand)"
        >
          {{ brand }}
        </button>
      </div>
      <p v-else class="section-note">No brands available yet.</p>
    </section>

    <section class="section protection">
      <div class="protection-card">
        <h3>Buyer Protection</h3>
        <ul>
          <li>Commitment to authenticity</li>
          <li>Global money-back guarantee</li>
          <li>Strict dealer guidelines</li>
          <li>Insured shipments</li>
        </ul>
        <button class="ghost">Learn more about security</button>
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <h2>{{ topListings.length ? "Top Listings" : "Our Top Picks" }}</h2>
      </div>
      <div class="listing-tabs">
        <button
          class="listing-tab"
          :class="{ active: listingTab === 'all' }"
          type="button"
          @click="listingTab = 'all'"
        >
          All listings
        </button>
        <button
          class="listing-tab"
          :class="{ active: listingTab === 'deals' }"
          type="button"
          @click="listingTab = 'deals'"
        >
          Deals
        </button>
      </div>
      <div v-if="listingTab === 'all'" class="card-grid">
        <WatchCard
          v-for="item in topListings"
          :key="item.label"
          :title="item.label"
          :description="item.description"
          :seller="item.seller"
          :price="item.price"
          :image="item.image"
          :badge="item.promo"
          clickable
          @click="handleSearchClick(item.query)"
        />
      </div>
      <div v-else>
        <div v-if="!discountedListings.length" class="search-state">
          No discounted listings yet.
        </div>
        <div v-else class="card-grid">
          <WatchCard
            v-for="item in discountedListings"
            :key="item.id"
            :title="item.label"
            :description="item.description"
            :seller="item.seller"
            :old-price="item.originalPrice"
            :new-price="item.discountedPrice"
            :image="item.image"
            :badge="item.badge"
            clickable
            @click="handleSearchClick(item.query)"
          />
        </div>
      </div>
    </section>

    </div>

    <section v-if="isSearchMode" class="section">
      <div v-if="isSearchMode" class="search-breadcrumb">
        <button class="crumb-link" @click="resetHome">Home</button>
        <span>›</span>
        <span>{{ query }}</span>
      </div>
      <div v-if="activeBrand" class="filter-row">
        <span class="filter-pill">Brand: {{ activeBrand }}</span>
        <button class="filter-clear" type="button" @click="clearBrandFilter">
          Clear filter
        </button>
      </div>
      <div v-if="searchError" class="search-state error">{{ searchError }}</div>
      <div v-else-if="searchLoading" class="search-state">Searching...</div>
      <div v-else-if="!primaryResult" class="search-state">No results.</div>
      <p v-if="isSeller" class="role-note">
        Seller accounts can view listings only. Shopping actions are disabled.
      </p>

      <div v-if="isSearchMode && results.length" class="search-grid">
        <WatchCard
          v-for="watch in results"
          :key="watch.id"
          :title="`${watch.brand} ${watch.name}`"
          :description="watch.description"
          :seller="sellerLabel(watch)"
          :price="formatPrice(watch.price)"
          :image="watch.images[0]"
          :badge="promotionFor(watch.id)?.discount || (promotionFor(watch.id) ? 'Deal' : '')"
          :active="watch.id === selectedId"
          clickable
          @click="selectResult(watch.id)"
        >
          <template #actions>
            <button
              class="primary dark"
              :disabled="isSeller"
              @click.stop="buyNow(watch)"
            >
              Buy
            </button>
            <button
              class="ghost dark"
              :disabled="isSeller"
              @click.stop="addToWishlist(watch)"
            >
              Add to wishlist
            </button>
          </template>
        </WatchCard>
      </div>

      <div v-else-if="primaryResult" class="detail-card">
        <div class="detail-images">
          <div
            v-for="(img, idx) in primaryResult.images.slice(0, 2)"
            :key="idx"
            class="detail-photo"
            :style="{ backgroundImage: `url(${img})` }"
          ></div>
        </div>
        <div class="detail-info">
          <h3>{{ primaryResult.name }}</h3>
          <p>{{ primaryResult.description }}</p>
          <span class="seller-line">Seller: {{ sellerLabel(primaryResult) }}</span>
          <strong>{{ formatPrice(primaryResult.price) }}</strong>
          <div class="detail-actions">
            <button
              class="primary dark"
              :disabled="isSeller"
              @click="buyNow(primaryResult)"
            >
              Buy
            </button>
            <button
              class="ghost dark"
              :disabled="isSeller"
              @click="addToWishlist(primaryResult)"
            >
              Add to wishlist
            </button>
          </div>
          <p v-if="promotionFor(primaryResult.id)" class="promo-note">
            Promotion: {{ promotionFor(primaryResult.id)?.title }}
          </p>
          <p v-if="actionMessage" class="action-message">{{ actionMessage }}</p>
        </div>
      </div>

    </section>

    <section v-if="cart.length" class="section" ref="purchaseRef">
      <h2>Purchase</h2>
      <div class="cart-panel">
        <div class="cart-head">
          <h3>Cart</h3>
          <span v-if="cart.length">{{ cart.length }} items</span>
        </div>
        <div v-if="cart.length" class="cart-list">
          <div v-for="item in cart" :key="item.id" class="cart-item">
            <div>
              <strong>{{ item.brand }} {{ item.name }}</strong>
              <span>{{ formatPrice(item.price) }}</span>
            </div>
            <button class="remove-btn" @click="removeFromCart(item.id)">Remove</button>
          </div>
          <div class="cart-total">
            Total: <strong>{{ formatPrice(cartTotal) }}</strong>
          </div>
        </div>
        <div v-else class="cart-empty">Your cart is empty.</div>
        <p class="cart-note">Demo checkout only — no payment is processed.</p>
      </div>
      <div class="form-card">
        <h3>Purchase Information</h3>
        <div class="form-grid">
          <label>
            Card
            <input type="text" placeholder="Card number" />
          </label>
          <label>
            Payment
            <input type="text" placeholder="Name on card" />
          </label>
          <div class="form-row">
            <label>
              CVC
              <input type="text" placeholder="CVC" />
            </label>
            <label>
              Date
              <input type="text" placeholder="MM/YY" />
            </label>
          </div>
          <label>
            Location
            <input type="text" placeholder="City, Country" />
          </label>
          <label>
            Postal zip
            <input type="text" placeholder="ZIP" />
          </label>
          <button class="primary dark" type="button" :disabled="!cart.length" @click="placeOrder">
            Submit
          </button>
          <p v-if="purchaseMessage" class="action-message">{{ purchaseMessage }}</p>
        </div>
      </div>
    </section>

  </div>
</template>

<script setup lang="ts">
import { computed, nextTick, onMounted, ref, watch } from "vue"
import { useRoute, useRouter } from "vue-router"
import { api } from "@/lib/api"
import WatchCard from "@/components/WatchCard.vue"
import SearchBar from "@/components/SearchBar.vue"

type WatchResult = {
  id: number
  name: string
  brand: string
  price: number
  description: string
  images: string[]
  image_url?: string
  imageUrl?: string
  seller_name?: string
  sellerName?: string
}

type Promotion = {
  id: number
  title: string
  description: string
  watch_id?: number
  watchId?: number
  discount?: string
  valid_until?: string
}

type PromotionResponse = {
  promotions: Promotion[]
}

type ListingCard = {
  label: string
  query: string
  price: string
  image: string
  promo?: string
  description?: string
  seller?: string
}

type DiscountedCard = {
  id: number
  label: string
  query: string
  image: string
  badge: string
  originalPrice: string
  discountedPrice: string
  description?: string
  seller?: string
}

const router = useRouter()
const route = useRoute()
const username = ref(
  localStorage.getItem("username") ||
    sessionStorage.getItem("username") ||
    "User"
)

const role = ref(
  localStorage.getItem("role") ||
    sessionStorage.getItem("role") ||
    "buyer"
)

const query = ref("")
const results = ref<WatchResult[]>([])
const selectedId = ref<number | null>(null)
const searchLoading = ref(false)
const searchError = ref("")
const showBuyMenu = ref(false)
const cart = ref<WatchResult[]>([])
const actionMessage = ref("")
const purchaseMessage = ref("")
const purchaseRef = ref<HTMLElement | null>(null)
const promotions = ref<Promotion[]>([])
const catalog = ref<WatchResult[]>([])
const activeBrand = ref<string | null>(null)
const listingTab = ref<"all" | "deals">("all")
const buyMenu = {
  categories: [
    "Men watches",
    "Swiss watch",
    "Women watches",
    "Chronograph",
    "Tourbillon",
    "Affordable watches",
  ],
  services: ["Repair"],
}

const brandFilters = computed(() => {
  if (!catalog.value.length) return []
  const set = new Set(
    catalog.value
      .map((watch) => (watch.brand || "").trim())
      .filter((brand) => brand.length > 0)
  )
  return Array.from(set).sort((a, b) => a.localeCompare(b))
})

const primaryResult = computed(() => {
  if (!results.value.length) return null
  if (selectedId.value === null) return results.value[0]
  return results.value.find((r) => r.id === selectedId.value) || results.value[0]
})

const promoMap = computed(() => {
  const map = new Map<number, Promotion>()
  promotions.value.forEach((promo) => {
    const watchId = promo.watch_id ?? promo.watchId
    if (watchId) {
      map.set(watchId, promo)
    }
  })
  return map
})

const parseDiscount = (discount?: string) => {
  if (!discount) return null
  const trimmed = discount.trim()
  if (!trimmed) return null
  const numMatch = trimmed.replace(/,/g, "").match(/-?\\d+(?:\\.\\d+)?/)
  if (!numMatch) return null
  const value = Number(numMatch[0])
  if (!Number.isFinite(value) || value <= 0) return null
  const isPercent = trimmed.includes("%")
  return { value, isPercent }
}

const discountedPrice = (price: number, discount?: string) => {
  const parsed = parseDiscount(discount)
  if (!parsed) return price
  if (parsed.isPercent) {
    const next = price * (1 - parsed.value / 100)
    return Math.max(0, next)
  }
  return Math.max(0, price - parsed.value)
}

const discountedListings = computed<DiscountedCard[]>(() => {
  if (!catalog.value.length) return []
  const items: DiscountedCard[] = []
  catalog.value.forEach((watch) => {
    const promo = promoMap.value.get(watch.id)
    if (!promo) return
    const original = formatPrice(watch.price)
    const discounted = formatPrice(discountedPrice(watch.price, promo.discount))
    items.push({
      id: watch.id,
      label: `${watch.brand} ${watch.name}`,
      query: watch.name,
      image: watch.image_url || watch.imageUrl || "",
      badge: promo.discount || "Deal",
      originalPrice: original,
      discountedPrice: discounted,
      description: watch.description,
      seller: sellerLabel(watch),
    })
  })
  return items
})

const topListings = computed(() => {
  if (!catalog.value.length) return []
  return catalog.value.map((watch) => {
    const promo = promoMap.value.get(watch.id)
    return {
      label: `${watch.brand} ${watch.name}`,
      query: watch.name,
      price: formatPrice(watch.price),
      image: watch.image_url || watch.imageUrl || "",
      promo: promo?.discount || (promo ? "Deal" : undefined),
      description: watch.description,
      seller: sellerLabel(watch),
    } as ListingCard
  })
})

const isAuthed = computed(() => {
  return Boolean(
    localStorage.getItem("auth_token") ||
      sessionStorage.getItem("auth_token")
  )
})

const isSeller = computed(() => role.value === "seller")
const isSearchMode = computed(() => query.value.trim().length > 0)
const cartTotal = computed(() =>
  cart.value.reduce((sum, item) => sum + item.price, 0)
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

const formatPrice = (price: number) => {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(price)
}

const sellerLabel = (watch: WatchResult) => {
  return watch.seller_name || watch.sellerName || "Unknown seller"
}

const promotionFor = (watchId: number) => {
  return promotions.value.find((promo) => {
    const id = promo.watch_id ?? promo.watchId
    return id === watchId
  })
}

const performSearch = async (options?: { brand?: string }) => {
  searchError.value = ""
  actionMessage.value = ""
  searchLoading.value = true
  try {
    const params = new URLSearchParams()
    if (options?.brand) {
      params.set("brand", options.brand)
      activeBrand.value = options.brand
    } else if (query.value.trim()) {
      params.set("q", query.value)
      activeBrand.value = null
    } else {
      activeBrand.value = null
    }
    const url = `http://localhost:8000/search${params.toString() ? `?${params}` : ""}`
    const res = await api<{ results: WatchResult[] }>(url)
    results.value = res.results.map((watch) => {
      const remote = watch.image_url || watch.imageUrl
      const images = remote ? [remote, remote] : [""]
      return { ...watch, images }
    })
    selectedId.value = results.value[0]?.id ?? null
  } catch (e: any) {
    searchError.value = e?.message || "Search failed"
  } finally {
    searchLoading.value = false
  }
}

const selectResult = (id: number) => {
  selectedId.value = id
}

const toggleBuyMenu = () => {
  showBuyMenu.value = !showBuyMenu.value
}

const handleSearchClick = async (value: string) => {
  query.value = value
  await performSearch()
  if (showBuyMenu.value) {
    showBuyMenu.value = false
  }
}

const handleBrandClick = async (brand: string) => {
  query.value = brand
  await performSearch({ brand })
  if (showBuyMenu.value) {
    showBuyMenu.value = false
  }
}

const clearBrandFilter = () => {
  activeBrand.value = null
  query.value = ""
  results.value = []
  selectedId.value = null
  searchError.value = ""
  searchLoading.value = false
}

const handleServiceClick = async () => {
  if (showBuyMenu.value) {
    showBuyMenu.value = false
  }
  await router.push("/repair")
}

const resetHome = () => {
  query.value = ""
  results.value = []
  selectedId.value = null
  searchError.value = ""
  searchLoading.value = false
  activeBrand.value = null
}

const requireBuyerAccess = async () => {
  if (!isAuthed.value) {
    actionMessage.value = "Please sign up or log in to add items to cart."
    await nextTick()
    await router.push("/signup")
    return false
  }
  if (isSeller.value) {
    actionMessage.value = "Seller accounts can view listings only."
    return false
  }
  return true
}

const addToCart = async (item: WatchResult) => {
  if (!(await requireBuyerAccess())) {
    return false
  }
  if (!cart.value.find((entry) => entry.id === item.id)) {
    cart.value.push(item)
  }
  actionMessage.value = `${item.brand} ${item.name} added to cart`
  return true
}

const addToWishlist = async (item: WatchResult) => {
  if (!(await requireBuyerAccess())) {
    return false
  }
  try {
    await api(`http://localhost:8000/wishlist/${item.id}`, { method: "POST" })
    await router.push("/wishlist")
    return true
  } catch (e: any) {
    actionMessage.value = e?.message || "Failed to add to wishlist"
    return false
  }
}

const removeFromCart = (id: number) => {
  cart.value = cart.value.filter((item) => item.id !== id)
}

const buyNow = async (item: WatchResult) => {
  if (!(await requireBuyerAccess())) return
  await addToCart(item)
  purchaseMessage.value = "Demo checkout only — no payment is processed."
  await nextTick()
  purchaseRef.value?.scrollIntoView({ behavior: "smooth", block: "start" })
}

const placeOrder = () => {
  if (!cart.value.length) return
  purchaseMessage.value = "Order submitted (demo)."
}

const loadPromotions = async () => {
  try {
    const res = await api<PromotionResponse>("http://localhost:8000/promotion")
    promotions.value = res.promotions || []
  } catch {
    promotions.value = []
  }
}

const loadCatalog = async () => {
  try {
    const res = await api<{ results: WatchResult[] }>("http://localhost:8000/search")
    catalog.value = res.results.map((watch) => {
      const remote = watch.image_url || watch.imageUrl
      const images = remote ? [remote, remote] : [""]
      return { ...watch, images }
    })
  } catch {
    catalog.value = []
  }
}

const syncFromRoute = async () => {
  const q = route.query.q
  if (typeof q === "string" && q.trim()) {
    query.value = q
    await performSearch()
    return
  }
  performSearch()
}

onMounted(() => {
  syncFromRoute()
  loadPromotions()
  loadCatalog()
})

watch(
  () => route.query.q,
  () => {
    syncFromRoute()
  }
)
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

.nav-link:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.nav-link.active {
  color: #111827;
  font-weight: 600;
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
  cursor: pointer;
}

.nav-pill em {
  background: #3b82f6;
  color: #fff;
  font-style: normal;
  font-size: 9px;
  border-radius: 999px;
  padding: 2px 6px;
}

.buy-menu {
  margin-top: 18px;
  background: #111319;
  color: #ffffff;
  border-radius: 18px;
  padding: 32px clamp(20px, 4vw, 44px);
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 32px;
  border: 1px solid #1f2430;
  box-shadow: 0 18px 32px rgba(5, 6, 10, 0.35);
}

.buy-menu-col h4 {
  margin: 0 0 12px;
  font-size: 16px;
  font-weight: 600;
}

.buy-menu-list {
  display: grid;
  gap: 12px;
}

.buy-menu-list button {
  text-align: left;
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.85);
  font-size: 14px;
  cursor: pointer;
  padding: 0;
}

.buy-menu-list button:hover {
  color: #ffffff;
}

.buy-menu-list .empty-note {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
}

.section-note {
  margin-top: 12px;
  font-size: 13px;
  color: #6b7280;
}

.auth-links {
  font-size: 12px;
  color: #374151;
  display: flex;
  gap: 6px;
  align-items: center;
}

.auth-links a {
  color: inherit;
  text-decoration: none;
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

.hero {
  margin-top: 20px;
  background: #111319;
  color: #fff;
  border-radius: 24px;
  padding: clamp(28px, 5vw, 54px);
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 24px;
  position: relative;
  overflow: hidden;
}

.hero-text h1 {
  font-size: clamp(28px, 3.6vw, 42px);
  margin: 0 0 14px;
}

.hero-text p {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  max-width: 420px;
  margin: 0 0 18px;
}

.primary {
  border: none;
  background: #ffffff;
  color: #0f1116;
  padding: 10px 18px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
}

.primary.small {
  padding: 8px 14px;
}

.hero-art {
  display: grid;
  place-items: center;
}

.watch-shell {
  width: min(240px, 60vw);
  aspect-ratio: 1 / 1;
  border-radius: 50%;
  background: radial-gradient(circle at 30% 30%, #2c2f3a, #111319 60%);
  border: 8px solid #1e212b;
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.35);
}

.section {
  margin-top: 34px;
}

.section h2 {
  font-size: 16px;
  margin-bottom: 16px;
}

.section-head {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
}

.listing-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 16px;
}

.listing-tab {
  border: 1px solid #e5e7eb;
  background: #ffffff;
  color: #111827;
  border-radius: 999px;
  padding: 6px 12px;
  font-size: 12px;
  cursor: pointer;
}

.listing-tab.active {
  background: #111827;
  color: #ffffff;
  border-color: #111827;
}

.pill {
  background: #0f172a;
  color: #fff;
  border-radius: 999px;
  padding: 4px 10px;
  font-size: 11px;
}

.deal-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}

.deal-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 16px;
  border: 1px solid #ededed;
  box-shadow: 0 14px 30px rgba(17, 24, 39, 0.06);
  display: grid;
  gap: 8px;
  font-size: 12px;
  color: #6b7280;
}

.deal-title {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  align-items: center;
  color: #111827;
  font-size: 13px;
}

.deal-title span {
  background: #111827;
  color: #fff;
  border-radius: 999px;
  padding: 4px 10px;
  font-size: 11px;
}

.deal-note {
  font-size: 11px;
  color: #9ca3af;
}

.brand-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 14px;
}

.brand-chip {
  border: none;
  background: #1a1d24;
  color: #fff;
  padding: 10px 12px;
  border-radius: 10px;
  font-size: 12px;
}

.protection-card {
  background: #12151c;
  color: #fff;
  padding: 26px;
  border-radius: 18px;
  max-width: 640px;
}

.protection-card ul {
  list-style: none;
  padding: 0;
  margin: 14px 0 18px;
  display: grid;
  gap: 8px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.7);
}

.protection-card li::before {
  content: "✓";
  margin-right: 8px;
  color: #7dd3fc;
}

.ghost {
  border: 1px solid rgba(255, 255, 255, 0.3);
  background: transparent;
  color: #fff;
  padding: 8px 14px;
  border-radius: 10px;
  font-size: 12px;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 360px));
  gap: 22px;
  align-items: start;
  justify-items: start;
  justify-content: start;
}

.empty-card {
  background: #ffffff;
  border-radius: 18px;
  padding: 30px 24px;
  border: 1px dashed #d9d9d9;
  text-align: center;
}

.empty-card h3 {
  margin: 0 0 8px;
  font-size: 14px;
  font-weight: 600;
}

.empty-card p {
  font-size: 12px;
  color: #6b7280;
  max-width: 520px;
  margin: 0 auto 10px;
}

.ghost-link {
  border: none;
  background: none;
  color: #111827;
  font-size: 12px;
  text-decoration: underline;
  cursor: pointer;
}

.detail-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 18px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  border: 1px solid #ededed;
}

.search-state {
  font-size: 12px;
  color: #6b7280;
  margin-bottom: 12px;
}

.search-state.error {
  color: #b3312d;
}

.role-note {
  margin: 6px 0 12px;
  font-size: 12px;
  color: #6b7280;
}

.search-breadcrumb {
  display: flex;
  gap: 8px;
  font-size: 12px;
  color: #6b7280;
  margin: 6px 0 12px;
}

.filter-row {
  margin: 0 0 12px;
  display: flex;
  gap: 10px;
  align-items: center;
}

.filter-pill {
  background: #111827;
  color: #ffffff;
  border-radius: 999px;
  padding: 6px 12px;
  font-size: 11px;
  font-weight: 600;
}

.filter-clear {
  border: 1px solid #e5e7eb;
  background: #ffffff;
  color: #111827;
  border-radius: 999px;
  padding: 6px 12px;
  font-size: 11px;
  cursor: pointer;
}

.crumb-link {
  border: none;
  background: none;
  color: #6b7280;
  padding: 0;
  cursor: pointer;
  font-size: 12px;
}

.crumb-link:hover {
  color: #111827;
}

.result-strip {
  margin-top: 14px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.result-chip {
  border: 1px solid #e5e7eb;
  background: #ffffff;
  border-radius: 999px;
  padding: 6px 12px;
  font-size: 11px;
  cursor: pointer;
}

.result-chip.active {
  border-color: #111827;
  background: #111827;
  color: #fff;
}

.detail-images {
  display: grid;
  grid-template-columns: repeat(2, minmax(120px, 1fr));
  gap: 12px;
}

.detail-photo {
  width: 100%;
  aspect-ratio: 1 / 1;
  border-radius: 10px;
  background: #e6e9ee;
  background-size: cover;
  background-position: center;
}

.detail-info {
  display: grid;
  gap: 10px;
  font-size: 13px;
  color: #6b7280;
}

.detail-info .seller-line {
  color: #4b5563;
  font-size: 12px;
}

.detail-info h3 {
  margin: 0;
  font-size: 16px;
  color: #111827;
}

.detail-info strong {
  font-size: 15px;
  color: #111827;
}

.detail-actions {
  display: flex;
  gap: 10px;
}

.action-message {
  margin: 0;
  font-size: 12px;
  color: #1f4f8f;
}

.result-grid {
  margin-top: 18px;
  display: grid;
  gap: 16px;
}

.result-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 14px;
  border: 1px solid #ededed;
  display: grid;
  grid-template-columns: minmax(160px, 200px) 1fr;
  gap: 16px;
}

.result-photo {
  border-radius: 12px;
  height: 120px;
  background: #e6e9ee;
  background-size: cover;
  background-position: center;
}

.result-body {
  display: grid;
  gap: 10px;
  font-size: 12px;
  color: #6b7280;
}

.result-body h4 {
  margin: 0 0 6px;
  font-size: 14px;
  color: #111827;
}

.result-actions {
  display: flex;
  gap: 10px;
}

.search-grid {
  margin-top: 18px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 360px));
  gap: 22px;
  align-items: start;
  justify-items: start;
  justify-content: start;
}

.detail-actions button:disabled {
  opacity: 0.55;
  cursor: not-allowed;
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

.promo-note {
  font-size: 12px;
  color: #111827;
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

.remove-btn {
  border: none;
  background: none;
  color: #b3312d;
  font-size: 11px;
  cursor: pointer;
  text-decoration: underline;
}

.cart-total {
  text-align: right;
  font-size: 12px;
  color: #111827;
}

.cart-empty {
  font-size: 12px;
  color: #6b7280;
}

.cart-note {
  margin: 8px 0 0;
  font-size: 11px;
  color: #6b7280;
}

.form-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 22px;
  border: 1px solid #ededed;
  max-width: 520px;
}

.form-card h3 {
  margin: 0 0 14px;
  font-size: 14px;
  font-weight: 600;
}

.form-grid {
  display: grid;
  gap: 12px;
  font-size: 12px;
  color: #6b7280;
}

.form-grid label {
  display: grid;
  gap: 6px;
}

.form-grid input {
  height: 34px;
  border-radius: 10px;
  border: 1px solid #e0e0e0;
  padding: 0 10px;
  outline: none;
  font-size: 12px;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(2, minmax(120px, 1fr));
  gap: 12px;
}

.upload-box {
  height: 90px;
  border: 1px dashed #d1d5db;
  border-radius: 12px;
  display: grid;
  place-items: center;
  color: #6b7280;
  background: #f8f8f8;
}

.upload-preview {
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #e5e7eb;
}

.upload-preview img {
  width: 100%;
  height: 160px;
  object-fit: cover;
  display: block;
}

@media (max-width: 960px) {
  .topbar {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  .result-card {
    grid-template-columns: 1fr;
  }
  .nav {
    flex-wrap: wrap;
    justify-content: flex-start;
  }
  .auth-links {
    justify-content: flex-start;
  }
}
</style>
