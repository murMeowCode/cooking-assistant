# documents.py
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Dish, Ingredient

@registry.register_document
class DishDocument(Document):
    ingredients = fields.NestedField(properties={
        'name': fields.TextField(),
        'quantity': fields.TextField(),
    })
    
    category = fields.ObjectField(properties={
        'name': fields.TextField(),
    })
    
    class Index:
        name = 'dishes'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}
    
    class Django:
        model = Dish
        fields = ['title', 'description', 'instructions', 'cooktime', 'starred']
        
        related_models = [Ingredient]
    
    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Ingredient):
            return related_instance.dishingredient_set.all().values_list('dish', flat=True)