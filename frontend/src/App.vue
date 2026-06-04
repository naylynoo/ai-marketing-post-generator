<template>
  <div class="app-shell">
    <header class="app-header">
      <div class="app-logo">
        <div class="app-logo-circle"></div>
        <div>
          <div class="app-title">AI Marketing Post Generator</div>
          <div class="app-subtitle">Turn product ideas into multi‑channel copy</div>
        </div>
      </div>

      <nav class="app-nav">
        <RouterLink to="/" class="app-nav-link">Home</RouterLink>
        <RouterLink to="/generate" class="app-nav-link">Generate</RouterLink>
        <RouterLink to="/history" class="app-nav-link">History</RouterLink>
        <DarkModeToggle />
      </nav>
    </header>

    <main class="app-main">
      <RouterView />
    </main>

    <ToastContainer />
  </div>
</template>

<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
import DarkModeToggle from "./components/DarkModeToggle.vue";
import ToastContainer from "./components/ToastContainer.vue";
</script>
