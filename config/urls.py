from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Atsweb.views import (
    UserViewSet,
    ServiceViewSet,
    TechnologyViewSet,
    RealisationViewSet,
    ArticleViewSet,
    TemoignageViewSet
)

# Crée le router DRF
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'technologies', TechnologyViewSet)
router.register(r'realisations', RealisationViewSet)
router.register(r'articles', ArticleViewSet)
router.register(r'temoignages', TemoignageViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Tous tes endpoints sont ici
]
