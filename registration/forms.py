from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()
class UserRegistrationForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput,label='confirm password')
    class Meta:
        model = User
        fields = ['username','email','password','password2',]
        widgets = {'password': forms.PasswordInput}

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError('Passwords dont match!')
        return data
