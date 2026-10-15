from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm

def student_list(request):
    students = Student.objects.all().order_by("name")
    return render(request, "students/student_list.html", {"students": students})

def student_add(request):
    form = StudentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("student_list")
    return render(request, "students/student_form.html", {"form": form})

def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        return redirect("student_list")
    return render(request, "students/student_confirm_delete.html", {"student": student})
