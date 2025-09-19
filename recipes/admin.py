from django.contrib import admin
from .models import Recipe

class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "user", "date_added")
    search_fields = ["name", "category__name", "user__username"]
    
# Register your models here.
admin.site.register(Recipe, RecipeAdmin)