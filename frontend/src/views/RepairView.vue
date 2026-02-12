<template>
  <div class="repair-page">
    <header class="repair-topbar">
      <div class="brand">TOURBILLON10</div>
      <div class="repair-links">
        <RouterLink to="/home">Back to home</RouterLink>
      </div>
    </header>

    <main class="repair-main">
      <div class="repair-card">
        <div v-if="loading" class="repair-state">Loading service...</div>
        <div v-else-if="error" class="repair-state error">{{ error }}</div>
        <div v-else-if="service" class="repair-body">
          <h1>{{ service.title }}</h1>
          <p class="repair-summary">{{ service.summary }}</p>
          <ul>
            <li v-for="item in service.bullets" :key="item">{{ item }}</li>
          </ul>
          <div class="repair-meta">
            <span>{{ service.turnaround }}</span>
            <span class="repair-pill">{{ service.price }}</span>
          </div>
          <button class="repair-cta">Request repair</button>
          <p class="repair-note">Demo only — no service request is sent.</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue"
import { api } from "@/lib/api"

type ServiceInfo = {
  key: string
  title: string
  summary: string
  bullets: string[]
  turnaround: string
  price: string
}

const service = ref<ServiceInfo | null>(null)
const loading = ref(false)
const error = ref("")

const loadService = async () => {
  loading.value = true
  error.value = ""
  try {
    service.value = await api<ServiceInfo>(
      "http://localhost:8000/services?type=repair"
    )
  } catch (e: any) {
    error.value = e?.message || "Failed to load repair service"
  } finally {
    loading.value = false
  }
}

onMounted(loadService)
</script>

<style scoped>
.repair-page {
  min-height: 100vh;
  background: #f3f2ef;
  padding: 24px clamp(16px, 4vw, 48px) 60px;
  font-family: "Manrope", "Segoe UI", sans-serif;
  color: #111827;
}

.repair-topbar {
  display: flex;
  justify-content: space-between;
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

.repair-links a {
  color: #111827;
  text-decoration: none;
  font-size: 13px;
}

.repair-main {
  margin-top: 28px;
  display: grid;
  place-items: center;
}

.repair-card {
  width: min(820px, 94vw);
  background: #111319;
  color: #ffffff;
  border-radius: 22px;
  padding: 32px clamp(22px, 4vw, 40px);
  border: 1px solid #1f2430;
  box-shadow: 0 18px 32px rgba(5, 6, 10, 0.35);
}

.repair-body h1 {
  margin: 0 0 12px;
  font-size: clamp(24px, 3.2vw, 32px);
}

.repair-summary {
  margin: 0 0 18px;
  color: rgba(255, 255, 255, 0.75);
  font-size: 14px;
}

.repair-card ul {
  margin: 0 0 18px;
  padding-left: 18px;
  display: grid;
  gap: 8px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.75);
}

.repair-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.75);
  margin-bottom: 18px;
}

.repair-pill {
  background: #ffffff;
  color: #111319;
  border-radius: 999px;
  padding: 6px 12px;
  font-size: 11px;
  font-weight: 600;
}

.repair-cta {
  border: none;
  background: #ffffff;
  color: #111319;
  padding: 10px 18px;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
}

.repair-note {
  margin: 12px 0 0;
  font-size: 11px;
  color: rgba(255, 255, 255, 0.6);
}

.repair-state {
  font-size: 13px;
}

.repair-state.error {
  color: #fca5a5;
}
</style>
