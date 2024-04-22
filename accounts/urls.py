# urls.py
from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.index, name='index'),
    path('search_doctor/',views.search_doctor,name='search_doctor'),
    path('view_all_doctors/',views.view_all_doctors,name='view_all_doctors'),
    path('search_by_specialization/',views.search_by_specialization, name='search_by_specialization'),
    path('profile_details/',views.profile_details, name='profile_details'),
    path('covid-questionnaire/',views.covid_questionnaire, name='covid_questionnaire'),
    path('search_provider/',views.search_provider,name='search_provider'),
    path('view_all_providers/',views.view_all_providers,name='view_all_providers'),
    path('view_all_packages/',views.view_all_packages,name='view_all_packages'),
    path('send_appointment_email/',views.send_appointment_email,name='send_appointment_email'),
    
    
]
