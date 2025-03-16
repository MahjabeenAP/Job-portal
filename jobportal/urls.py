"""
URL configuration for jobportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from jobs.views import *

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("alljobs/",jobfn,name='jobfn'),
    path("viewjob/<int:job_id>",detailjobfn),
    path("apply/<int:job_id>",applicationformfn),
    path('myapplications/',jobseekerapplications),
    path('editapplication/<int:v_id>',edit_application),
    path('deleteapplication/<int:v_id>',delete_application),

    path('reg/',registerfn),
    path('',login_view),
    path('logout/',logoutfn),
    
    path('emp/',employer_dashboard),
    path('newjob/',job_create,name="job_create"),
    path('addcategory/',add_category),
    path('addtype/',add_job_type),
    path('myjobs/',my_jobs),
    path('editjob/<int:p_id>',update_job),
    path('deletejob/<int:p_id>',delete_job),
    path('mycandidates/',view_applications),
    path('viewapplicant/<int:v_id>',viewapplicantdetails, name='viewapplicantdetails'),
    # path('update-status/<int:v_id>', update_application_status, name='update_application_status'),
    


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
