<template>
  <div class="stack">
    <div class="card stack">
      <div class="card-header">
        <div>
          <div class="card-title">Launch-ready marketing copy in one place</div>
          <p class="card-description">
            Describe your product once and instantly generate platform‑aware captions, short ads,
            hashtags, email subject lines, and calls to action.
          </p>
        </div>
      </div>

      <div class="stack">
        <div class="stack-row">
          <span class="badge">Facebook</span>
          <span class="badge">Instagram</span>
          <span class="badge">TikTok</span>
          <span class="badge">Email</span>
        </div>
        <p class="card-description">
          Perfect for solo founders, small marketing teams, and creators who want to keep a
          consistent voice across channels.
        </p>
      </div>

      <div class="stack-row" style="margin-top: 1rem">
        <RouterLink to="/generate" class="btn btn-primary">
          Start generating
        </RouterLink>
        <RouterLink to="/history" class="btn btn-outline">
          View past ideas
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from "vue-router";
</script>

<style scoped>
.badge {
  padding: 0.25rem 0.7rem;
  border-radius: 999px;
  font-size: 0.75rem;
  border: 1px solid var(--border);
  background-color: var(--bg-soft);
}
</style>
