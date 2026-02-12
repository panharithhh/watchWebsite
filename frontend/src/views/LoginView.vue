<template>
  <div class="auth">
    <div class="auth-card">
      <h1 class="auth-title">Log in</h1>

      <div class="auth-form">
        <BaseInput v-model="email" label="Email address" type="email" placeholder="you@example.com" />
        <BaseInput v-model="password" label="Password" type="password" />
      </div>

      <div class="auth-row">
        <label class="auth-check">
          <input type="checkbox" v-model="remember" />
          Remember me
        </label>
      </div>

      <BaseButton @click="onLogin" :disabled="loading">
        {{ loading ? "Logging in..." : "Log in" }}
      </BaseButton>

      <p v-if="error" class="auth-error">{{ error }}</p>
      <div class="auth-row">
        <RouterLink class="auth-link" to="/signup">Sign up</RouterLink>
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

type LoginResponse = {
  access_token: string
  token_type: string
  username: string
  role: string
  seller_verified: boolean
}

const email = ref("")
const password = ref("")
const remember = ref(true)
const loading = ref(false)
const error = ref("")
const router = useRouter()

const onLogin = async () => {
  error.value = ""
  loading.value = true
  try {
    const res = await api<LoginResponse>("http://localhost:8000/auth/login", {
      method: "POST",
      body: JSON.stringify({ email: email.value, password: password.value }),
    })
    if (remember.value) {
      localStorage.setItem("auth_token", res.access_token)
      localStorage.setItem("username", res.username)
      localStorage.setItem("role", res.role)
    } else {
      sessionStorage.setItem("auth_token", res.access_token)
      sessionStorage.setItem("username", res.username)
      sessionStorage.setItem("role", res.role)
    }
    if (res.role === "admin") {
      await router.push("/admin")
    } else {
      await router.push("/home")
    }
  } catch (e: any) {
    error.value = e?.message || "Login failed"
  } finally {
    loading.value = false
  }
}
</script>
