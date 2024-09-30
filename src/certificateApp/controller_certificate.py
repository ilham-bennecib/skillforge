from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .form_certificate import CertificateForm
from . import dataMapper_certificate

def get_all_certificates(request):
    all_certificates = dataMapper_certificate.CertificateMapper().get_all_certificates()
    if len(all_certificates) != 0:
        certificate_list = [
            {
                'id': one_certificate[0],
                'title': one_certificate[1],
                'description': one_certificate[2],
                'date': one_certificate[3],
                'status': one_certificate[4],
                'type': one_certificate[5],
                'level': one_certificate[6],
                'studentId': one_certificate[7],
                'createdAt': one_certificate[8],
                'updatedAt': one_certificate[9],
            } for one_certificate in all_certificates
        ]
        return JsonResponse(certificate_list, safe=False)
    else:
        return JsonResponse({'error': 'Certificates not found'}, status=404)


def get_one_certificate(request, certificate_id):
    one_certificate = dataMapper_certificate.CertificateMapper().get_certificate_by_id(certificate_id)
    if one_certificate:
        certificate_data = {
            'id': one_certificate[0],
            'title': one_certificate[1],
            'description': one_certificate[2],
            'date': one_certificate[3],
            'status': one_certificate[4],
            'type': one_certificate[5],
            'level': one_certificate[6],
            'studentId': one_certificate[7],
            'createdAt': one_certificate[8],
            'updatedAt': one_certificate[9],
        }
        return JsonResponse(certificate_data, safe=False)
    else:
        return JsonResponse({'error': 'Certificate not found'}, status=404)


@csrf_exempt
def create_certificate(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = CertificateForm(data)

            if form.is_valid():
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                date = form.cleaned_data['date']
                status = form.cleaned_data['status']
                cert_type = form.cleaned_data['type']
                level = form.cleaned_data['level']
                student_id = form.cleaned_data['studentId']

                certificate_id = dataMapper_certificate.CertificateMapper().create_certificate(
                    title=title, description=description, date=date, status=status, cert_type=cert_type, level=level, student_id=student_id
                )
                return JsonResponse({'certificate_id': certificate_id, 'message': 'Certificate created successfully'})
            else:
                return JsonResponse({'error': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def update_certificate(request, certificate_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            form = CertificateForm(data)

            if form.is_valid():
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                date = form.cleaned_data['date']
                status = form.cleaned_data['status']
                cert_type = form.cleaned_data['type']
                level = form.cleaned_data['level']
                student_id = form.cleaned_data['studentId']

                result = dataMapper_certificate.CertificateMapper().update_certificate(
                    certificate_id, title, description, date, status, cert_type, level, student_id
                )
                return JsonResponse(result)
            else:
                return JsonResponse({'error': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def delete_certificate(request, certificate_id):
    if request.method == 'DELETE':
        result = dataMapper_certificate.CertificateMapper().delete_certificate(certificate_id)
        return JsonResponse(result)
    return JsonResponse({'error': 'Method not allowed'}, status=405)
