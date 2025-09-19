from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_elasticsearch_dsl.registries import registry

class Dish(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructions = models.TextField()
    cooktime = models.IntegerField(help_text="Cook time in minutes", null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    starred = models.BooleanField(default=False)
    photo = models.ImageField()

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

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
@receiver(post_save, sender=Dish)
def update_dish_index(sender, instance, **kwargs):
    registry.update(instance)

@receiver(post_save, sender=Ingredient)
def update_ingredient_index(sender, instance, **kwargs):
    for dish_ingredient in instance.dishingredient_set.all():
        registry.update(dish_ingredient.dish)

@receiver(post_delete, sender=Dish)
def delete_dish_index(sender, instance, **kwargs):
    registry.delete(instance)
