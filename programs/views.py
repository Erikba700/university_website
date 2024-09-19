from django.views.generic import ListView, DetailView

from .models import Program, Institutes


class ProgramListView(ListView):
    model = Program
    template_name = 'programs/programs_list.html'
    context_object_name = 'programs'


class ProgramDetailView(DetailView):
    model = Program
    template_name = 'programs/programs_details.html'
    context_object_name = 'program'


class ProgramSearchView(ListView):
    model = Program
    template_name = 'programs/programs_list.html'
    context_object_name = 'results'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class InstitutesListView(ListView):
    model = Institutes
    template_name = 'programs/institutes_list.html'
    context_object_name = 'institutes'


class InstituteDetailView(DetailView):
    model = Institutes
    template_name = 'programs/institutes_details.html'
    context_object_name = 'institute'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['programs'] = Program.objects.filter(institute=self.object)

        return context
