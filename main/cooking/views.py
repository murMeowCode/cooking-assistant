from rest_framework.mixins import ListModelMixin, UpdateModelMixin
from rest_framework.generics import ListAPIView
from main.cooking.models import Dish
from main.cooking.serializers import DishSerializer

class DishViewSet(ListModelMixin, UpdateModelMixin):
    starred_dishes = Dish.objects.filter(starred=True)
    serializer = DishSerializer(starred_dishes, many=True)
    queryset = starred_dishes

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)  
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
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
    pagination_class = None  # Disable pagination to return all results

    def get_queryset(self):
        ingredients = self.request('ingredients')
        if not ingredients:
            return Dish.objects.none()
        
        dishes = Dish.objects.all()
        possible_dishes = []
        for dish in dishes:
            dish_ingredients = dish.dishingredient_set.all()
            if all(any(ing.name == ingredient for ing in dish_ingredients.values_list('ingredient__name', flat=True)) for ingredient in ingredients):
                possible_dishes.append(dish)
        
        return possible_dishes