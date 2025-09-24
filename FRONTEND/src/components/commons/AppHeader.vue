<template>
  <header>
    <div class="container">
      <div class="header-content">
        <div class="logo">
          <span class="logo-icon">👨‍🍳</span>
          Gusto
        </div>
        <nav>
          <router-link 
            to="/" 
            class="nav-link"
            :class="{ active: $route.path === '/' }"
          >
            Все рецепты
          </router-link>
          <router-link 
            to="/favorites" 
            class="nav-link"
            :class="{ active: $route.path === '/favorites' }"
          >
            Избранное
          </router-link>
        </nav>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'AppHeader'
}
</script>

<style scoped>
header {
  background: var(--card);
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
}

.logo {
  font-size: 2rem;
  font-weight: 700;
  color: var(--primary);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.logo-icon {
  font-size: 1.8rem;
}

nav {
  display: flex;
  gap: 2rem;
}

.nav-link {
  text-decoration: none;
  color: var(--text);
  font-weight: 500;
  padding: 0.7rem 1.5rem;
  border-radius: 10px;
  transition: all 0.3s ease;
  position: relative;
}

.nav-link.active {
  background: var(--primary);
  color: white;
}

.nav-link:not(.active):hover {
  background: var(--bg);
  color: var(--primary);
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
  }
  
  nav {
    width: 100%;
    justify-content: center;
  }
}
</style>