<template>
  <button class="btn btn-outline" @click="toggle">
    <span v-if="isDark">☀︎ Light</span>
    <span v-else>☾ Dark</span>
  </button>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";

const isDark = ref(false);

const apply = () => {
  const body = document.body;
  if (isDark.value) {
    body.classList.add("dark");
  } else {
    body.classList.remove("dark");
  }
  localStorage.setItem("aimp-theme", isDark.value ? "dark" : "light");
};

const toggle = () => {
  isDark.value = !isDark.value;
  apply();
};

onMounted(() => {
  const saved = localStorage.getItem("aimp-theme");
  isDark.value = saved === "dark";
  apply();
});
</script>
