<template>
  <div class="ingredients-section">
    <div class="ingredients-header">
      <div class="toggle-group">
        <span class="toggle-label">Могу докупить:</span>
        <label class="toggle-switch">
          <input 
            type="checkbox" 
            v-model="localHasIngredients"
            @change="updateFilter"
          >
          <span class="toggle-slider"></span>
        </label>
      </div>
      
      <div class="search-input-container" style="flex: 1;">
        <span class="search-icon">➕</span>
        <input 
          type="text" 
          class="search-input" 
          v-model="ingredientInput"
          @input="handleIngredientInput"
          @keypress.enter="addIngredient"
          placeholder="Добавьте ингредиенты..."
        >
        <div class="autocomplete-results" v-show="showAutocomplete">
          <div 
            v-for="ingredient in autocompleteResults" 
            :key="ingredient"
            class="autocomplete-result"
            @click="addIngredient(ingredient)"
          >
            {{ ingredient }}
          </div>
        </div>
      </div>
    </div>
    
    <div class="selected-ingredients">
      <div 
        v-for="ingredient in localIngredients" 
        :key="ingredient"
        class="ingredient-tag"
      >
        {{ ingredient }}
        <button class="remove-ingredient" @click="removeIngredient(ingredient)">
          ×
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, ref, watch } from 'vue'

export default {
  name: 'IngredientsFilter',
  props: {
    ingredients: {
      type: Array,
      default: () => []
    },
    hasIngredients: {
      type: Boolean,
      default: false
    },
    allIngredients: {
      type: Array,
      default: () => []
    }
  },
  emits: ['update:ingredients', 'update:hasIngredients'],
  setup(props, { emit }) {
    const localIngredients = ref([...props.ingredients])
    const localHasIngredients = ref(props.hasIngredients)
    const ingredientInput = ref('')
    const showAutocomplete = ref(false)

    const autocompleteResults = computed(() => {
      if (ingredientInput.value.length < 2) return []
      
      return props.allIngredients.filter(ingredient => 
        ingredient.toLowerCase().includes(ingredientInput.value.toLowerCase()) && 
        !localIngredients.value.includes(ingredient)
      )
    })

    const handleIngredientInput = () => {
      showAutocomplete.value = ingredientInput.value.length > 1
    }

    const addIngredient = (ingredient = null) => {
      const ingredientToAdd = ingredient || ingredientInput.value.trim()
      
      if (ingredientToAdd && !localIngredients.value.includes(ingredientToAdd)) {
        localIngredients.value.push(ingredientToAdd)
        ingredientInput.value = ''
        showAutocomplete.value = false
        updateFilter()
      }
    }

    const removeIngredient = (ingredient) => {
      localIngredients.value = localIngredients.value.filter(item => item !== ingredient)
      updateFilter()
    }

    const updateFilter = () => {
      emit('update:ingredients', [...localIngredients.value])
      emit('update:hasIngredients', localHasIngredients.value)
    }

    watch(() => props.ingredients, (newVal) => {
      localIngredients.value = [...newVal]
    })

    watch(() => props.hasIngredients, (newVal) => {
      localHasIngredients.value = newVal
    })

    return {
      localIngredients,
      localHasIngredients,
      ingredientInput,
      showAutocomplete,
      autocompleteResults,
      handleIngredientInput,
      addIngredient,
      removeIngredient,
      updateFilter
    }
  }
}
</script>

<style scoped>
.ingredients-section {
  background: var(--bg);
  padding: 1.5rem;
  border-radius: 15px;
  border: 2px dashed var(--border);
}

.ingredients-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  gap: 1rem;
}

.toggle-group {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: var(--card);
  padding: 0.8rem 1.2rem;
  border-radius: 12px;
  border: 2px solid var(--border);
}

.toggle-label {
  font-weight: 600;
  color: var(--text);
  white-space: nowrap;
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 26px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 34px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .toggle-slider {
  background-color: var(--success);
}

input:checked + .toggle-slider:before {
  transform: translateX(24px);
}

.selected-ingredients {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
}

.ingredient-tag {
  background: var(--primary);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.remove-ingredient {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  padding: 0;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: rgba(255,255,255,0.2);
}

.search-input-container {
  position: relative;
  width: 100%;
}

.search-input {
  width: 100%;
  padding: 1rem 1.2rem 1rem 3rem;
  border: 2px solid var(--border);
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: var(--card);
}

.search-input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(74, 108, 247, 0.1);
}

.search-icon {
  position: absolute;
  left: 1.2rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-light);
}

.autocomplete-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: var(--card);
  border: 2px solid var(--border);
  border-radius: 12px;
  margin-top: 0.5rem;
  box-shadow: var(--shadow-hover);
  z-index: 10;
  max-height: 200px;
  overflow-y: auto;
}

.autocomplete-result {
  padding: 1rem 1.2rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border-bottom: 1px solid var(--border-light);
}

.autocomplete-result:last-child {
  border-bottom: none;
}

.autocomplete-result:hover {
  background: var(--bg);
  color: var(--primary);
}

@media (max-width: 768px) {
  .ingredients-header {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>