from rest_framework import serializers
from .models import User, Service, Technology, Realisation, Article, Temoignage

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = '__all__'

class RealisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Realisation
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

class TemoignageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temoignage
        fields = '__all__'
