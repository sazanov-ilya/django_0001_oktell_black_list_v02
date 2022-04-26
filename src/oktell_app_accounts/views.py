from django.shortcuts import render

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


class SignUpView(generic.CreateView):
    # Общий класс представления (generic) CreateView наследуется в классе SignUpView.
    form_class = UserCreationForm  # Используем встроенную UserCreationForm
    success_url = reverse_lazy('add_number')  # Перенаправление ТОЛЬКО успешной регистрации
    template_name = 'accounts/authentication.html'
