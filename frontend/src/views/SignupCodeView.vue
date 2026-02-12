<template>
  <div class="auth">
    <div class="auth-card">
      <h1 class="auth-title">Verification Code</h1>

      <div class="auth-form">
        <BaseInput v-model="code" label="Signup code" placeholder="Enter the 6-digit code" />
        <p v-if="error" class="auth-error">{{ error }}</p>
        <div v-if="isSeller" class="seller-docs">
          <p class="auth-info">Required documents for seller verification:</p>
          <ul>
            <li>Government ID (front + back)</li>
            <li>Business registration (if applicable)</li>
            <li>Proof of inventory ownership</li>
          </ul>
          <label class="seller-upload">
            Upload documents (optional)
            <input type="file" multiple />
          </label>
          <a class="seller-mail" :href="mailtoLink">Email documents to us</a>
        </div>
      </div>

      <BaseButton @click="verifyCode" :disabled="loading">
        {{ loading ? "Verifying..." : "Verify" }}
      </BaseButton>

      <div class="auth-row">
        <RouterLink class="auth-link" to="/signup">Back to sign up</RouterLink>
        <RouterLink class="auth-link" to="/login">Log in</RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue"
import { useRouter } from "vue-router"
import BaseInput from "@/components/BaseInput.vue"
import BaseButton from "@/components/BaseButton.vue"
import { api } from "@/lib/api"

const code = ref("")
const error = ref("")
const loading = ref(false)
const router = useRouter()
const supportEmail = "chatgptlolol12@gmail.com"
const mailtoLink = `mailto:${supportEmail}?subject=Seller%20Verification%20Documents`
const isSeller = (() => {
  const raw = sessionStorage.getItem("signup_payload")
  if (!raw) return false
  try {
    const payload = JSON.parse(raw)
    return payload?.role === "seller"
  } catch {
    return false
  }
})()
const saved = sessionStorage.getItem("signup_code")
if (saved) {
  code.value = saved
}

const verifyCode = async () => {
  error.value = ""
  loading.value = true

  try {
    const raw = sessionStorage.getItem("signup_payload")
    if (!raw) {
      throw new Error("No signup info found. Go back to sign up.")
    }
    const payload = JSON.parse(raw)
    await api("http://localhost:8000/auth/signUp", {
      method: "POST",
      body: JSON.stringify({ ...payload, signup_code: code.value }),
    })
    sessionStorage.removeItem("signup_payload")
    sessionStorage.removeItem("signup_code")
    await router.push("/login")
  } catch (e: any) {
    error.value = e?.message || "Verification failed"
  } finally {
    loading.value = false
  }
}
</script>
