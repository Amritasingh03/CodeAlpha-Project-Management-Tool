from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db.models import Q

from .models import Project, Task, Comment


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "members"]


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "assigned_to", "status", "due_date"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Write your comment..."
                }
            )
        }


def models_query_owner(user):
    return Q(owner=user) | Q(members=user)


@login_required
def project_list(request):
    projects = Project.objects.filter(
        models_query_owner(request.user)
    ).distinct()

    total_projects = projects.count()
    tasks = Task.objects.filter(project__in=projects)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status="done").count()
    pending_tasks = total_tasks - completed_tasks

    context = {
        "projects": projects,
        "total_projects": total_projects,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
    }

    return render(request, "projects/project_list.html", context)


@login_required
def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            form.save_m2m()

            messages.success(
                request,
                "Project created successfully!"
            )
            return redirect("project_list")
    else:
        form = ProjectForm()

    return render(
        request,
        "projects/project_form.html",
        {"form": form}
    )


def get_user_project(project_id, user):
    return get_object_or_404(
        Project.objects.filter(
            models_query_owner(user)
        ).distinct(),
        pk=project_id
    )


@login_required
def project_detail(request, project_id):
    project = get_user_project(project_id, request.user)
    tasks = project.tasks.select_related("assigned_to").all()

    return render(
        request,
        "projects/project_detail.html",
        {
            "project": project,
            "tasks": tasks,
        }
    )


@login_required
def task_create(request, project_id):
    project = get_user_project(project_id, request.user)

    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()

            messages.success(
                request,
                "Task created successfully!"
            )
            return redirect(
                "project_detail",
                project_id=project.id
            )
    else:
        form = TaskForm()

    return render(
        request,
        "projects/task_form.html",
        {
            "form": form,
            "project": project,
            "page_title": "Create Task",
        }
    )


@login_required
def task_update(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    project = get_user_project(task.project_id, request.user)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Task updated successfully!"
            )
            return redirect(
                "project_detail",
                project_id=project.id
            )
    else:
        form = TaskForm(instance=task)

    return render(
        request,
        "projects/task_form.html",
        {
            "form": form,
            "project": project,
            "page_title": "Update Task",
        }
    )


@login_required
def add_comment(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    project = get_user_project(task.project_id, request.user)

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()

            messages.success(
                request,
                "Comment added successfully!"
            )

    return redirect(
        "project_detail",
        project_id=project.id
    )


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Account created successfully. Please log in."
            )
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(
        request,
        "registration/register.html",
        {"form": form}
    )