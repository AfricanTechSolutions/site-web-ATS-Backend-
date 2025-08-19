from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from Atsweb.views import (
    UserViewSet,
    LogoutView,
    ServiceViewSet,
    TechnologyViewSet,
    RealisationViewSet,
    ArticleViewSet,
    TemoignageViewSet,
    MyTokenObtainPairView,
    DashboardStatsView,  # Add this view for dashboard stats
    RegisterView,        # Add this for user registration
    CurrentUserView,     # Add this for current user details
)

# Create DRF router
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'technologies', TechnologyViewSet)
router.register(r'realisations', RealisationViewSet)
router.register(r'articles', ArticleViewSet)
router.register(r'temoignages', TemoignageViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API routes
    path('api/', include(router.urls)),  # Changed from 'Atsweb/' to 'api/' for clarity
    
    # Authentication endpoints
    path('api/auth/login/', csrf_exempt(MyTokenObtainPairView.as_view()), name='token_obtain_pair'),
    path('api/auth/refresh/', ensure_csrf_cookie(TokenRefreshView.as_view()), name='token_refresh'),
    path('api/auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    
    # Dashboard specific endpoints
    path('api/dashboard/stats/', DashboardStatsView.as_view(), name='dashboard_stats'),
    
    # User management actions (for admin dashboard)
    path('api/users/<int:user_id>/suspend/', UserViewSet.as_view({'post': 'suspend'}), name='user_suspend'),
    path('api/users/<int:user_id>/activate/', UserViewSet.as_view({'post': 'activate'}), name='user_activate'),
    path('api/users/<int:pk>/set-admin/', 
         UserViewSet.as_view({'post': 'set_admin'}), 
         name='user-set-admin'),
    
    # Current user endpoint
    path('api/current-user/', CurrentUserView.as_view(), name='current-user'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)