from django.db import models

class Dish(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructions = models.TextField()
    cooktime = models.IntegerField(help_text="Cook time in minutes", null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    type = models.ForeignKey('Type', on_delete=models.SET_NULL, null=True, blank=True)
    starred = models.BooleanField(default=False)
    photo = models.ImageField(null=True)
    video = models.CharField(max_length=300,null=True)

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

class Type(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
        
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    