from django.views.generic import FormView

from .forms import RegisterForm


class RegisterView(FormView):
    template_name = "users/registration.html"
    form_class = RegisterForm
    success_url = "main"

    def form_valid(self, form):
        instance = form.save()
        instance.profile.save()
        return super().form_valid(form)
