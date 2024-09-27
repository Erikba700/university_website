from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

from programs.models import Program
from student.models import StudentProfile


class RegisterForm(UserCreationForm):
    chosen_major = forms.ModelChoiceField(queryset=Program.objects.all(), required=True)
    admission_year = forms.IntegerField(required=True)
    image = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["email"].required = True

    class Meta(UserCreationForm.Meta):
        fields = ("first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)

        user.username = self.cleaned_data['email'][:5] + get_random_string(5)

        while User.objects.filter(username=user.username).exists():
            user.username = self.cleaned_data['email'][:5] + get_random_string(5)
        if commit:
            user.save()
            profile, created = StudentProfile.objects.get_or_create(user=user)
            profile.admission_year = self.cleaned_data.get("admission_year")
            profile.image = self.cleaned_data.get("image")
            profile.chosen_major = self.cleaned_data.get("chosen_major")
            profile.save()

            subject = "Welcome to Our University"
            message = f"Dear {user.first_name},\n\nThank you for registering with us. Your username for login is {user.username}."
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [self.cleaned_data['email']]

            send_mail(subject, message, from_email, recipient_list)
        return user


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
