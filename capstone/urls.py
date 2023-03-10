"""capstone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from personnelPlanet import views
from django.views.static import serve


urlpatterns = [
    #APIs and admin
    path('admin/', admin.site.urls),
    path('availability', views.availability, name='availability'),
    path('schedules/<int:workerId>', views.schedules, name='schedules'),
    path('memo', views.memo, name='memo'),
    path('clock', views.clock, name='clock'),
    path('get_availability/<int:user>',
         views.get_availability, name='get_availability'),
    path('task', views.task, name='task'),
    path('empInfo/<int:empId>', views.empInfo, name='empInfo'),
    path('get_schedule_by_week/<int:workerId>/<str:week>',
         views.get_schedule_by_week, name='get_schedule_by_week'),
    # Views
    path('/', views.home, name='home'),
    path('shifts', views.shift, name='shifts'),
    path('profile', views.profile, name='profile'),
    path('messages', views.messages, name='messages'),
    path('addToTask', views.addToTask, name='addToTask'),
    # Authentication/Authorization
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    re_path(r'^$', views.home, name='home'),
    re_path(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,
            {'document_root': settings.STATIC_ROOT}),
]

urlpatterns + staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
