import json
from django.http import JsonResponse


def covid_questionnaire_form(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        symptoms = data.get('symptoms')
        positiveTest = data.get('positiveTest')
        waitingResults = data.get('waitingResults')
        testedPositive = data.get('testedPositive')
        commercialFlight = data.get('commercialFlight')
        closeProximity = data.get('closeProximity')
        higherRisk = data.get('higherRisk')
        higherRiskExplanation = data.get('higherRiskExplanation')

        return JsonResponse({'message': 'Form submitted successfully'}, status=200)

    return JsonResponse({'error': 'Method not allowed'}, status=405)