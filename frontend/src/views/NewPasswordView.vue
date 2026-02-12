<template>
  <div class="auth">
    <div class="auth-card">
      <h1 class="auth-title">New Password</h1>

      <div class="auth-form">
        <BaseInput label="Reset token" placeholder="Paste token here" />
        <BaseInput label="New password" type="password" />
        <BaseInput label="Re-enter new password" type="password" />
      </div>

      <BaseButton>Log in</BaseButton>

      <div class="auth-row">
        <RouterLink class="auth-link" to="/login">Back to login</RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import BaseInput from "@/components/BaseInput.vue"
import BaseButton from "@/components/BaseButton.vue"
</script>
