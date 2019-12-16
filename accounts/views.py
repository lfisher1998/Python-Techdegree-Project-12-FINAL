from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from . import forms, models

from create_project import views

class LoginView(generic.FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy("create_project:projects")
    template_name = "accounts/signin.html"
    
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request, **self.get_form_kwargs())
    
    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)
    
class LogoutView(generic.RedirectView):
    url = reverse_lazy("home")
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)
    
class SignUpView(generic.CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("home")
    template_name = "accounts/signup.html"
    
    
def show_profile(request):
    profile = request.user.profile
    skills = profile.skills.all()
    return render(
        request,
        'accounts/profile.html',
        {'profile': profile, 'skills': skills}
    )

def show_other_profiles(request, pk):
    profile = models.Profile.objects.get(id=pk)
    skills = profile.skills.all()
    return render(
        request,
        'accounts/profile.html',
        {'profile': profile, 'skills': skills}
    )
    
class EditProfileView(LoginRequiredMixin, generic.UpdateView):
    model = models.Profile
    fields = ['avatar', 'about', 'skills']
    success_url = reverse_lazy('accounts:view')

    def form_valid(self, form):
        if form.instance.user == self.request.user:
            return super(EditProfileView, self).form_valid(form)
        else:
            raise PermissionDenied
            

    
class ViewProfileView(generic.DetailView):
    model = models.Profile
    template_name = "accounts/profile.html"
    
    def get_context_data(self, **kwargs):
        context = super(ViewProfileView, self).get_context_data(**kwargs)
        if self.request.user:
            context['user'] = self.request.user
        return context
        
    