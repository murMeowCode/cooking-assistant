from django.urls import  path, re_path, include
from .views import AllDishListView, PossibleDishesListView, StarredDishView, StarredUpdateView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Настройка Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Cooking Assistant API",
        default_version='v1',
        description="API documentation for Cooking Assistant",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@cooking.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path('dishes/all/', AllDishListView.as_view()),
    path('dishes/possible/', PossibleDishesListView.as_view()),
    path('starred/',StarredDishView.as_view()),
    path('starred/<int:pk>/',StarredUpdateView.as_view()),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
