from django.views.generic import TemplateView, DetailView

from programs.models import Events


class MainPageView(TemplateView):
    template_name = "main/main_page.html"


class ContactPageView(TemplateView):
    template_name = "main/contact_page.html"


class CampusLifePageView(TemplateView):
    template_name = "main/campus_life.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['events'] = Events.objects.all()

        return context


class EventsDetailView(DetailView):
    model = Events
    template_name = 'main/events/events_details_without_account.html'
    context_object_name = 'event'
