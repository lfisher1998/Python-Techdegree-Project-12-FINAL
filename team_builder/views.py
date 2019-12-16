from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views import generic

from create_project.models import Project


class HomeView(generic.TemplateView):
    template_name = "create_project/projects.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_project'] = Project.objects.all()
        return context