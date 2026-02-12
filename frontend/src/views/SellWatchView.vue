<template>
  <div class="home">
    <header class="topbar">
      <div class="topbar-row">
        <div class="brand">TOURBILLON10</div>
        <SearchBar
          v-model="searchQuery"
          placeholder="Search"
          @search="submitSearch"
        />
        <div class="auth-links">
          <span class="user-text">Hi, {{ username }}</span>
          <button class="logout-btn" @click="logout">Logout</button>
        </div>
      </div>
      <nav class="nav">
        <button class="nav-link" @click="router.push('/home')">Home</button>
        <span class="nav-pill">Sell a watch</span>
      </nav>
    </header>

    <section class="section">
      <h2>Sell a watch</h2>
      <div v-if="!isSeller" class="access-note">
        <p>Seller account required to submit listings.</p>
        <div class="access-actions">
          <RouterLink to="/signup">Create account</RouterLink>
          <RouterLink to="/login">Log in</RouterLink>
        </div>
      </div>

      <div class="tab-row">
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'listing' }"
          @click="activeTab = 'listing'"
        >
          Listing
        </button>
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'promotions' }"
          @click="activeTab = 'promotions'"
        >
          Promotions
        </button>
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'inventory' }"
          @click="activeTab = 'inventory'"
        >
          Inventory
        </button>
      </div>

      <div v-if="activeTab === 'listing'" class="form-card">
        <h3>Listing details</h3>
        <div class="form-grid">
          <label>
            Watch name
            <input v-model="sellForm.name" type="text" placeholder="Rolex Datejust" />
          </label>
          <label>
            Brand
            <input v-model="sellForm.brand" type="text" placeholder="Rolex" />
          </label>
          <label>
            Image attachment
            <input
              ref="fileInput"
              type="file"
              accept="image/*"
              @change="onImageChange"
            />
          </label>
          <div v-if="sellForm.imageUrl" class="upload-preview">
            <img :src="sellForm.imageUrl" alt="Watch preview" />
          </div>
          <label>
            Description
            <input v-model="sellForm.description" type="text" placeholder="Full set, verified." />
          </label>
          <label>
            Asking price
            <input v-model="sellForm.price" type="number" placeholder="12500" />
          </label>
          <label>
            Tags
            <input v-model="sellForm.tags" type="text" placeholder="rolex,datejust,classic" />
          </label>
          <button
            class="primary dark"
            type="button"
            :disabled="sellLoading || !isSeller"
            @click="submitListing"
          >
            {{
              sellLoading
                ? "Submitting..."
                : editingId
                  ? "Update listing"
                  : "Submit listing"
            }}
          </button>
          <p v-if="sellMessage" class="action-message">{{ sellMessage }}</p>
        </div>
      </div>

      <div v-if="activeTab === 'promotions'" class="form-card promo-card" ref="promoRef">
        <h3>Promotions</h3>
        <div class="form-grid">
          <div v-if="inventoryLoading" class="action-message">
            Loading inventory for promotions...
          </div>
          <div v-else-if="!inventory.length" class="action-message">
            Add a watch to your inventory first.
          </div>
          <div v-else class="inventory-select">
            <p>Select a watch</p>
            <div class="inventory-options">
              <label
                v-for="item in inventory"
                :key="item.id"
                class="inventory-option"
                :class="{ selected: promoForm.watchId === String(item.id) }"
              >
                <input
                  type="radio"
                  name="promoWatch"
                  :value="String(item.id)"
                  v-model="promoForm.watchId"
                  @change="selectPromoWatch(item.id)"
                />
                <span>{{ item.brand }} {{ item.name }}</span>
                <em>#{{ item.id }}</em>
                <span v-if="promotionFor(item.id)" class="promo-flag">Promo</span>
                <span v-if="promoForm.watchId === String(item.id)" class="selected-flag">
                  ✓ Selected
                </span>
              </label>
            </div>
          </div>
          <label>
            Watch ID
            <input v-model="promoForm.watchId" type="text" placeholder="e.g. 12" />
          </label>
          <label>
            Promotion title
            <input v-model="promoForm.title" type="text" placeholder="Holiday drop" />
          </label>
          <label>
            Description
            <input
              v-model="promoForm.description"
              type="text"
              placeholder="Limited run, verified listings."
            />
          </label>
          <label>
            Discount / Offer
            <input v-model="promoForm.discount" type="text" placeholder="10% off" />
          </label>
          <label>
            Valid until
            <input v-model="promoForm.validUntil" type="text" placeholder="Mar 31, 2026" />
          </label>
          <button
            class="primary dark"
            type="button"
            :disabled="promoLoading || !isSeller"
            @click="submitPromotion"
          >
            {{ promoLoading ? "Posting..." : "Post promotion" }}
          </button>
          <p v-if="promoMessage" class="action-message">{{ promoMessage }}</p>
        </div>
      </div>

      <div v-if="activeTab === 'inventory'" class="form-card promo-card">
        <h3>Your inventory</h3>
        <div v-if="inventoryLoading" class="action-message">Loading inventory...</div>
        <div v-else-if="!inventory.length" class="action-message">
          No listings yet.
        </div>
        <div v-else class="inventory-grid">
          <div v-for="item in inventory" :key="item.id" class="inventory-card">
            <div
              class="inventory-photo"
              :style="{ backgroundImage: itemImage(item) ? `url(${itemImage(item)})` : '' }"
            ></div>
            <div class="inventory-body">
              <strong>{{ item.brand }} {{ item.name }}</strong>
              <span>{{ formatPrice(item.price) }}</span>
              <span v-if="promotionFor(item.id)" class="promo-line">
                Promo: {{ promotionFor(item.id)?.title }}
                <em v-if="promotionFor(item.id)?.discount">
                  ({{ promotionFor(item.id)?.discount }})
                </em>
              </span>
            </div>
            <div class="inventory-actions">
              <button class="ghost small" type="button" @click="startEdit(item)">
                Edit
              </button>
              <button class="ghost small danger" type="button" @click="deleteListing(item.id)">
                Delete
              </button>
              <button class="ghost small" type="button" @click="openPromotion(item.id)">
                Add promo
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { nextTick, onMounted, ref } from "vue"
import { useRouter } from "vue-router"
import { api } from "@/lib/api"
import SearchBar from "@/components/SearchBar.vue"

