from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomLoginForm, CustomSignUpForm

# Create your views here.
class SignUpView(CreateView):
    form_class = CustomSignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

class LoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'registration/login.html'

class LogoutView(LogoutView):
    template_name = 'registration/logout.html'
