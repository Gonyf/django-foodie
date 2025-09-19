from rest_framework import serializers
from django.contrib.auth.models import User
from foodie_app.models import Category
from .models import Recipe

class UserSerializer(serializers.ModelSerializer):
    picture = serializers.CharField(source="profile.picture.url", read_only=True)
    class Meta:
        model = User
        fields = ["username", "picture", "id"]
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', "id"]
        
class RecipeSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Recipe
        fields = "__all__"