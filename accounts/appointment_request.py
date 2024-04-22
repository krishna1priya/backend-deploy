import json
from django.http import JsonResponse


def appointment_request_form(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        patientFirstName = data.get('patientFirstName')
        patientLastName = data.get('patientLastName')
        patientGender = data.get('patientGender')
        contactPhone = data.get('contactPhone')
        emailAddress = data.get('emailAddress')
        appointmentDate = data.get('appointmentDate')
        appointmentTime = data.get('appointmentTime')

        return JsonResponse({'message': 'Appointment Request submitted successfully'}, status=200)

    return JsonResponse({'error': 'Method not allowed'}, status=405)