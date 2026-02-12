<template>
  <div class="admin-page">
    <header class="admin-topbar">
      <div class="brand">TOURBILLON10</div>
      <div class="admin-search">
        <SearchBar
          v-model="watchQuery"
          placeholder="Search inventory"
          variant="admin"
          @search="applyWatchSearch"
        />
      </div>
      <div class="admin-user">
        Hi, Admin <span class="admin-link">Logout</span>
      </div>
    </header>

    <main class="admin-main">
      <section class="admin-panel">
        <div class="panel-head">
          <div>
            <div class="panel-kicker">Admin Dashboard</div>
            <h1 class="panel-title">Pending seller approvals</h1>
            <p class="panel-sub">
              Review submitted documents and approve sellers when requirements are met.
            </p>
          </div>
          <button class="panel-refresh" type="button" @click="loadPending" :disabled="loading">
            {{ loading ? "Refreshing..." : "Refresh" }}
          </button>
        </div>

        <p v-if="error" class="panel-error">{{ error }}</p>

        <div v-if="pending.length === 0 && !loading" class="panel-empty">
          No pending sellers.
        </div>

        <div v-for="user in pending" :key="user.id" class="panel-card">
          <div class="panel-card-head">
            <div>
              <div class="panel-name">{{ user.username }}</div>
              <div class="panel-email">{{ user.email }}</div>
            </div>
            <span class="panel-status">Pending verification</span>
          </div>

          <div class="panel-docs">
            <div class="panel-docs-title">Required documents</div>
            <div class="panel-docs-grid">
              <div class="panel-doc">
                <div>
                  <div class="doc-title">Government ID</div>
                  <div class="doc-meta">ID_card.pdf</div>
                </div>
                <span class="doc-chip ok">Received</span>
              </div>
              <div class="panel-doc">
                <div>
                  <div class="doc-title">Business registration</div>
                  <div class="doc-meta">business_license.pdf</div>
                </div>
                <span class="doc-chip pending">Pending</span>
              </div>
              <div class="panel-doc">
                <div>
                  <div class="doc-title">Proof of inventory</div>
                  <div class="doc-meta">inventory_photos.zip</div>
                </div>
                <span class="doc-chip ok">Received</span>
              </div>
            </div>
          </div>

          <div class="panel-actions">
            <BaseButton @click="approve(user.id)">Approve Seller</BaseButton>
          </div>
        </div>
      </section>

      <section class="admin-panel">
        <div class="panel-head">
          <div>
            <div class="panel-kicker">Inventory</div>
            <h1 class="panel-title">Watch inventory</h1>
            <p class="panel-sub">All listings visible to buyers.</p>
          </div>
          <button
            class="panel-refresh"
            type="button"
            @click="loadWatches"
            :disabled="watchLoading"
          >
            {{ watchLoading ? "Refreshing..." : "Refresh" }}
          </button>
        </div>

        <p v-if="watchError" class="panel-error">{{ watchError }}</p>
        <div v-if="watchLoading" class="panel-empty">Loading inventory...</div>
        <div v-else-if="!filteredWatches.length" class="panel-empty">
          No listings found.
        </div>
        <div v-else class="watch-grid">
          <div v-for="watch in filteredWatches" :key="watch.id" class="watch-card">
            <div
              class="watch-photo"
              :style="{ backgroundImage: `url(${watch.image_url || watch.imageUrl || ''})` }"
            ></div>
            <div class="watch-meta">
              <strong>{{ watch.brand }} {{ watch.name }}</strong>
              <span>{{ watch.description }}</span>
              <span class="seller-line">Seller: {{ sellerLabel(watch) }}</span>
              <span class="price">{{ formatPrice(watch.price) }}</span>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue"
import BaseButton from "@/components/BaseButton.vue"
import { api } from "@/lib/api"
import SearchBar from "@/components/SearchBar.vue"

type AdminUser = {
  id: number
  username: string
  email: string
  role: string
  seller_verified: boolean
}

type WatchItem = {
  id: number
  name: string
  brand: string
  price: number
  description: string
  image_url?: string
  imageUrl?: string
  seller_name?: string
  sellerName?: string
}

const pending = ref<AdminUser[]>([])
const loading = ref(false)
const error = ref("")
const watches = ref<WatchItem[]>([])
const watchLoading = ref(false)
const watchError = ref("")
const watchQuery = ref("")

const loadPending = async () => {
  error.value = ""
  loading.value = true
  try {
    pending.value = await api<AdminUser[]>("http://localhost:8000/admin/pending-sellers")
  } catch (e: any) {
    error.value = e?.message || "Failed to load pending sellers"
  } finally {
    loading.value = false
  }
}

const approve = async (userId: number) => {
  error.value = ""
  try {
    await api(`http://localhost:8000/admin/approve-seller/${userId}`, { method: "POST" })
    pending.value = pending.value.filter((u) => u.id !== userId)
  } catch (e: any) {
    error.value = e?.message || "Approval failed"
  }
}

