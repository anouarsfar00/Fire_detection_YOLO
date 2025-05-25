# ce fichier est pour des décorateurs personnalisés (Ajout de permissions utilisateur et restriction de pages
# basées sur les niveaux d'authentification des utilisateurs ((clients/superviseurs/admins)) avec des décorateurs de vue personnalisés.) 
# que nous avons créés au lieu de ceux faits par Django
# pour simplifier, écrit ici (dans un fichier séparé) afin de rendre le code plus propre
#decorators c'est une fonction qui prend un autre fonction comme des parametres (+ & -)
from functools import wraps
from django.shortcuts import *
from Superviseur.models import Superviseur, Client

#si le user est authentifié, il ne peut pas acceder la page avec ce decorator (exemple: login page)
def user_is_authenticated(view_func): 
    def wrapper_func(request, *args, **kwargs): 
        pseudo = request.session.get('user_pseudo')
        if request.user.is_authenticated: 
            if pseudo and Superviseur.objects.filter(pseudo=pseudo).exists():
                return redirect('dashboard_superviseur') 
            else:
                if pseudo and Client.objects.filter(pseudo=pseudo).exists():
                    return redirect('dashboard_client') 
        else: return view_func(request, *args, **kwargs)
    return wrapper_func

#si le superviseur est authentifié, il ne peut pas acceder au application client
def user_is_superviseur(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Assuming the user's pseudo is stored in the session 
        pseudo = request.session.get('user_pseudo')
        if pseudo and Superviseur.objects.filter(pseudo=pseudo).exists():
            return view_func(request, *args, **kwargs)
        else:
            return render(request, 'client_error.html')
    return _wrapped_view


#si le client est authentifié, il ne peut pas acceder au application superviseur
def user_is_client(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        pseudo = request.session.get('user_pseudo')
        if pseudo and Client.objects.filter(pseudo=pseudo).exists():
            return view_func(request, *args, **kwargs)
        else:
            return render(request, 'superviseur_error.html')
    return _wrapped_view
