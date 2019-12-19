from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from django.views import generic
from notifications.signals import notify

from .models import Project, Position, Application
from .forms import ProjectForm, PositionForm


def all_projects(request):
    projects = Project.objects.all()
    return render(request, 'create_project/projects.html', {'projects': projects})

@login_required
def project_detail(request, project_pk):
    project = Project.objects.get(id=project_pk)
    positions = project.positions.all()
    return render(request,
                  'create_project/project_detail.html',
                  {'project': project, 'positions': positions})

class NewProjectView(LoginRequiredMixin, generic.CreateView):
    form_class = ProjectForm
    success_url = reverse_lazy("create_project:projects")
    template_name = "create_project/new_project.html"
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(NewProjectView, self).form_valid(form)
    
class EditProjectView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    fields = ['title', 'description', 'requirements', 'timeline', 'complete']
    success_url = reverse_lazy("create_project:projects")
    
    def form_valid(self, form):
        if form.instance.owner == self.request.user:
            return super(EditProjectView, self).form_valid(form)
        else:
            raise PermissionDenied
            
@login_required
def create_new_position(request, project_pk):
    project = Project.objects.get(id=project_pk)
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            position = form.save(commit=False)
            position.project = project
            position.save()
            return redirect('create_project:project_detail', project_pk=project.id)
    else:
        form = PositionForm()
    return render(request, 'create_project/create_new_position.html', {'form': form})

@login_required
def apply_position(request, position_pk):
    position = Position.objects.get(id=position_pk)
    project = position.project
    application = Application.objects.filter(
        applicant=request.user,
        position=position
    )
    if application.exists():
        return HttpResponseRedirect(reverse(
                'create_project:project_detail',
                kwargs={'project_pk': project.id}
            ))
    
    Application.objects.create(
        applicant=request.user,
        position=position
    )
    
    notify.send(
        request.user,
        recipient=request.user,
        verb="You applied to {} in project {}".format(
            position.name, project.title
        )
    )
    
    notify.send(
        request.user,
        recipient=project.owner,
        verb="{} just applied to the position {} for project {}".format(
            request.user, position.name, project.title
        )
    )
    
    return HttpResponseRedirect(reverse("create_project:notifications"))

@login_required
def view_notifications(request):
    notifications = request.user.notifications.unread()
    return render(request, 'create_project/notifications.html',
                  {'notifications': notifications})

@login_required
def view_applications(request):
    applications = Application.objects.filter(
        position__project__owner=request.user
    )
    return render(request, 'create_project/applications.html',
                  {'applications': applications})

@login_required
def app_status(request, app_pk, status):
    application = Application.objects.get(id=app_pk)
    position = Position.objects.get(application__id=application.id)
    if status == "accept":
        application.status = "A"
        application.save()
        position.filled = True
        position.save()
        notify.send(
            request.user,
            recipient=application.applicant,
            verb="{} accepted you for the position {}.".format(
                request.user,
                application.position.name
            )
        )
        notify.send(
            request.user,
            recipient=request.user,
            verb="You accepted {} for the position {}.".format(
                application.applicant,
                application.position.name
            )
        )
            
    if status == "reject":
        application.status = "R"
        application.save()
        notify.send(
            request.user,
            recipient=application.applicant,
            verb="{} rejected you for the position {}.".format(
                request.user,
                application.position.name
            )
        )
        notify.send(
            request.user,
            recipient=project.owner,
            verb="You rejected {} for the position {}.".format(
                request.user,
                application.position.name
            )
        )
    return HttpResponseRedirect(reverse('home'))
            
@login_required
def delete_project(request, project_pk):
    project = Project.objects.get(id=project_pk)
    if request.user == project.owner:
        project.delete()
        return HttpResponseRedirect(reverse("create_project:projects"))
    else:
        raise PermissionDenied
        
def search(request):
    search_term = request.GET.get('q')
    projects = Project.objects.filter(
        Q(title__icontains=search_term) | Q(description__icontains=search_term)
    )
    return render(request, 'create_project/search.html', {'projects': projects})
    
def by_skill(request, skill):
    projects = Project.objects.filter(positions__skill__name=skill)
    print("output: {}".format(projects))
    return render(request, "create_project/search.html", {'projects': projects})
    