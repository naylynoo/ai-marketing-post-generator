import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../pages/HomePage.vue";
import GeneratePage from "../pages/GeneratePage.vue";
import HistoryPage from "../pages/HistoryPage.vue";

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", name: "home", component: HomePage },
    { path: "/generate", name: "generate", component: GeneratePage },
    { path: "/history", name: "history", component: HistoryPage }
  ]
});
