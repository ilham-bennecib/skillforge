from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from functools import wraps
from django.http import JsonResponse

# Création du décorateur qui vérifie la validité du token
def token_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        print("Authorization Header:", request.headers.get('Authorization'))  # Debug ici
        auth = JWTAuthentication()
        try:
            # Authentifier la requête
            result = auth.authenticate(request)
            if result is None:
                return JsonResponse({'error': 'Token manquant ou invalide'}, status=401)

            # Décomposer le résultat
            user, token = result
            request.user = user  # Ajouter l'utilisateur à la requête
            request.token = token  # Rendre le token disponible si nécessaire

        except AuthenticationFailed as e:
            return JsonResponse({'error': 'Token invalide ou expiré'}, status=401)

        # Continuer avec la vue
        return view_func(request, *args, **kwargs)
    return _wrapped_view
