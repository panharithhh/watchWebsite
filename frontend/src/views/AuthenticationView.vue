<template>
  <div class="auth">
    <div class="auth-grid">
      <div class="auth-card">
        <h1 class="auth-title">Sign up</h1>

        <div class="auth-form">
          <BaseInput label="Username" type="text" placeholder="yourname" />
          <BaseInput label="Email address" type="email" placeholder="you@example.com" />
          <BaseInput label="Password" type="password" />
          <BaseInput label="Re-enter your password" type="password" />
          <div class="field">
            <label class="label" for="auth-role">Role</label>
            <select id="auth-role" class="auth-select">
              <option value="user">User</option>
              <option value="seller">Seller</option>
            </select>
          </div>
        </div>

        <BaseButton>SignUp</BaseButton>
      </div>

      <div class="auth-card">
        <h1 class="auth-title">Log in</h1>

        <div class="auth-form">
          <BaseInput label="Email address" type="email" placeholder="you@example.com" />
          <BaseInput label="Password" type="password" />
        </div>

        <BaseButton>Log in</BaseButton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import BaseInput from "@/components/BaseInput.vue"
import BaseButton from "@/components/BaseButton.vue"
</script>
