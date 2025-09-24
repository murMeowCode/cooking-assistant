<template>
  <div id="app">
    <AppHeader />
    <router-view />
  </div>
</template>

<script>
import AppHeader from '@/components/common/AppHeader.vue'

export default {
  name: 'App',
  components: {
    AppHeader
  }
}
</script>

<style>
/* Глобальные стили из оригинального файла */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

:root {
  --primary: #4A6CF7;
  --primary-light: #6A8AFF;
  --primary-dark: #3A5CE5;
  --bg: #F9F9F9;
  --card: #FFFFFF;
  --text: #333333;
  --text-light: #666666;
  --border: #E0E0E0;
  --border-light: #F0F0F0;
  --accent: #FF6B6B;
  --success: #4CAF50;
  --warning: #FF9800;
  --shadow: 0 2px 15px rgba(0,0,0,0.08);
  --shadow-hover: 0 8px 25px rgba(0,0,0,0.15);
}

body {
  background-color: var(--bg);
  color: var(--text);
  line-height: 1.6;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

@media (max-width: 768px) {
  .container {
    padding: 0 15px;
  }
}
</style>