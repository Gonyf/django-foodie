from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from accounts.forms import UserProfileForm

# Create your views here.
def register(request):
    if request.method != "POST":
        form = UserCreationForm()
    else:
        form = UserCreationForm(data = request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect("foodie_app:home")
        
    context = {
        "form": form
    }
    return render(request, "registration/register.html", context)

def edit_user_profile(request):
    if request.method == "POST":
        print(request.FILES)
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect("foodie_app:home")
    else:
        form = UserProfileForm(instance=request.user.profile)
    
    context = {'form': form}
    return render(request, "accounts/edit_profile.html", context)