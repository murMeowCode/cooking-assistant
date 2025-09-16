from rest_framework import serializers
from .models import Dish, Ingredient, DishIngredient

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']

class DishIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = DishIngredient
        fields = ['id', 'ingredient', 'quantity']

class DishSerializer(serializers.ModelSerializer):
    match_percentage = serializers.SerializerMethodField()
    missing_ingredients = serializers.SerializerMethodField()
    
    class Meta:
        model = Dish
        fields = '__all__'
    
    def get_match_percentage(self, obj):
        if hasattr(obj, 'matching_ingredients_count') and hasattr(obj, 'total_ingredients_count'):
            if obj.total_ingredients_count > 0:
                return (obj.matching_ingredients_count / obj.total_ingredients_count) * 100
        return 0
    
    def get_missing_ingredients(self, obj):
        user_ingredients = self.context.get('user_ingredients', [])
        dish_ingredients = obj.dishingredient_set.values_list('ingredient__name', flat=True)
        return list(set(dish_ingredients) - set(user_ingredients))