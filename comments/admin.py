from django.contrib import admin
from comments.models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ["recipe", "text", "user"]
    search_fields = ["text", "recipe__name", "user__username"]
    
# Register your models here.
admin.site.register(Comment, CommentAdmin)