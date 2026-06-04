<template>
  <div class="card stack">
    <div class="card-header">
      <div>
        <div class="card-title">Generated content</div>
        <p class="card-description">
          Copy what you like and tweak tone or emojis before posting.
        </p>
      </div>
      <div class="stack-row">
        <button class="btn btn-outline" type="button" @click="copyAll">
          Copy all
        </button>
        <button class="btn btn-outline" type="button" @click="downloadTxt">
          Export .txt
        </button>
      </div>
    </div>

    <section class="stack">
      <section v-if="caption">
        <header class="section-header">
          <h3>Caption</h3>
          <button class="btn btn-ghost" type="button" @click="copy(caption, 'Caption copied')">Copy</button>
        </header>
        <p class="body">{{ caption }}</p>
      </section>

      <section v-if="shortAdText">
        <header class="section-header">
          <h3>Short ad text</h3>
          <button class="btn btn-ghost" type="button" @click="copy(shortAdText, 'Ad text copied')">Copy</button>
        </header>
        <p class="body">{{ shortAdText }}</p>
      </section>

      <section v-if="hashtags?.length">
        <header class="section-header">
          <h3>Hashtags</h3>
          <button
            class="btn btn-ghost"
            type="button"
            @click="copy(hashtags.join(' '), 'Hashtags copied')"
          >
            Copy
          </button>
        </header>
        <p class="body hashtags">
          <span v-for="tag in hashtags" :key="tag" class="tag">{{ tag }}</span>
        </p>
      </section>

      <section v-if="emailSubject">
        <header class="section-header">
          <h3>Email subject</h3>
          <button class="btn btn-ghost" type="button" @click="copy(emailSubject, 'Email subject copied')">
            Copy
          </button>
        </header>
        <p class="body">{{ emailSubject }}</p>
      </section>

      <section v-if="cta">
        <header class="section-header">
          <h3>Call to action</h3>
          <button class="btn btn-ghost" type="button" @click="copy(cta, 'CTA copied')">Copy</button>
        </header>
        <p class="body">{{ cta }}</p>
      </section>
    </section>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  caption: string;
  shortAdText: string;
  hashtags: string[];
  emailSubject: string;
  cta: string;
}>();

const showToast = (message: string, type: "success" | "error" | "info" = "info") => {
  window.dispatchEvent(
    new CustomEvent("aimp-toast", { detail: { message, type } })
  );
};

const copy = async (text: string, message: string) => {
  try {
    await navigator.clipboard.writeText(text);
    showToast(message, "success");
  } catch {
    showToast("Unable to copy to clipboard", "error");
  }
};

const copyAll = () => {
  const content = [
    "Caption:",
    props.caption,
    "",
    "Short ad text:",
    props.shortAdText,
    "",
    "Hashtags:",
    props.hashtags.join(" "),
    "",
    "Email subject:",
    props.emailSubject,
    "",
    "Call to action:",
    props.cta
  ].join("\n");
  copy(content, "All content copied");
};

const downloadTxt = () => {
  const content = [
    "Caption:",
    props.caption,
    "",
    "Short ad text:",
    props.shortAdText,
    "",
    "Hashtags:",
    props.hashtags.join(" "),
    "",
    "Email subject:",
    props.emailSubject,
    "",
    "Call to action:",
    props.cta
  ].join("\n");

  const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "ai-marketing-copy.txt";
  a.click();
  URL.revokeObjectURL(url);
  showToast(".txt file downloaded", "success");
};
</script>

<style scoped>
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.4rem;
}

.section-header h3 {
  font-size: 0.95rem;
  font-weight: 600;
}

.body {
  font-size: 0.9rem;
  line-height: 1.5;
  white-space: pre-wrap;
}

.hashtags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.tag {
  padding: 0.2rem 0.55rem;
  border-radius: 999px;
  background-color: var(--bg-soft);
  border: 1px dashed var(--border);
  font-size: 0.75rem;
}
</style>
