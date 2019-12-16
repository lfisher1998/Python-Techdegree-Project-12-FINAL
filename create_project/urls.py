from django.conf.urls import url

from . import views

app_name = "create_project"

urlpatterns = [
    url(r"projects/$", views.all_projects, name="projects"),
    url(r"projects/new/$",
        views.NewProjectView.as_view(), name="new_project"),
    url(r"projects/(?P<project_pk>\d+)/$",
        views.project_detail, name="project_detail"),
    url(r"projects/(?P<pk>\d+)/edit/$",
        views.EditProjectView.as_view(), name="edit_project"),
    url(r"projects/(?P<project_pk>\d+)/new/position/$",
        views.create_new_position, name="create_new_position"),
    url(r"projects/(?P<project_pk>\d+)/delete/$",
        views.delete_project, name="delete_project"),
    url(r"position/(?P<position_pk>\d+)/application/new/$",
        views.apply_position, name="apply"),
    url(r"notifications/$", views.view_notifications, name="notifications"),
    url(r"applications/$", views.view_applications, name="applications"),
    url(r"applications/(?P<app_pk>\d+)/(?P<status>accept|reject)/$",
        views.app_status, name="app_status"),
    url(r"search/skill/(?P<skill>[a-zA-Z]+)/$",
        views.by_skill, name="by_skill"),
    url(r"search/$", views.search, name="search")
]