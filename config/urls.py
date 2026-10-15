from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/projects/', permanent=False), name='home'),
    path('admin/', admin.site.urls),
    path('students/', include('students.urls')),
    path('projects/', include('projects.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
