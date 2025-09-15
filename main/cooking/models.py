from django.db import models

class Dish(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructions = models.TextField()

    def __str__(self):
        return self.title 

class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"
    
class DishIngredient(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.quantity} of {self.ingredient.name} for {self.dish.title}"
