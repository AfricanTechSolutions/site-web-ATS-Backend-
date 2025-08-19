from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import check_password

from .models import Service, Technology, Realisation, Article, Temoignage

User = get_user_model()


# --- User Serializers ---
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "password", "role", "cv", 
            "ip_address", "is_active", "is_verified", "date_joined"
        ]
        read_only_fields = ["role", "ip_address", "is_verified", "date_joined"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


# User list serializer for admin dashboard (without sensitive data)
class UserListSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "is_active", "is_verified", "date_joined", "status"]
    
    def get_status(self, obj):
        return "Actif" if obj.is_active else "Suspendu"


# --- Login Serializer ---
class MyTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = User.objects.filter(email=email).first()
        if not user or not check_password(password, user.password):
            raise serializers.ValidationError("Email ou mot de passe incorrect")

        if not user.is_active:
            raise serializers.ValidationError("Compte suspendu")

        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
        }


# --- Content Serializers ---
class ServiceSerializer(serializers.ModelSerializer):
    auteur_username = serializers.CharField(source='auteur.username', read_only=True)
    
    class Meta:
        model = Service
        fields = "__all__"
    
    def create(self, validated_data):
        # Auto-assign current user as author if not provided
        if 'auteur' not in validated_data and self.context.get('request'):
            validated_data['auteur'] = self.context['request'].user
        return super().create(validated_data)


class ServiceListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing services in dashboard"""
    auteur_username = serializers.CharField(source='auteur.username', read_only=True)
    
    class Meta:
        model = Service
        fields = ["id", "titre", "description", "auteur_username", "heure_cree"]


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = "__all__"


class RealisationSerializer(serializers.ModelSerializer):
    technologies_names = serializers.StringRelatedField(source='technologies', many=True, read_only=True)
    technology_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Technology.objects.all(), 
        write_only=True, source='technologies', required=False
    )
    auteur_username = serializers.CharField(source='auteur.username', read_only=True)
    
    class Meta:
        model = Realisation
        fields = "__all__"
        extra_kwargs = {
            'technologies': {'read_only': True}
        }
    
    def create(self, validated_data):
        if 'auteur' not in validated_data and self.context.get('request'):
            validated_data['auteur'] = self.context['request'].user
        
        technologies = validated_data.pop('technologies', [])
        realisation = Realisation.objects.create(**validated_data)
        realisation.technologies.set(technologies)
        return realisation
    
    def update(self, instance, validated_data):
        technologies = validated_data.pop('technologies', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if technologies is not None:
            instance.technologies.set(technologies)
        
        return instance


class RealisationListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing portfolio items in dashboard"""
    technologies_names = serializers.StringRelatedField(source='technologies', many=True, read_only=True)
    auteur_username = serializers.CharField(source='auteur.username', read_only=True)
    
    class Meta:
        model = Realisation
        fields = ["id", "titre", "client", "technologies_names", "auteur_username", "heure_cree"]


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"


class ArticleListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing articles in dashboard"""
    class Meta:
        model = Article
        fields = ["id", "titre", "auteur", "heure_cree"]


class TemoignageSerializer(serializers.ModelSerializer):
    auteur_username = serializers.CharField(source='auteur.username', read_only=True)
    
    class Meta:
        model = Temoignage
        fields = "__all__"
    
    def create(self, validated_data):
        if 'auteur' not in validated_data and self.context.get('request'):
            validated_data['auteur'] = self.context['request'].user
        return super().create(validated_data)


class TemoignageListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing testimonials in dashboard"""
    auteur_username = serializers.CharField(source='auteur.username', read_only=True)
    
    class Meta:
        model = Temoignage
        fields = ["id", "nom", "auteur_username", "heure_cree"]


# --- Dashboard Stats Serializer ---
class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for dashboard statistics"""
    total_users = serializers.IntegerField()
    total_articles = serializers.IntegerField()
    total_services = serializers.IntegerField()
    total_realisations = serializers.IntegerField()
    total_temoignages = serializers.IntegerField()
    recent_users = serializers.IntegerField()  # users registered in last 30 days