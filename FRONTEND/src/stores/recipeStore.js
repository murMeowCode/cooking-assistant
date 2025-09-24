import { reactive, computed } from 'vue'
import { defineStore } from 'pinia'

export const useRecipeStore = defineStore('recipes', () => {
  const state = reactive({
    recipes: [],
    favorites: [],
    filters: {
      category: 'all',
      cuisine: '',
      time: 'all',
      ingredients: [],
      hasIngredients: false
    },
    searchQuery: '',
    isLoading: false
  })

  // Геттеры
  const filteredRecipes = computed(() => {
    if (!state.filtersApplied) return state.recipes
    
    return state.recipes.filter(recipe => {
      // Фильтрация по категории
      if (state.filters.category !== 'all' && recipe.category !== state.filters.category) {
        return false
      }

      // Фильтрация по кухне
      if (state.filters.cuisine && !recipe.cuisine.includes(state.filters.cuisine)) {
        return false
      }

      // Фильтрация по времени
      if (state.filters.time !== 'all') {
        const time = parseInt(recipe.time)
        if (state.filters.time === 'quick' && time > 30) return false
        if (state.filters.time === 'medium' && (time <= 30 || time > 60)) return false
        if (state.filters.time === 'long' && time <= 60) return false
      }

      // Фильтрация по ингредиентам
      if (state.filters.hasIngredients && state.filters.ingredients.length > 0) {
        const hasIngredients = state.filters.ingredients.every(ingredient => 
          recipe.ingredients.includes(ingredient)
        )
        if (!hasIngredients) return false
      }

      return true
    })
  })

  const favoriteRecipes = computed(() => {
    return state.recipes.filter(recipe => recipe.isFavorite)
  })

  const resultsCount = computed(() => filteredRecipes.value.length)

  // Действия
  const toggleFavorite = (recipeId) => {
    const recipe = state.recipes.find(r => r.id === recipeId)
    if (recipe) {
      recipe.isFavorite = !recipe.isFavorite
      
      if (recipe.isFavorite) {
        state.favorites.push(recipeId)
      } else {
        state.favorites = state.favorites.filter(id => id !== recipeId)
      }
    }
  }

  const updateFilters = (newFilters) => {
    Object.assign(state.filters, newFilters)
  }

  const setRecipes = (recipes) => {
    state.recipes = recipes
  }

  const applyFilters = () => {
    state.filtersApplied = true
  }

  const resetFilters = () => {
    state.filters = {
      category: 'all',
      cuisine: '',
      time: 'all',
      ingredients: [],
      hasIngredients: false
    }
    state.filtersApplied = false
  }

  return {
    state,
    filteredRecipes,
    favoriteRecipes,
    resultsCount,
    toggleFavorite,
    updateFilters,
    setRecipes,
    applyFilters,
    resetFilters
  }
})