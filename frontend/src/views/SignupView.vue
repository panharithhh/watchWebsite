<template>
    <div class="auth">
      <div class="auth-card">
        <h1 class="auth-title">Sign up</h1>
  
        <div class="auth-form">
          <BaseInput v-model="form.username" label="Username" type="text" placeholder="yourname" />
          <BaseInput v-model="form.email" label="Email address" type="email" placeholder="you@example.com" />
          <BaseInput v-model="form.password" label="Password" type="password" />
          <BaseInput v-model="form.confirm_password" label="Re-enter your password" type="password" />
  
          <div class="field">
            <label class="label" for="role">Role</label>
            <select id="role" class="auth-select" v-model="form.role">
              <option value="user">User</option>
              <option value="seller">Seller</option>
            </select>
          </div>
  
          <p v-if="error" class="auth-error">{{ error }}</p>
          <p v-if="info" class="auth-info">{{ info }}</p>
        </div>
  
        <BaseButton @click="signUp" :disabled="loading">
          {{ loading ? "Sending code..." : "SignUp" }}
        </BaseButton>

        
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { reactive, ref } from "vue"
  import { useRouter } from "vue-router"
  import BaseInput from "@/components/BaseInput.vue"
  import BaseButton from "@/components/BaseButton.vue"
  import { api } from "@/lib/api" // change this import path to your api.ts location
  
  const form = reactive({
    username: "",
    email: "",
    password: "",
    confirm_password: "",
    role: "user",
  })
  
  const router = useRouter()
  const loading = ref(false)
  const error = ref("")
  const info = ref("")
  
  const signUp = async () => {
    error.value = ""
    info.value = ""
    loading.value = true
  
    try {
      const res = await api<{ message: string; code?: string }>("/auth/requestSignupCode", {
        method: "POST",
        body: JSON.stringify({ email: form.email }),
      })
      if (res.code) {
        sessionStorage.setItem("signup_code", res.code)
        info.value = `${res.message} Code: ${res.code}`
      }
      sessionStorage.setItem("signup_payload", JSON.stringify(form))
      await router.push("/signup-code")
    } catch (e: any) {
      error.value = e?.message || "Signup failed"
    } finally {
      loading.value = false
    }
  }
  </script>
