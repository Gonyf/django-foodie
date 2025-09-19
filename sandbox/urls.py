from django.urls import path
from . import views

app_name="sandbox"

urlpatterns = [
    path("", views.index, name="index"),
    path("foods/", views.RecipeListView.as_view(), name="recipe_list"),
    path("foods/<int:pk>", views.RecipeDetailView.as_view(), name="recipe_detail"),
    path("feedback", views.feedback, name="feedback"),
    path("thank-you", views.thank_you, name="thank_you"),
] 
