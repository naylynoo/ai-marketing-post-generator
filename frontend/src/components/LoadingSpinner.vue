<template>
  <div class="spinner-wrap">
    <div class="spinner"></div>
    <span class="label">Generating smart copy…</span>
  </div>
</template>

<script setup lang="ts"></script>

<style scoped>
.spinner-wrap {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  padding: 0.75rem 1rem;
  border-radius: 999px;
  background-color: var(--bg-soft);
  border: 1px solid var(--border);
  width: fit-content;
}

.spinner {
  width: 18px;
  height: 18px;
  border-radius: 999px;
  border: 2px solid rgba(148, 163, 184, 0.5);
  border-top-color: var(--primary);
  animation: spin 0.7s linear infinite;
}

.label {
  font-size: 0.85rem;
  color: var(--muted);
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