const loadWatches = async () => {
  watchError.value = ""
  watchLoading.value = true
  try {
    const res = await api<{ results: WatchItem[] }>("http://localhost:8000/search")
    watches.value = res.results
  } catch (e: any) {
    watchError.value = e?.message || "Failed to load inventory"
  } finally {
    watchLoading.value = false
  }
}

const formatPrice = (price: number) => {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(price)
}

const sellerLabel = (watch: WatchItem) => {
  return watch.seller_name || watch.sellerName || "Unknown seller"
}

const applyWatchSearch = () => {
  watchQuery.value = watchQuery.value.trim()
}

const filteredWatches = computed(() => {
  const term = watchQuery.value.trim().toLowerCase()
  if (!term) return watches.value
  return watches.value.filter((watch) => {
    const seller = sellerLabel(watch)
    return `${watch.brand} ${watch.name} ${watch.description} ${seller}`
      .toLowerCase()
      .includes(term)
  })
})

onMounted(() => {
  loadPending()
  loadWatches()
})
</script>

<style scoped>
.admin-page {
  min-height: 100vh;
  background: #f3f2ef;
  padding: 24px clamp(16px, 4vw, 48px) 60px;
  color: #111827;
  font-family: "Manrope", "Segoe UI", sans-serif;
}

.admin-topbar {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 20px;
  align-items: center;
  background: #ffffff;
  border: 1px solid #e6e5e2;
  border-radius: 18px;
  padding: 16px 20px;
  box-shadow: 0 14px 30px rgba(17, 24, 39, 0.08);
}

.brand {
  font-size: 16px;
  letter-spacing: 0.18em;
  font-weight: 600;
}

.admin-search {
  display: flex;
  align-items: center;
  width: 100%;
}

.admin-search :deep(.search-bar) {
  width: 100%;
}

.admin-user {
  font-size: 14px;
  color: #111827;
  display: flex;
  gap: 8px;
  align-items: center;
}

.admin-link {
  color: #111827;
  text-decoration: underline;
  font-weight: 600;
  cursor: pointer;
}

.admin-main {
  margin-top: 28px;
}

.admin-panel {
  background: #ffffff;
  border-radius: 22px;
  border: 1px solid #e6e5e2;
  padding: 28px clamp(20px, 3vw, 36px);
  box-shadow: 0 18px 36px rgba(17, 24, 39, 0.08);
}

.panel-head {
  display: flex;
  justify-content: space-between;
  gap: 18px;
  align-items: center;
  margin-bottom: 18px;
}

.panel-kicker {
  text-transform: uppercase;
  letter-spacing: 0.24em;
  font-size: 11px;
  color: #9aa0aa;
  margin-bottom: 6px;
}

.panel-title {
  margin: 0;
  font-size: clamp(22px, 3vw, 30px);
  font-weight: 700;
}

.panel-sub {
  margin: 6px 0 0;
  color: #6b7280;
  font-size: 14px;
  max-width: 520px;
}

.panel-refresh {
  border: 1px solid #d1d5db;
  background: #ffffff;
  border-radius: 10px;
  padding: 8px 14px;
  cursor: pointer;
  font-size: 12px;
}

.panel-error {
  margin: 10px 0 0;
  color: #b3312d;
  font-size: 13px;
}

.panel-empty {
  margin-top: 18px;
  color: #1f4f8f;
  font-size: 13px;
}

.panel-card {
  border: 1px solid #ededed;
  border-radius: 18px;
  padding: 18px;
  margin-top: 18px;
  background: #ffffff;
}

.panel-card-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}

.panel-name {
  font-weight: 600;
  font-size: 15px;
}

.panel-email {
  font-size: 12px;
  color: #6b7280;
}

.panel-status {
  background: #111827;
  color: #fff;
  border-radius: 999px;
  font-size: 10px;
  padding: 5px 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.panel-docs {
  background: #fafafa;
  border: 1px dashed #e2e2e2;
  border-radius: 14px;
  padding: 14px;
}

.panel-docs-title {
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 10px;
  color: #374151;
}

.panel-docs-grid {
  display: grid;
  gap: 10px;
}

.panel-doc {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #ffffff;
  border: 1px solid #ededed;
  border-radius: 12px;
  padding: 10px 12px;
}

.doc-title {
  font-size: 12px;
  font-weight: 600;
}

.doc-meta {
  font-size: 11px;
  color: #6b7280;
}

.doc-chip {
  font-size: 10px;
  padding: 4px 8px;
  border-radius: 999px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.doc-chip.ok {
  background: #e8f4ec;
  color: #1b6b3a;
}

.doc-chip.pending {
  background: #fef3c7;
  color: #92400e;
}

.panel-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 12px;
}

.watch-grid {
  margin-top: 16px;
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
}

.watch-card {
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 14px;
  display: grid;
  gap: 10px;
}

.watch-photo {
  width: 100%;
  aspect-ratio: 4 / 3;
  border-radius: 12px;
  background: #e6e9ee;
  background-size: cover;
  background-position: center;
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

.watch-meta .price {
  color: #111827;
  font-weight: 600;
}

.seller-line {
  color: #4b5563;
  font-size: 11px;
}

@media (max-width: 720px) {
  .admin-topbar {
    grid-template-columns: 1fr;
  }

  .panel-head {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
