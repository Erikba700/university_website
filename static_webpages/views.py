from django.views.generic import TemplateView


class MainPageView(TemplateView):
    template_name = "main/main_page.html"


class ContactPageView(TemplateView):
    template_name = "main/contact_page.html"
