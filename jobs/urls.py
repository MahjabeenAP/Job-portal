from django.urls import path
from . import api_views 
from .api_views import apiregisterfn, apiloginfn, apilogoutfn

urlpatterns = [
    # User APIs
    path('users/', api_views.user_list_create, name='user-list-create'),
    path('users/<int:pk>/', api_views.user_detail, name='user-detail'),

    # Job Category APIs
    path('jobcategories/', api_views.jobcategory_list_create, name='jobcategory-list-create'),
    path('jobcategories/<int:pk>/', api_views.jobcategory_detail, name='jobcategory-detail'),

    # JobType APIs
    path('jobtypes/', api_views.jobtype_list_create, name='jobtype-list-create'),
    path('jobtypes/<int:pk>/', api_views.jobtype_detail, name='jobtype-detail'),

    # Job APIs
    path('jobs/', api_views.job_list_create, name='job-list-create'),
    path('jobs/<int:pk>/', api_views.job_detail, name='job-detail'),

    # Application APIs
    path('applications/', api_views.application_list_create, name='application-list-create'),
    path('applications/<int:pk>/', api_views.application_detail, name='application-detail'),

    # Interview APIs
    path('interviews/', api_views.interview_list_create, name='interview-list-create'),
    path('interviews/<int:pk>/', api_views.interview_detail, name='interview-detail'),

    path('register/', apiregisterfn, name='api_register'),
    path('login/', apiloginfn, name='api_login'),
    path('logout/', apilogoutfn, name='api_logout'),
   
]