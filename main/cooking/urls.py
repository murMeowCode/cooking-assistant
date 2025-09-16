from django.urls import path
from views import AllDishListView,DishViewSet,PossibleDishesListView

urls = [
    path('dishes/all/',AllDishListView.as_view()),
    path('dishes/starred/',DishViewSet),
    path('dishes/possible/',PossibleDishesListView.as_view())
]