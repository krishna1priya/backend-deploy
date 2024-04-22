from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.http import JsonResponse
# from .models import Doctor, AppointmentTime
# from .forms import Doctor, AppointmentTime
import json 
from accounts.covid_questionnaire import covid_questionnaire_form
import firebase_admin
from firebase_admin import credentials, firestore

db = firestore.client()

@csrf_exempt
def index(request):
    return render(request,'accounts/index.html')

@csrf_exempt
def search_doctor(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        search_value = data.get('searchValue')
        if search_value:
            search_value = search_value
            doctors_ref = db.collection('doctor')
            query = doctors_ref.where('fullName', '>=', search_value).where('fullName', '<=', search_value+'\uf8ff')
            doctors = query.stream()
        else:
            doctors_ref = db.collection('doctor') 
            doctors = doctors_ref.stream()

        doctors_list = [doc.to_dict() for doc in doctors]

        return JsonResponse(doctors_list, safe=False, status=200)
    else:
        return JsonResponse({'error'}, status=405)
    
@csrf_exempt
def search_provider(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        search_value = data.get('searchValue', '')
        
        providers_ref = db.collection('providers')
        if search_value:
            query = providers_ref.where('name', '>=', search_value).where('name', '<=', search_value+'\uf8ff')
            providers = query.stream()
        else:
            providers = providers_ref.stream()
        
        providers_list = [doc.to_dict() for doc in providers]

        return JsonResponse(providers_list, safe=False, status=200)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
def search_by_specialization(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        search_value = data.get('searchSpecialty')
        if search_value:
            doctors_ref = db.collection('doctor')
            query = doctors_ref.where('specialization', '>=', search_value).where('specialization', '<=', search_value+'\uf8ff')
            doctors = query.stream()
        else:
            doctors_ref = db.collection('doctor') 
            doctors = doctors_ref.stream()

        doctors_list = [doc.to_dict() for doc in doctors]

        return JsonResponse(doctors_list, safe=False, status=200)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
        
@csrf_exempt
def view_all_doctors(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        doctors_ref = db.collection('doctor')
        doctors = doctors_ref.stream()
        doctors_list = [doc.to_dict() for doc in doctors]
        return JsonResponse(doctors_list, safe=False)
    else:
        return JsonResponse({'error'}, status=405)
    
@csrf_exempt
def profile_details(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
    else:
        return JsonResponse({'error'}, status=405) 
@csrf_exempt
def covid_questionnaire(request):
    return covid_questionnaire_form(request)

@csrf_exempt
def view_all_providers(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        providers_ref = db.collection('providers')
        providers = providers_ref.stream()
        
        providers_list = [doc.to_dict() for doc in providers]
        return JsonResponse(providers_list, safe=False, status=200)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def view_all_packages(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        provider_name = data.get('providerName')
        if provider_name:
            # provider_name = provider_name.lower()
            providers_ref = db.collection('providers')
            query = providers_ref.where('name', '==', provider_name)
            providers_doc = query.stream()
            for doc in providers_doc:
                provider_data = doc.to_dict()
                if 'packages' in provider_data:
                    packages = provider_data['packages']
                    packages_list = [{
                        'name': package_name,
                        **details
                    } for package_name, details in packages.items()]
                    return JsonResponse(packages_list, safe=False, status=200)

            return JsonResponse({'error': 'No matching provider or packages found'}, status=404)
        else:
            return JsonResponse({'error': 'Provider name not provided'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
def send_appointment_email(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        formData = data.get('formData')
        doctorData = data.get('doctor')
        patient_first_name = formData.get('patientFirstName')
        patient_email = formData.get('emailAddress')
        doctor_name = doctorData.get('fullName')
        doctor_email = doctorData.get('email')
        
        appointment_date = formData.get('appointmentDate')
        appointment_time = formData.get('appointmentTime')

        subject = 'Appointment Confirmation from MediApp'
        patient_message = f'Hi {patient_first_name}, Your appointment with Dr. {doctor_name} is confirmed for {appointment_date} at {appointment_time}.' 
        doctor_message = f'Hi Dr. {doctor_name}, {patient_first_name} has booked an appointment with you for {appointment_date} at {appointment_time} through MediApp.'
        send_mail(
            subject,
            patient_message,
            settings.EMAIL_HOST_USER,
            [patient_email],
            fail_silently=False,
        )
        send_mail(
            subject,
            doctor_message,
            settings.EMAIL_HOST_USER,
            [doctor_email],
            fail_silently=False,
        )
        return JsonResponse({'message': 'Email sent successfully!'}, status=200)

    else:
        return JsonResponse({'error'}, status=400)