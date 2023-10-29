from django.shortcuts import render

# Create your views here.

from django.contrib.auth.views import PasswordResetView

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'