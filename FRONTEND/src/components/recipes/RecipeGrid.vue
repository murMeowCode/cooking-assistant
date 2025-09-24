<template>
  <section class="recipes-grid">
    <div v-if="recipes.length === 0" class="empty-state">
      <h3>Рецепты не найдены</h3>
      <p>Попробуйте изменить параметры фильтрации</p>
    </div>
    
    <RecipeCard
      v-for="recipe in recipes"
      :key="recipe.id"
      :recipe="recipe"
      @favorite-toggle="$emit('favorite-toggle', $event)"
      @click="$emit('recipe-click', recipe)"
    />
  </section>
</template>

<script>
import RecipeCard from './RecipeCard.vue'

export default {
  name: 'RecipeGrid',
  components: {
    RecipeCard
  },
  props: {
    recipes: {
      type: Array,
      default: () => []
    }
  },
  emits: ['favorite-toggle', 'recipe-click']
}
</script>

<style scoped>
.recipes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: var(--text-light);
  grid-column: 1 / -1;
}

.empty-state h3 {
  margin-bottom: 1rem;
  color: var(--text);
}

@media (max-width: 768px) {
  .recipes-grid {
    grid-template-columns: 1fr;
  }
}
</style>