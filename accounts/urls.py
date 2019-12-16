from django.conf.urls import url

from . import views

app_name = "accounts"


urlpatterns = [
    url(r"login/$", views.LoginView.as_view(), name="signin"),
    url(r"logout/$", views.LogoutView.as_view(), name="signout"),
    url(r"signup/$", views.SignUpView.as_view(), name="signup"),
    url(r"profile/$", views.show_profile, name="view"),
    url(r"profile/(?P<pk>\d+)/$", views.show_other_profiles, name="view_other"),
    url(r"(?P<pk>\d+)/edit/$", views.EditProfileView.as_view(), name="edit"),
]