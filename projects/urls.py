from django.urls import path
from . import views

urlpatterns = [
    path("", views.project_list, name="project_list"),
    path("create/", views.project_create, name="project_create"),
    path("register/", views.register, name="register"),

    path("<int:project_id>/", views.project_detail, name="project_detail"),
    path("<int:project_id>/tasks/create/", views.task_create, name="task_create"),
    path("tasks/<int:task_id>/edit/", views.task_update, name="task_update"),
    path("tasks/<int:task_id>/comments/", views.add_comment, name="add_comment"),
]