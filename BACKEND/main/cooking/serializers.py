from rest_framework import serializers
from .models import Dish, Ingredient, DishIngredient

class DishUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id','starred']

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']

class DishIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = DishIngredient
        fields = ['id', 'ingredient', 'quantity']

class ElasticDishSerializer(serializers.ModelSerializer):
    match_percentage = serializers.SerializerMethodField()
    missing_ingredients = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)
    type_name = serializers.CharField(source='type.name', read_only=True)
    
    class Meta:
        model = Dish
        fields = [
            'id', 'title', 'description', 'instructions', 'cooktime', 
            'starred', 'photo', 'video','category_name', 'type_name',
            'match_percentage','missing_ingredients'
        ]
    
    def get_match_percentage(self, obj):
        # ПРАВИЛЬНЫЙ расчет процента совпадения
        if hasattr(obj, 'total_ingredients_count') and obj.total_ingredients_count > 0:
            return round((obj.matching_ingredients_count / obj.total_ingredients_count) * 100, 1)
        return 0
    
    def get_missing_ingredients(self, obj):
        user_ingredients = self.context.get('user_ingredients', [])
        # Получаем все ингредиенты блюда
        dish_ingredients = obj.dishingredient_set.select_related('ingredient').all()
        
        missing = []
        for dish_ingredient in dish_ingredients:
            if dish_ingredient.ingredient.id not in user_ingredients:
                missing.append(dish_ingredient.ingredient.name)
        
        return missing
    
class DishSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    type_name = serializers.CharField(source='type.name', read_only=True)
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Dish
        fields = [
            'id', 'title', 'description', 'instructions', 'cooktime', 
            'starred', 'photo', 'video','category_name', 'type_name',
            'ingredients'
        ]

    def get_ingredients(self, obj):
        # Получаем все ингредиенты блюда
        dish_ingredients = obj.dishingredient_set.select_related('ingredient').all()
        
        ingredients = []
        for dish_ingredient in dish_ingredients:
            ingredients.append(dish_ingredient.ingredient.name)
        
        return ingredients
