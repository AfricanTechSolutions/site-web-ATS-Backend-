from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Permission : 
    - Tout le monde peut lire (GET, HEAD, OPTIONS)
    - Seul un admin peut créer, modifier ou supprimer
    """
    def has_permission(self, request, view):
        # Requête "safe" → lecture autorisée
        if request.method in SAFE_METHODS:
            return True
        
        # Sinon vérifier que l'utilisateur est authentifié ET admin
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'admin'


class IsAdminOrTemoignageUser(BasePermission):
    """
    Permission pour les témoignages :
    - Tout le monde peut lire (GET)
    - Tout utilisateur authentifié peut créer (POST)
    - Seul l'admin peut modifier ou supprimer
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        
        if request.method == "POST":
            return request.user.is_authenticated
        
        # Pour PUT, PATCH, DELETE → seul admin
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'admin'


class IsOwnerOrAdmin(BasePermission):
    """
    Permission optionnelle si on veut que les utilisateurs ne puissent modifier
    que leurs propres témoignages (non utilisé dans l'instant mais pratique)
    """
    def has_object_permission(self, request, view, obj):
        # Lecture autorisée pour tous
        if request.method in SAFE_METHODS:
            return True
        
        # Modification / suppression autorisée pour l'auteur ou admin
        return request.user.is_authenticated and (
            getattr(request.user, 'role', None) == 'admin' or obj.auteur == request.user
        )