const router = useRouter()
const searchQuery = ref("")
const username = ref(
  localStorage.getItem("username") ||
    sessionStorage.getItem("username") ||
    "Seller"
)

const sellForm = ref({
  name: "",
  brand: "",
  price: "",
  description: "",
  tags: "",
  imageUrl: "",
})
const fileInput = ref<HTMLInputElement | null>(null)
const sellLoading = ref(false)
const sellMessage = ref("")
const promoForm = ref({
  watchId: "",
  title: "",
  description: "",
  discount: "",
  validUntil: "",
})
const promoLoading = ref(false)
const promoMessage = ref("")
const inventory = ref<
  {
    id: number
    name: string
    brand: string
    price: number
    status: string
    description?: string
    tags?: string
    image_url?: string
    imageUrl?: string
  }[]
>([])
const inventoryLoading = ref(false)
const promotions = ref<
  {
    id: number
    watch_id?: number
    watchId?: number
    title: string
    description: string
    discount?: string
    valid_until?: string
  }[]
>([])
const promoRef = ref<HTMLElement | null>(null)
const isSeller = ref(
  (localStorage.getItem("role") || sessionStorage.getItem("role")) === "seller"
)
const editingId = ref<number | null>(null)
const activeTab = ref<"listing" | "promotions" | "inventory">("listing")

const submitListing = async () => {
  sellMessage.value = ""
  if (!sellForm.value.name || !sellForm.value.brand || !sellForm.value.price) {
    sellMessage.value = "Name, brand, and price are required."
    return
  }
  if (!isSeller.value) {
    sellMessage.value = "Seller account required."
    return
  }
  sellLoading.value = true
  try {
    if (editingId.value) {
      await api(`http://localhost:8000/watches/${editingId.value}`, {
        method: "PUT",
        body: JSON.stringify({
          name: sellForm.value.name,
          brand: sellForm.value.brand,
          price: Number(sellForm.value.price),
          description: sellForm.value.description || "Listing updated.",
          tags: sellForm.value.tags || "",
          imageUrl: sellForm.value.imageUrl || "",
        }),
      })
      sellMessage.value = "Listing updated."
      activeTab.value = "inventory"
    } else {
      const created = await api<{ id: number }>("http://localhost:8000/watches/getWatch", {
        method: "POST",
        body: JSON.stringify({
          name: sellForm.value.name,
          brand: sellForm.value.brand,
          price: Number(sellForm.value.price),
          description: sellForm.value.description || "Listing submitted.",
          tags: sellForm.value.tags || "",
          imageUrl: sellForm.value.imageUrl || "",
        }),
      })
      sellMessage.value = "Listing submitted for approval."
      activeTab.value = "inventory"
      if (!promoForm.value.watchId && created?.id) {
        promoForm.value.watchId = String(created.id)
      }
    }
    await loadInventory()
    sellForm.value = {
      name: "",
      brand: "",
      price: "",
      description: "",
      tags: "",
      imageUrl: "",
    }
    editingId.value = null
    if (fileInput.value) {
      fileInput.value.value = ""
    }
  } catch (e: any) {
    sellMessage.value = e?.message || "Failed to submit listing"
  } finally {
    sellLoading.value = false
  }
}

const onImageChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) {
    sellForm.value.imageUrl = ""
    return
  }
  const reader = new FileReader()
  reader.onload = () => {
    sellForm.value.imageUrl = String(reader.result || "")
  }
  reader.readAsDataURL(file)
}

const submitPromotion = async () => {
  promoMessage.value = ""
  if (!promoForm.value.title || !promoForm.value.description) {
    promoMessage.value = "Title and description are required."
    return
  }
  if (!isSeller.value) {
    promoMessage.value = "Seller account required."
    return
  }
  promoLoading.value = true
  try {
    const watchId = Number(promoForm.value.watchId)
    if (!Number.isFinite(watchId) || watchId <= 0) {
      promoMessage.value = "Valid watch ID is required."
      return
    }
    await api("http://localhost:8000/promotion", {
      method: "POST",
      body: JSON.stringify({
        watchId,
        title: promoForm.value.title,
        description: promoForm.value.description,
        discount: promoForm.value.discount || undefined,
        valid_until: promoForm.value.validUntil || undefined,
      }),
    })
    promoMessage.value = "Promotion posted."
    await loadPromotions()
    promoForm.value = {
      watchId: "",
      title: "",
      description: "",
      discount: "",
      validUntil: "",
    }
  } catch (e: any) {
    promoMessage.value = e?.message || "Failed to post promotion"
  } finally {
    promoLoading.value = false
  }
}

const loadInventory = async () => {
  if (!isSeller.value) return
  inventoryLoading.value = true
  try {
    const res = await api<typeof inventory.value>("http://localhost:8000/watches/mine")
    inventory.value = res
  } catch {
    inventory.value = []
  } finally {
    inventoryLoading.value = false
  }
}

const loadPromotions = async () => {
  if (!isSeller.value) return
  try {
    const res = await api<{ promotions: typeof promotions.value }>(
      "http://localhost:8000/promotion"
    )
    promotions.value = res.promotions || []
  } catch {
    promotions.value = []
  }
}

const promotionFor = (watchId: number) => {
  return promotions.value.find((promo) => {
    const id = promo.watch_id ?? promo.watchId
    return id === watchId
  })
}

const startEdit = async (item: (typeof inventory.value)[number]) => {
  editingId.value = item.id
  sellForm.value = {
    name: item.name,
    brand: item.brand,
    price: String(item.price),
    description: item.description || "",
    tags: item.tags || "",
    imageUrl: (item.image_url || item.imageUrl || "") as string,
  }
  sellMessage.value = "Editing listing."
  activeTab.value = "listing"
  await nextTick()
}

const deleteListing = async (id: number) => {
  try {
    await api(`http://localhost:8000/watches/${id}`, { method: "POST" })
    inventory.value = inventory.value.filter((item) => item.id !== id)
    if (editingId.value === id) {
      editingId.value = null
    }
  } catch (e: any) {
    sellMessage.value = e?.message || "Failed to delete listing"
  }
}

const editPromotion = async (watchId: number) => {
  const promo = promotionFor(watchId)
  promoForm.value.watchId = String(watchId)
  promoForm.value.title = promo?.title || ""
  promoForm.value.description = promo?.description || ""
  promoForm.value.discount = promo?.discount || ""
  promoForm.value.validUntil = promo?.valid_until || ""
  promoMessage.value = promo ? "Editing promotion." : "Creating promotion."
  activeTab.value = "promotions"
  await nextTick()
  promoRef.value?.scrollIntoView({ behavior: "smooth", block: "start" })
}

const openPromotion = (watchId: number) => {
  editPromotion(watchId)
}

const selectPromoWatch = (watchId: number) => {
  const promo = promotionFor(watchId)
  promoForm.value.watchId = String(watchId)
  promoForm.value.title = promo?.title || ""
  promoForm.value.description = promo?.description || ""
  promoForm.value.discount = promo?.discount || ""
  promoForm.value.validUntil = promo?.valid_until || ""
}

