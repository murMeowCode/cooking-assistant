from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Dish
from .serializers import DishSerializer, DishUpdateSerializer, ElasticDishSerializer
from django.db.models import Count, F, Q
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10

class StarredDishView(ListAPIView):
    queryset = Dish.objects.filter(starred=True)
    serializer_class = DishSerializer

class StarredUpdateView(UpdateAPIView):
    serializer_class = DishUpdateSerializer
    queryset = Dish.objects.all()
    lookup_field = 'pk'

class AllDishListView(ListAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    filterset_fields = ['category__name']
    search_fields = ['title', 'description', 'instructions', 'ingredients__ingredient__name']
    ordering_fields = ['title', 'cooktime']
    ordering = ['title']

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__name=category)
        return queryset
    

class PossibleDishesListView(APIView):
    pagination_class = CustomPagination
    
    def post(self, request):
        user_ingredients = request.data.get('ingredients', [])
        willing_to_buy = request.data.get('willing_to_buy', False)
        
        if not user_ingredients:
            return self.get_paginated_response([])
        
        # Аннотируем все блюда с количеством совпадающих ингредиентов
        dishes = Dish.objects.annotate(
            matching_ingredients_count=Count(
                'dishingredient__ingredient_id',
                filter=Q(dishingredient__ingredient_id__in=user_ingredients),
                distinct=True
            ),
            total_ingredients_count=Count('dishingredient__ingredient_id', distinct=True)
        )
        
        if willing_to_buy:
            # При willing_to_buy=True: показываем все блюда, где есть ХОТЯ БЫ ОДИН совпадающий ингредиент
            dishes = dishes.filter(matching_ingredients_count__gte=1)
            dishes = dishes.order_by('-matching_ingredients_count', 'title')
        else:
            # При willing_to_buy=False: показываем только блюда, которые можно приготовить ПОЛНОСТЬЮ
            dishes = dishes.filter(matching_ingredients_count=F('total_ingredients_count'))
            dishes = dishes.order_by('title')
        
        # Пагинация
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(dishes, request, view=self)
        
        serializer = ElasticDishSerializer(
            page, 
            many=True,
            context={'user_ingredients': user_ingredients}
        )
        
        return paginator.get_paginated_response(serializer.data)
    
    def get_paginated_response(self, data):
        return Response({
            'count': 0,
            'next': None,
            'previous': None,
            'results': data
        })
