from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "roll_number", "email", "course", "created_at")
    search_fields = ("name", "roll_number", "email", "course")
    list_filter = ("course",)
