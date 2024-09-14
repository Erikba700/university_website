from django.shortcuts import render, redirect
from .forms import RegisterForm

def main(request):
    return render(request, "main.html")

def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            instance = form.save()
            instance.profile.save()
            return redirect("main")
    return render(request, "users/registration.html", {'form': form})