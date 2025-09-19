from urllib import request
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import ListView, DetailView
from django.contrib import messages
from sandbox.forms import FeedbackForm

from recipes.models import Recipe
from sandbox.models import Feedback
[
    "alert-error",
    "alert-success",
    "alert-warning",
    "alert-info",
]
# Create your views here.
def index(request):
    data = {
        "recipes": Recipe.objects.all(),
        "children": ["marie", "eric"]
    }
    
    return render(request, "sandbox/index.html", data)

class RecipeListView(ListView):
    model = Recipe
    template_name = "sandbox/index.html"
    context_object_name = "recipes"
    
class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "sandbox/detail.html"
    
def feedback(request):
    request.session["feedback_visits"] = request.session.get("feedback_visits", 0) + 1
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            data = (form.cleaned_data)
            Feedback.objects.create(
                name = data["name"],
                email = data["email"],
                feedback = data["feedback"],
                satisfaction = data["satisfaction"]
            )
            
            messages.success(request, "Thanks for your feedback")
            return redirect("sandbox:index")
    else:
        form = FeedbackForm()
        
    context = {
        "form": form,
        "visits": request.session["feedback_visits"]
    }
    return render(request, "sandbox/feedback_form.html", context)
    
def thank_you(request):
    return HttpResponse("Thanks, man!")