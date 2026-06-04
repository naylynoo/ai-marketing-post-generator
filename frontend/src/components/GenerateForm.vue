<template>
  <form class="stack" @submit.prevent="onSubmit">
    <div class="results-grid">
      <div class="stack">
        <div class="card">
          <div class="card-header">
            <div>
              <div class="card-title">Tell us about your product</div>
              <p class="card-description">
                Fill in a few details and we’ll draft a caption, ad text, hashtags, email subject, and CTA.
              </p>
            </div>
          </div>

          <div class="field">
            <label class="field-label" for="product-name">Product name</label>
            <input
              id="product-name"
              v-model="productName"
              class="input"
              type="text"
              placeholder="EcoGlow LED Desk Lamp"
            />
            <p class="field-help">Keep it short but descriptive.</p>
            <p v-if="errors.productName" class="field-error">{{ errors.productName }}</p>
          </div>

          <div class="field">
            <label class="field-label" for="product-description">Product description</label>
            <textarea
              id="product-description"
              v-model="productDescription"
              class="textarea"
              placeholder="Energy‑efficient LED desk lamp with adjustable arm and warm/cool light modes…"
            ></textarea>
            <p class="field-help">Highlight benefits, not just features.</p>
            <p v-if="errors.productDescription" class="field-error">
              {{ errors.productDescription }}
            </p>
          </div>

          <div class="field">
            <label class="field-label" for="target-audience">Target audience</label>
            <input
              id="target-audience"
              v-model="targetAudience"
              class="input"
              type="text"
              placeholder="Remote workers who care about eye comfort and modern design"
            />
            <p class="field-help">Who are you trying to reach?</p>
            <p v-if="errors.targetAudience" class="field-error">
              {{ errors.targetAudience }}
            </p>
          </div>

          <div class="field">
            <label class="field-label" for="platform-type">Platform</label>
            <select id="platform-type" v-model="platformType" class="select">
              <option disabled value="">Select a platform</option>
              <option value="Facebook">Facebook</option>
              <option value="Instagram">Instagram</option>
              <option value="TikTok">TikTok</option>
            </select>
            <p class="field-help">We’ll adapt tone and length for this channel.</p>
            <p v-if="errors.platformType" class="field-error">
              {{ errors.platformType }}
            </p>
          </div>

          <div class="stack-row" style="justify-content: space-between; margin-top: 0.75rem">
            <button class="btn btn-primary" type="submit" :disabled="submitting">
              <span v-if="submitting">Generating…</span>
              <span v-else>Generate marketing copy</span>
            </button>

            <button class="btn btn-ghost" type="button" @click="reset">
              Clear
            </button>
          </div>

          <div v-if="submitting" style="margin-top: 1rem">
            <LoadingSpinner />
          </div>
        </div>
      </div>

      <ResultCard
        v-if="hasResult"
        :caption="caption"
        :short-ad-text="shortAdText"
        :hashtags="hashtags"
        :email-subject="emailSubject"
        :cta="cta"
      />
    </div>
  </form>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from "vue";
import LoadingSpinner from "./LoadingSpinner.vue";
import ResultCard from "./ResultCard.vue";
import { api } from "../services/api";

interface GenerateResponse {
  id?: number;
  caption: string;
  short_ad_text: string;
  hashtags: string[];
  email_subject: string;
  cta: string;
}

const productName = ref("");
const productDescription = ref("");
const targetAudience = ref("");
const platformType = ref("");
const submitting = ref(false);

const caption = ref("");
const shortAdText = ref("");
const hashtags = ref<string[]>([]);
const emailSubject = ref("");
const cta = ref("");

const errors = reactive({
  productName: "",
  productDescription: "",
  targetAudience: "",
  platformType: ""
});

const hasResult = computed(
  () =>
    !!caption.value ||
    !!shortAdText.value ||
    !!emailSubject.value ||
    !!cta.value ||
    hashtags.value.length > 0
);

const showToast = (message: string, type: "success" | "error" | "info" = "info") => {
  window.dispatchEvent(
    new CustomEvent("aimp-toast", { detail: { message, type } })
  );
};

const validate = () => {
  errors.productName = productName.value.trim().length < 2 ? "Product name is required." : "";
  errors.productDescription =
    productDescription.value.trim().length < 10 ? "Please describe your product (at least 10 characters)." : "";
  errors.targetAudience =
    targetAudience.value.trim().length < 3 ? "Target audience is required." : "";
  errors.platformType = !platformType.value ? "Please choose a platform." : "";

  return !errors.productName &&
    !errors.productDescription &&
    !errors.targetAudience &&
    !errors.platformType;
};

const reset = () => {
  productName.value = "";
  productDescription.value = "";
  targetAudience.value = "";
  platformType.value = "";
  caption.value = "";
  shortAdText.value = "";
  hashtags.value = [];
  emailSubject.value = "";
  cta.value = "";
  Object.keys(errors).forEach((k) => (errors[k as keyof typeof errors] = ""));
};

const onSubmit = async () => {
  if (!validate()) {
    showToast("Please fix the validation errors first.", "error");
    return;
  }

  submitting.value = true;

  try {
    const payload = {
      product_name: productName.value.trim(),
      product_description: productDescription.value.trim(),
      target_audience: targetAudience.value.trim(),
      platform_type: platformType.value
    };

    const res = await api.post<GenerateResponse>("/generate", payload);

    caption.value = res.data.caption;
    shortAdText.value = res.data.short_ad_text;
    hashtags.value = res.data.hashtags ?? [];
    emailSubject.value = res.data.email_subject;
    cta.value = res.data.cta;

    showToast("Fresh copy generated ✨", "success");
  } catch (error: any) {
    console.error(error);
    showToast("Something went wrong while generating. Please try again.", "error");
  } finally {
    submitting.value = false;
  }
};
</script>
