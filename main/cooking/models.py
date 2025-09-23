from django.conf import settings
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
    
@receiver(post_save, sender=Dish)
def update_dish_index(sender, instance, **kwargs):
    try:
        registry.update(instance)
    except:
        if settings.DEBUG:
            print("Elasticsearch недоступен, пропускаем индексацию")
