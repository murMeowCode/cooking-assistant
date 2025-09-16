from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import AllDishListView, DishViewSet, PossibleDishesListView


router = DefaultRouter()
router.register(r'dishes', DishViewSet,basename='starred')

urlpatterns = [
    path('dishes/all/', AllDishListView.as_view()),
    path('dishes/possible/', PossibleDishesListView.as_view()),
    path('',include(router.urls))
]
