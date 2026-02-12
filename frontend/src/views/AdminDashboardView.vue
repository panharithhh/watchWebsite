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
            <div class="panel-docs-title">Attachments</div>
            <div v-if="user.documents?.length" class="panel-docs-media">
              <div
                v-for="(doc, index) in user.documents"
                :key="`${user.id}-${index}`"
                class="panel-doc-preview"
              >
                <img v-if="isImage(doc)" :src="doc" alt="Seller attachment" />
                <a v-else :href="doc" target="_blank" rel="noopener">View attachment</a>
              </div>
            </div>
            <div v-else class="panel-docs-empty">No attachments uploaded.</div>
          </div>

          <div class="panel-actions">
            <BaseButton class="approve-btn" @click="approve(user.id)">
              Approve Seller
            </BaseButton>
          </div>
        </div>
      </section>

      <section class="admin-panel">
        <div class="panel-head">
          <div>
            <div class="panel-kicker">Seller Documents</div>
            <h1 class="panel-title">Uploaded proof</h1>
            <p class="panel-sub">All seller attachments submitted at signup.</p>
          </div>
          <button class="panel-refresh" type="button" @click="loadSellerDocs" :disabled="docsLoading">
            {{ docsLoading ? "Refreshing..." : "Refresh" }}
          </button>
        </div>

        <p v-if="docsError" class="panel-error">{{ docsError }}</p>
        <div v-if="docsLoading" class="panel-empty">Loading documents...</div>
        <div v-else-if="!sellerDocs.length" class="panel-empty">No seller documents yet.</div>
        <div v-else class="docs-grid">
          <div v-for="seller in sellerDocs" :key="seller.userId" class="docs-card">
            <div class="docs-card-head">
              <div class="panel-name">{{ seller.username }}</div>
              <div class="panel-email">{{ seller.email }}</div>
            </div>
            <div class="docs-card-media">
              <div
                v-for="(doc, index) in seller.documents"
                :key="`${seller.userId}-${index}`"
                class="panel-doc-preview"
              >
                <img v-if="isImage(doc)" :src="doc" alt="Seller attachment" />
                <a v-else :href="doc" target="_blank" rel="noopener">View attachment</a>
              </div>
            </div>
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
          <WatchCard
            v-for="watch in filteredWatches"
            :key="watch.id"
            :title="`${watch.brand} ${watch.name}`"
            :description="watch.description"
            :seller="sellerLabel(watch)"
            :price="formatPrice(watch.price)"
            :image="watch.image_url || watch.imageUrl || ''"
          >
            <template #actions>
              <button
                class="ghost danger"
                type="button"
                :disabled="deletingIds.has(watch.id)"
                @click.stop="deleteWatch(watch.id)"
              >
                {{ deletingIds.has(watch.id) ? "Deleting..." : "Delete" }}
              </button>
            </template>
          </WatchCard>
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
import WatchCard from "@/components/WatchCard.vue"

type AdminUser = {
  id: number
  username: string
  email: string
  role: string
  seller_verified: boolean
  documents?: string[]
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

type SellerDocs = {
  userId: number
  username: string
  email: string
  documents: string[]
}

const pending = ref<AdminUser[]>([])
const loading = ref(false)
const error = ref("")
const watches = ref<WatchItem[]>([])
const watchLoading = ref(false)
const watchError = ref("")
const watchQuery = ref("")
const deletingIds = ref<Set<number>>(new Set())
const sellerDocs = ref<SellerDocs[]>([])
const docsLoading = ref(false)
const docsError = ref("")

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

const loadSellerDocs = async () => {
  docsError.value = ""
  docsLoading.value = true
  try {
    sellerDocs.value = await api<SellerDocs[]>("http://localhost:8000/admin/seller-documents")
  } catch (e: any) {
    docsError.value = e?.message || "Failed to load seller documents"
  } finally {
    docsLoading.value = false
  }
}

const deleteWatch = async (watchId: number) => {
  if (!confirm("Delete this watch listing?")) return
  const next = new Set(deletingIds.value)
  next.add(watchId)
  deletingIds.value = next
  watchError.value = ""
  try {
    await api(`http://localhost:8000/watches/${watchId}`, { method: "POST" })
    watches.value = watches.value.filter((watch) => watch.id !== watchId)
  } catch (e: any) {
    watchError.value = e?.message || "Failed to delete watch"
  } finally {
    const updated = new Set(deletingIds.value)
    updated.delete(watchId)
    deletingIds.value = updated
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

const isImage = (doc: string) => doc.startsWith("data:image")

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
  loadSellerDocs()
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
  color: #111827;
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

.panel-docs-media {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.panel-doc-preview {
  width: 120px;
  height: 120px;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  background: #ffffff;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.panel-doc-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.panel-doc-preview a {
  font-size: 11px;
  color: #111827;
  text-decoration: underline;
}

.panel-docs-empty {
  font-size: 12px;
  color: #6b7280;
}

.docs-grid {
  display: grid;
  gap: 16px;
}

.docs-card {
  background: #ffffff;
  border: 1px solid #ededed;
  border-radius: 16px;
  padding: 16px;
  display: grid;
  gap: 12px;
}

.docs-card-media {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.panel-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 12px;
}

.approve-btn {
  background: #111827;
  color: #ffffff;
  border: none;
  padding: 10px 18px;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
}

.approve-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.ghost.danger {
  border: 1px solid #ef4444;
  color: #ef4444;
  background: #fff;
  padding: 8px 14px;
  border-radius: 10px;
  font-size: 12px;
  cursor: pointer;
}

.ghost.danger:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.watch-grid {
  margin-top: 18px;
  display: grid;
  gap: 22px;
  grid-template-columns: repeat(auto-fill, minmax(240px, 360px));
  align-items: start;
  justify-items: start;
  justify-content: start;
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
