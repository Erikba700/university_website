from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["email"].required = True

    class Meta(UserCreationForm.Meta):
        fields = ("first_name", "last_name", "email", "password1", "password2")
