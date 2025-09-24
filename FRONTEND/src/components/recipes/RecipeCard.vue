<template>
  <div class="recipe-card" @click="$emit('click', recipe)">
    <img :src="recipe.image" :alt="recipe.title" class="recipe-image">
    <div class="recipe-content">
      <div class="recipe-header">
        <h3 class="recipe-title">{{ recipe.title }}</h3>
        <button 
          class="favorite-btn" 
          :class="{ active: recipe.isFavorite }"
          @click.stop="toggleFavorite"
        >
          {{ recipe.isFavorite ? '★' : '☆' }}
        </button>
      </div>
      <div class="recipe-meta">
        <span>⏱ {{ recipe.time }}</span>
        <span>{{ recipe.difficulty }}</span>
        <span>{{ recipe.cuisine }}</span>
      </div>
      <p class="recipe-description">{{ recipe.description }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RecipeCard',
  props: {
    recipe: {
      type: Object,
      required: true
    }
  },
  emits: ['favorite-toggle', 'click'],
  methods: {
    toggleFavorite() {
      this.$emit('favorite-toggle', this.recipe.id)
    }
  }
}
</script>

<style scoped>
.recipe-card {
  background: var(--card);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: var(--shadow);
  transition: all 0.3s ease;
  cursor: pointer;
  border: 1px solid var(--border-light);
}

.recipe-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-hover);
  border-color: var(--primary-light);
}

.recipe-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.recipe-card:hover .recipe-image {
  transform: scale(1.05);
}

.recipe-content {
  padding: 1.5rem;
}

.recipe-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.8rem;
}

.recipe-title {
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--text);
}

.favorite-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--text-light);
  transition: all 0.3s ease;
  padding: 0.5rem;
  border-radius: 50%;
}

.favorite-btn:hover {
  background: var(--bg);
}

.favorite-btn.active {
  color: var(--accent);
  animation: heartBeat 0.6s ease;
}

@keyframes heartBeat {
  0% { transform: scale(1); }
  25% { transform: scale(1.3); }
  50% { transform: scale(0.9); }
  75% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

.recipe-meta {
  display: flex;
  gap: 1rem;
  color: var(--text-light);
  font-size: 0.9rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.recipe-description {
  color: var(--text-light);
  font-size: 0.95rem;
  line-height: 1.5;
}
</style>