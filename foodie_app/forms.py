from django import forms
from foodie_app.models import Category
from recipes.models import Recipe

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields =  ["name"]
        labels = {
            "name": "Category Name"
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Category Name"})
        }
        
class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            "name",
            "description",
            "ingredients",
            "directions",
            "category",
        ]
        labels = {
            "name": "Title"
        }
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Title"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter description...",
                "rows": 5
            }),
            "category": forms.Select(attrs={
                "class": "form-select"
            })
        }