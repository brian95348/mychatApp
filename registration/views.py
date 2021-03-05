from django.contrib.auth import get_user_model
from .forms import UserRegistrationForm
from django.shortcuts import redirect
from django.views.generic.edit import FormView

# Create your views here.

User = get_user_model()

class UserRegistration(FormView):
    template_name = 'registration/register.html'
    form_class = UserRegistrationForm
    success_url = 'registration-success'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        User.objects.create_user(username,email,password)
        return redirect(self.success_url)
