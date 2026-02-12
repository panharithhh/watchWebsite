<template>
  <div class="auth">
    <div class="auth-card">
      <h1 class="auth-title">Forget my password</h1>

      <div class="auth-form">
        <BaseInput label="Email address" type="email" placeholder="you@example.com" />
      </div>

      <BaseButton>Send</BaseButton>

      <div class="auth-row">
        <RouterLink class="auth-link" to="/login">Back to login</RouterLink>
        <RouterLink class="auth-link" to="/new-password">I have a token</RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import BaseInput from "@/components/BaseInput.vue"
import BaseButton from "@/components/BaseButton.vue"
</script>
