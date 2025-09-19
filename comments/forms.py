from django import forms
from comments.models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields =  ["text"]
        labels = {
            "text": "Comment"
        }
        widgets = {
            "text": forms.TextInput(attrs={"placeholder": "Type Comment..."})
        }