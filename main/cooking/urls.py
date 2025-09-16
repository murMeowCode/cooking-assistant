from django.urls import  path
from .views import AllDishListView, PossibleDishesListView, StarredDishView, StarredUpdateView




urlpatterns = [
    path('dishes/all/', AllDishListView.as_view()),
    path('dishes/possible/', PossibleDishesListView.as_view()),
    path('starred/',StarredDishView.as_view()),
    path('starred/<int:pk>/',StarredUpdateView.as_view())
]