const formatPrice = (price: number) => {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(price)
}

const itemImage = (item: (typeof inventory.value)[number]) => {
  return item.image_url || item.imageUrl || ""
}
const logout = () => {
  localStorage.removeItem("auth_token")
  localStorage.removeItem("username")
  localStorage.removeItem("role")
  sessionStorage.removeItem("auth_token")
  sessionStorage.removeItem("username")
  sessionStorage.removeItem("role")
  router.push("/login")
}

const submitSearch = () => {
  const value = searchQuery.value.trim()
  if (!value) {
    router.push("/home")
    return
  }
  router.push({ path: "/home", query: { q: value } })
}

onMounted(() => {
  loadInventory()
  loadPromotions()
})
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

.access-note {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 14px;
  margin-bottom: 16px;
  font-size: 12px;
  color: #6b7280;
}

.access-actions {
  display: flex;
  gap: 12px;
  margin-top: 8px;
}

.access-actions a {
  color: #111827;
  text-decoration: underline;
  font-size: 12px;
}

.form-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 22px;
  border: 1px solid #ededed;
  max-width: 620px;
}

.promo-card {
  margin-top: 18px;
}

.tab-row {
  display: flex;
  gap: 10px;
  margin: 16px 0;
}

.tab-btn {
  border: 1px solid #e5e7eb;
  background: #ffffff;
  color: #374151;
  padding: 6px 12px;
  border-radius: 10px;
  font-size: 11px;
  cursor: pointer;
}

.tab-btn.active {
  background: #111827;
  color: #ffffff;
  border-color: #111827;
}

.inventory-select {
  display: grid;
  gap: 10px;
}

.inventory-select p {
  margin: 0;
  font-size: 12px;
  color: #6b7280;
}

.inventory-options {
  display: grid;
  gap: 8px;
}

.inventory-option {
  display: grid;
  grid-template-columns: auto 1fr auto auto;
  gap: 8px;
  align-items: center;
  padding: 8px 10px;
  border-radius: 10px;
  border: 1px solid #ededed;
  font-size: 12px;
  color: #111827;
}

.inventory-option.selected {
  border-color: #111827;
  background: #f9fafb;
}

.inventory-option em {
  font-style: normal;
  color: #6b7280;
  font-size: 11px;
}

.promo-flag {
  background: #111827;
  color: #fff;
  border-radius: 999px;
  padding: 3px 8px;
  font-size: 10px;
}

.selected-flag {
  background: #3b82f6;
  color: #fff;
  border-radius: 999px;
  padding: 3px 8px;
  font-size: 10px;
}

.inventory-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 24px;
}

.inventory-card {
  border: 1px solid #ededed;
  border-radius: 12px;
  padding: 12px;
  display: grid;
  gap: 10px;
}

.inventory-photo {
  width: 100%;
  aspect-ratio: 1 / 1;
  border-radius: 10px;
  background: #eef0f4;
  background-size: cover;
  background-position: center;
}

.inventory-body {
  display: grid;
  gap: 3px;
  font-size: 10px;
  color: #6b7280;
}

.inventory-body strong {
  color: #111827;
  font-size: 11px;
}

.inventory-actions {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.ghost.small {
  border: 1px solid #d1d5db;
  background: #ffffff;
  color: #111827;
  padding: 4px 8px;
  border-radius: 8px;
  font-size: 10px;
  cursor: pointer;
}

.ghost.small.danger {
  border-color: #ef4444;
  color: #b91c1c;
}

.promo-line {
  display: block;
  margin-top: 6px;
  font-size: 11px;
  color: #111827;
}

.promo-line em {
  font-style: normal;
  color: #6b7280;
}

.status {
  background: #111827;
  color: #fff;
  border-radius: 999px;
  padding: 4px 10px;
  font-size: 10px;
  text-transform: capitalize;
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

.form-grid input[type="file"] {
  padding: 4px 10px;
  background: #f9fafb;
  border: 1px dashed #d1d5db;
  color: #6b7280;
}

.form-grid input[type="file"]::file-selector-button {
  border: none;
  background: #111827;
  color: #fff;
  padding: 6px 10px;
  border-radius: 8px;
  margin-right: 10px;
  font-size: 11px;
  cursor: pointer;
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

.action-message {
  margin: 0;
  font-size: 12px;
  color: #1f4f8f;
}

.upload-preview {
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #e5e7eb;
}

.upload-preview img {
  width: 100%;
  height: 180px;
  object-fit: cover;
  display: block;
}
</style>
