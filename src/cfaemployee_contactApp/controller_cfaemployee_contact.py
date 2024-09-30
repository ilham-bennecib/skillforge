from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .form_cfaemployee_contact import CfaEmployeeContactForm
from . import dataMapper_cfaemployee_contact

def get_all_exchanges(request):
    all_exchanges = dataMapper_cfaemployee_contact.CfaEmployeeContactMapper().get_all_exchanges()
    if len(all_exchanges) != 0:
        exchange_list = [
            {
                'id': one_exchange[0],
                'cfaemployeeId': one_exchange[1],
                'contactId': one_exchange[2],
                'exchange': one_exchange[3],
                'createdAt': one_exchange[4],
                'updatedAt': one_exchange[5],
            } for one_exchange in all_exchanges
        ]
        return JsonResponse(exchange_list, safe=False)
    else:
        return JsonResponse({'error': 'No exchanges found'}, status=404)


def get_one_exchange(request, exchange_id):
    one_exchange = dataMapper_cfaemployee_contact.CfaEmployeeContactMapper().get_exchange_by_id(exchange_id)
    if one_exchange:
        exchange_data = {
            'id': one_exchange[0],
            'cfaemployeeId': one_exchange[1],
            'contactId': one_exchange[2],
            'exchange': one_exchange[3],
            'createdAt': one_exchange[4],
            'updatedAt': one_exchange[5],
        }
        return JsonResponse(exchange_data, safe=False)
    else:
        return JsonResponse({'error': 'Exchange not found'}, status=404)


@csrf_exempt
def create_exchange(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = CfaEmployeeContactForm(data)

            if form.is_valid():
                cfaemployee_id = form.cleaned_data['cfaemployeeId']
                contact_id = form.cleaned_data['contactId']
                exchange = form.cleaned_data['exchange']

                exchange_id = dataMapper_cfaemployee_contact.CfaEmployeeContactMapper().create_exchange(
                    cfaemployee_id=cfaemployee_id, contact_id=contact_id, exchange=exchange
                )
                return JsonResponse({'exchange_id': exchange_id, 'message': 'Exchange created successfully'})
            else:
                return JsonResponse({'error': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def update_exchange(request, exchange_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            form = CfaEmployeeContactForm(data)

            if form.is_valid():
                cfaemployee_id = form.cleaned_data['cfaemployeeId']
                contact_id = form.cleaned_data['contactId']
                exchange = form.cleaned_data['exchange']

                result = dataMapper_cfaemployee_contact.CfaEmployeeContactMapper().update_exchange(
                    exchange_id, cfaemployee_id, contact_id, exchange
                )
                return JsonResponse(result)
            else:
                return JsonResponse({'error': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def delete_exchange(request, exchange_id):
    if request.method == 'DELETE':
        result = dataMapper_cfaemployee_contact.CfaEmployeeContactMapper().delete_exchange(exchange_id)
        return JsonResponse(result)
    return JsonResponse({'error': 'Method not allowed'}, status=405)
