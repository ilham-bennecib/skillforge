from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from functools import wraps
from django.http import JsonResponse


#Création du décoratuer qui va vérifier la validité du token
def token_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        auth = JWTAuthentication()
        try:
            user, token = auth.authenticate(request)
            request.user = user  
        except AuthenticationFailed as e:
            return JsonResponse({'error': 'Token invalide ou expiré'}, status=401)
        return view_func(request, *args, **kwargs)
    return _wrapped_view