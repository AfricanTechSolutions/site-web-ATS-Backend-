from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

from .permissions import IsAdminOrReadOnly, IsAdminOrTemoignageUser
from .models import Service, Technology, Realisation, Article, Temoignage, PREDEFINED_ADMINS
from .serializers import (
    UserSerializer, UserListSerializer, MyTokenObtainPairSerializer,
    ServiceSerializer, ServiceListSerializer, TechnologySerializer,
    RealisationSerializer, RealisationListSerializer, ArticleSerializer, ArticleListSerializer,
    TemoignageSerializer, TemoignageListSerializer, DashboardStatsSerializer
)

User = get_user_model()


# --- User Registration / Management ---
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]  # everyone can register

    def get_serializer_class(self):
        """Use different serializers for list vs detail views"""
        if self.action == 'list':
            return UserListSerializer
        return UserSerializer

    def get_permissions(self):
        """Different permissions for different actions"""
        if self.action == 'create':  # Registration
            permission_classes = [AllowAny]
        elif self.action in ['suspend', 'activate', 'list', 'destroy']:
            permission_classes = [IsAuthenticated]  # Only authenticated admins
        else:
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        ip = self.request.META.get('REMOTE_ADDR')
        serializer.save(ip_address=ip, role='guest')

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if user.username in PREDEFINED_ADMINS:
            return Response(
                {'error': 'Cannot delete predefined admin users'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def suspend(self, request, pk=None):
        """Suspend a user (set is_active=False)"""
        user = self.get_object()
        if user.username in PREDEFINED_ADMINS:
            return Response(
                {'error': 'Cannot suspend predefined admin users'},
                status=status.HTTP_403_FORBIDDEN
            )
        user.is_active = False
        user.save()
        return Response({'status': 'User suspended'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate a user (set is_active=True)"""
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({'status': 'User activated'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def set_admin(self, request, pk=None):
        """Set a user as admin"""
        if not request.user.role == 'admin':
            return Response(
                {'error': 'Only admins can perform this action'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            user = self.get_object()
            user.role = 'admin'
            user.save()
            return Response(
                {'message': f'User {user.username} is now an admin'}, 
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )


# --- JWT Login with Email ---
class MyTokenObtainPairView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = MyTokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get the refresh token from the request data
            refresh_token = request.data.get("refresh")
            if refresh_token:
                # Blacklist the refresh token to invalidate it
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            # Optionally, clear any session data
            # If you're using session authentication alongside JWT, you can clear the session
            # request.session.flush()
            
            return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# --- Registration View ---
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            ip = request.META.get('REMOTE_ADDR')
            user = serializer.save(ip_address=ip, role='guest')
            return Response({
                'message': 'User created successfully',
                'user_id': user.id,
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- Dashboard Stats View ---
class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Calculate stats for dashboard
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        stats = {
            'total_users': User.objects.count(),
            'total_articles': Article.objects.count(),
            'total_services': Service.objects.count(),
            'total_realisations': Realisation.objects.count(),
            'total_temoignages': Temoignage.objects.count(),
            'recent_users': User.objects.filter(date_joined__gte=thirty_days_ago).count(),
            'active_users': User.objects.filter(is_active=True).count(),
            'suspended_users': User.objects.filter(is_active=False).count(),
        }
        
        serializer = DashboardStatsSerializer(stats)
        return Response(serializer.data, status=status.HTTP_200_OK)


# --- CRUD for other models ---
class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all().order_by('-heure_cree')
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return ServiceListSerializer
        return ServiceSerializer

    def perform_create(self, serializer):
        serializer.save(auteur=self.request.user)


class TechnologyViewSet(viewsets.ModelViewSet):
    queryset = Technology.objects.all().order_by('name')
    serializer_class = TechnologySerializer
    permission_classes = [IsAdminOrReadOnly]


class RealisationViewSet(viewsets.ModelViewSet):
    queryset = Realisation.objects.all().order_by('-heure_cree')
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return RealisationListSerializer
        return RealisationSerializer

    def perform_create(self, serializer):
        serializer.save(auteur=self.request.user)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('-heure_cree')
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        return ArticleSerializer


class TemoignageViewSet(viewsets.ModelViewSet):
    queryset = Temoignage.objects.all().order_by('-heure_cree')
    permission_classes = [IsAdminOrTemoignageUser]

    def get_serializer_class(self):
        if self.action == 'list':
            return TemoignageListSerializer
        return TemoignageSerializer

    def perform_create(self, serializer):
        """
        When a user (guest or authenticated) posts a testimonial,
        automatically assign the current user as the author.
        """
        serializer.save(auteur=self.request.user)


# --- Additional utility views ---
class CurrentUserView(APIView):
    """Get current user info"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class HealthCheckView(APIView):
    """Health check endpoint"""
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            'status': 'healthy',
            'timestamp': timezone.now(),
            'version': '1.0'
        })