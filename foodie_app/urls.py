from django.urls import include, path
from . import views
from recipes.views import RecipeViewSet
from rest_framework.routers import DefaultRouter 

app_name = "foodie_app"

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipe')

urlpatterns = [
    path("", views.index, name="home"),
    path("category/<int:category_id>", views.category, name="category"),
    path("add-category", views.add_category, name="add_category"),
    path("add-recipe", views.add_recipe, name="add_recipe"),
    path("category/<int:category_id>/add-recipe", views.add_recipe, name="add_recipe_with_category"),
    path("api/", include(router.urls))
]
