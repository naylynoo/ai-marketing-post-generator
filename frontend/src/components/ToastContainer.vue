<template>
  <div class="toast-container">
    <transition-group name="toast">
      <div v-for="toast in toasts" :key="toast.id" class="toast" :class="toast.type">
        {{ toast.message }}
      </div>
    </transition-group>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref } from "vue";

type ToastType = "success" | "error" | "info";

interface Toast {
  id: number;
  message: string;
  type: ToastType;
}

const toasts = ref<Toast[]>([]);

let counter = 0;

const addToast = (message: string, type: ToastType = "info") => {
  const id = ++counter;
  toasts.value.push({ id, message, type });
  setTimeout(() => {
    toasts.value = toasts.value.filter((t) => t.id !== id);
  }, 3500);
};

const handler = (event: CustomEvent<{ message: string; type?: ToastType }>) => {
  addToast(event.detail.message, event.detail.type ?? "info");
};

onMounted(() => {
  window.addEventListener("aimp-toast" as any, handler as any);
});

onUnmounted(() => {
  window.removeEventListener("aimp-toast" as any, handler as any);
});
</script>

<style scoped>
.toast-container {
  position: fixed;
  bottom: 1.25rem;
  right: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  z-index: 40;
}

.toast {
  min-width: 220px;
  padding: 0.7rem 0.95rem;
  border-radius: 0.9rem;
  font-size: 0.85rem;
  color: #0b1120;
  background-color: #e5e7eb;
  box-shadow:
    0 10px 30px rgba(15, 23, 42, 0.25),
    0 0 0 1px rgba(148, 163, 184, 0.5);
}

.toast.success {
  background-color: #bbf7d0;
}

.toast.error {
  background-color: #fecaca;
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.24s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(6px) scale(0.96);
}
</style>
