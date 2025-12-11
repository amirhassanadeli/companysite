from django.urls import path

from . import views

app_name = 'website'

urlpatterns = [
    path('', views.home, name='index'),
    path('identity/', views.business_card, name='identity'),
    path('contact/', views.contact_view, name='contact'),
    path('job-request/', views.job_request, name='job_request'),
]
