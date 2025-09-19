from rest_framework.generics import ListAPIView, UpdateAPIView
from .documents import DishDocument
from .models import Dish
from .serializers import DishSerializer
from django.db.models import Count, Case, When, IntegerField, F
from elasticsearch_dsl import Q

class StarredDishView(ListAPIView):
    queryset = Dish.objects.filter(starred=True)
    serialzier_class = DishSerializer

class StarredUpdateView(UpdateAPIView):
    queryset = Dish.objects.all()
    lookup_field = 'pk'

class AllDishListView(ListAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    filterset_fields = ['category__name']
    search_fields = ['title', 'description', 'instructions', 'ingredients__ingredient__name']
    ordering_fields = ['title', 'cooktime']
    ordering = ['title']
    pagination_class = None  # Disable pagination to return all results

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__name=category)
        return queryset
    


class PossibleDishesListView(ListAPIView):
    serializer_class = DishSerializer
    def get_queryset(self):
        user_ingredients = self.request.data.get('ingredients', [])
        willing_to_buy = self.request.data.get('willing_to_buy', False)
        
        if not user_ingredients:
            return Dish.objects.none()
        
        search = DishDocument.search()
        
        # Поиск всех рецептов, содержащих пользовательские ингредиенты
        query = Q(
            'nested', 
            path='ingredients',
            query=Q('terms', ingredients__id=user_ingredients)
        )
        search = search.query(query)
        
        response = search.execute()
        dish_ids = [int(hit.meta.id) for hit in response.hits]
        
        # Аннотируем количество совпадающих ингредиентов
        dishes = Dish.objects.filter(id__in=dish_ids).annotate(
            matching_ingredients_count=Count(
                Case(
                    When(dishingredient__ingredient__id__in=user_ingredients, then=1),
                    output_field=IntegerField(),
                )
            ),
            total_ingredients_count=Count('dishingredient')
        )
        
        if willing_to_buy:
            # Сортируем по количеству совпадений (убывание)
            return dishes.order_by('-matching_ingredients_count')
        else:
            # Только полностью совпадающие рецепты
            return dishes.filter(matching_ingredients_count=F('total_ingredients_count'))
    
