from django.shortcuts import get_object_or_404, redirect, render
from foodie_app.forms import CategoryForm, RecipeForm
from foodie_app.models import Category
from recipes.models import Recipe
from django.contrib.auth.decorators import login_required 

# Create your views here.
def index(request):
    categories = Category.objects.all()
    context = {
        "categories": categories
    }
    return render(request, "foodie_app/index.html", context)

def category(request, category_id):
    category = Category.objects.get(id=category_id)
    recipes = Recipe.objects.filter(category__id=category_id).all()
    context = {
        "category": category,
        "recipes": recipes
    }
    return render(request, "foodie_app/category.html", context)

def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("foodie_app:home")
        
    form = CategoryForm()
    context = {"form": form}
    return render(request, "foodie_app/add_category.html", context)

@login_required
def add_recipe(request, category_id=None):
    category = None
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        form = RecipeForm(request.POST or None, initial={"category": category})
    else:
        form = RecipeForm(request.POST or None)
        
    if request.method == "POST" and form.is_valid():
        form = RecipeForm(request.POST)
        recipe = form.save(commit=False)
        recipe.user = request.user
        recipe.save()
        return redirect("recipes:recipe_detail", recipe_id=recipe.id)
    
    context = {
        "form": form,
        "category": category
    }
    
    return render(request, "foodie_app/add_recipe.html", context)