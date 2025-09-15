from rest_framework import serializers
from main.cooking.models import Dish, Ingredient, DishIngredient

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
    ingredients = DishIngredientSerializer(source='dishingredient_set', many=True)

    class Meta:
        model = Dish
        fields = ['id', 'title', 'description', 'instructions', 'ingredients']