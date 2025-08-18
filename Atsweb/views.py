from rest_framework import viewsets
from .models import User, Service, Technology, Realisation, Article, Temoignage
from .serializers import (
    UserSerializer, ServiceSerializer, TechnologySerializer,
    RealisationSerializer, ArticleSerializer, TemoignageSerializer
)
from .permissions import IsAdminOrReadOnly, IsAdminOrTemoignageUser


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminOrReadOnly]


class TechnologyViewSet(viewsets.ModelViewSet):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    permission_classes = [IsAdminOrReadOnly]


class RealisationViewSet(viewsets.ModelViewSet):
    queryset = Realisation.objects.all()
    serializer_class = RealisationSerializer
    permission_classes = [IsAdminOrReadOnly]


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAdminOrReadOnly]


class TemoignageViewSet(viewsets.ModelViewSet):
    queryset = Temoignage.objects.all()
    serializer_class = TemoignageSerializer
    permission_classes = [IsAdminOrTemoignageUser]

    def perform_create(self, serializer):
        """
        Lorsqu'un utilisateur (user ou guest) ajoute un témoignage,
        on enregistre automatiquement l'auteur (user connecté).
        """
        serializer.save(auteur=self.request.user)
