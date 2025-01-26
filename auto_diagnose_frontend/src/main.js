import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import axios from 'axios';

// Import the global styles
import './assets/styles.css';

const app = createApp(App);

// Add Axios to the global properties to make it available as `this.$axios`
app.config.globalProperties.$axios = axios;

app.use(router).mount('#app');
