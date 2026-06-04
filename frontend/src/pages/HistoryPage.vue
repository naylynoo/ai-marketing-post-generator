<template>
  <div class="stack">
    <div class="card stack">
      <div class="card-header">
        <div>
          <div class="card-title">History</div>
          <p class="card-description">
            Recent generations are stored so you can revisit ideas without re‑typing your brief.
          </p>
        </div>
        <button class="btn btn-outline" type="button" @click="load">
          Refresh
        </button>
      </div>

      <div v-if="loading">
        <LoadingSpinner />
      </div>

      <div v-else-if="items.length === 0" class="card-description">
        No history yet. Generate your first post to see it here.
      </div>

      <div v-else class="stack">
        <div
          v-for="item in items"
          :key="item.id"
          class="history-item"
        >
          <header class="history-header">
            <div>
              <h3>{{ item.product_name }}</h3>
              <p class="meta">
                {{ item.platform_type }} · {{ new Date(item.created_at).toLocaleString() }}
              </p>
            </div>
            <button class="btn btn-ghost" type="button" @click="remove(item.id)">
              Delete
            </button>
          </header>

          <p class="body">{{ item.product_description }}</p>

          <details class="details">
            <summary>View generated copy</summary>
            <p class="label">Caption</p>
            <p class="body">{{ item.caption }}</p>

            <p class="label">Short ad text</p>
            <p class="body">{{ item.short_ad_text }}</p>

            <p class="label">Hashtags</p>
            <p class="body">{{ item.hashtags.join(" ") }}</p>

            <p class="label">Email subject</p>
            <p class="body">{{ item.email_subject }}</p>

            <p class="label">CTA</p>
            <p class="body">{{ item.cta }}</p>
          </details>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { api } from "../services/api";
import LoadingSpinner from "../components/LoadingSpinner.vue";

interface HistoryItem {
  id: number;
  product_name: string;
  product_description: string;
  target_audience: string;
  platform_type: string;
  caption: string;
  short_ad_text: string;
  hashtags: string[];
  email_subject: string;
  cta: string;
  created_at: string;
}

const items = ref<HistoryItem[]>([]);
const loading = ref(false);

const showToast = (message: string, type: "success" | "error" | "info" = "info") => {
  window.dispatchEvent(
    new CustomEvent("aimp-toast", { detail: { message, type } })
  );
};

const load = async () => {
  loading.value = true;
  try {
    const res = await api.get<{ items: HistoryItem[] }>("/history");
    items.value = res.data.items;
  } catch (error) {
    console.error(error);
    showToast("Failed to load history", "error");
  } finally {
    loading.value = false;
  }
};

const remove = async (id: number) => {
  try {
    await api.delete(`/history/${id}`);
    items.value = items.value.filter((x) => x.id !== id);
    showToast("History item deleted", "success");
  } catch (error) {
    console.error(error);
    showToast("Could not delete item", "error");
  }
};

onMounted(load);
</script>

<style scoped>
.history-item {
  border-radius: 1rem;
  border: 1px solid var(--border);
  padding: 1rem;
  background-color: var(--bg-soft);
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.history-header h3 {
  margin: 0;
  font-size: 0.95rem;
}

.meta {
  font-size: 0.75rem;
  color: var(--muted);
}

.label {
  font-size: 0.8rem;
  margin-top: 0.75rem;
  font-weight: 500;
}

.body {
  font-size: 0.85rem;
  line-height: 1.5;
}

.details summary {
  cursor: pointer;
  font-size: 0.8rem;
  margin-top: 0.5rem;
}
</style>

