import { createRouter, createWebHistory } from "vue-router";
import CybersecurityDiagnostic from "../components/home.vue"; // Adjust path as needed
import Questions from "../components/questions.vue"; // Adjust path as needed

const routes = [
  { path: "/", component: CybersecurityDiagnostic }, // Main landing page
  { path: "/questions", component: Questions }, // Questions page
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
