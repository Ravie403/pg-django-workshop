from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import UserCreationForm
from .models import User

# Create your views here.


class SignUpView(generic.CreateView):
    model = User
    form_class = UserCreationForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:home")


def HomeView(request):
    return render(request, "accounts/home.html")
