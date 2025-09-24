<template>
  <section class="hero">
    <div class="container">
      <div class="hero-content">
        <h1>Откройте мир вкуса</h1>
        <p>Более 1000 проверенных рецептов для каждого дня. Готовьте с удовольствием!</p>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'HeroSection'
}
</script>

<style scoped>
.hero {
  text-align: center;
  padding: 4rem 0 3rem;
  background: linear-gradient(135deg, #4A6CF7 0%, #6A8AFF 50%, #8CABFF 100%);
  color: white;
  margin-bottom: 2rem;
  border-radius: 0 0 30px 30px;
  position: relative;
  overflow: hidden;
}

.hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" opacity="0.1"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="white"/><circle cx="20" cy="20" r="0.5" fill="white"/><circle cx="80" cy="80" r="0.7" fill="white"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
}

.hero-content {
  position: relative;
  z-index: 2;
}

.hero h1 {
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
  background: linear-gradient(45deg, #FFFFFF, #F0F4FF);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero p {
  font-size: 1.3rem;
  opacity: 0.95;
  max-width: 600px;
  margin: 0 auto 2rem;
  font-weight: 300;
}

@media (max-width: 768px) {
  .hero h1 {
    font-size: 2.5rem;
  }
}
</style>