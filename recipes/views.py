from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets

from comments.forms import CommentForm
from foodie_app.forms import RecipeForm
from foodie_app.models import Category
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer

# Create your views here.
def recipes(request):
    recipes = Recipe.objects.all()
    context = {
        "recipes": recipes
    }
    return render(request, "recipes/recipes.html", context)

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    new_comment = None
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.recipe = recipe
            new_comment.user = request.user
            new_comment.save()
            return redirect(recipe.get_absolute_url())
    else:
        comment_form = CommentForm()
        
    context = {
        "recipe": recipe,
        "category": recipe.category,
        "comments": recipe.comments.all(),
        "comment_form": comment_form
    }
    return render(request, "recipes/recipe.html", context)

@login_required
def add_recipe(request, category_id=None):
    print(f"user: {request.user}")
    category = None
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        form = RecipeForm(request.POST or None, initial={"category": category})
    else:
        form = RecipeForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        new_recipe = form.save(commit=False)
        new_recipe.user = request.user
        print(f"user: {request.user}")
        new_recipe.save()
        return redirect("foodie_app:category", category_id=new_recipe.id)
    
    context = {
        "form": form,
        "category": category
    }
    return render(request, "recipes/add_recipe.html", context)

def search(request):
    query = request.GET.get('query', '')
    recipes_full = Recipe.objects.filter(
        Q(name__icontains=query)
        | Q(ingredients__icontains=query)
        | Q(category__name__icontains=query)
    ).all()
    
    recipes = []
    if recipes_full:
        seen_ids = []
        
        for recipe in recipes_full:
            if recipe.id in seen_ids:
                continue
            
            seen_ids.append(recipe.id)
            recipes.append(recipe)
    
    context = {
        "recipes": recipes,
        "search": query
    }
    return render(request, 'recipes/recipes.html', context)
    
class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)