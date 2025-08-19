# Atsweb/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

USER_ROLES = (
    ('guest', 'Guest'),
    ('admin', 'Admin'),
    ('user', 'User'),
)
PREDEFINED_ADMINS = [
    'admin1',
    'superadmin',
]


class User(AbstractUser):
    first_name = None  # remove first_name
    last_name = None   # remove last_name
    email = models.EmailField(unique=True)
    
    role = models.CharField(choices=USER_ROLES, max_length=20, default='guest')
    cv = models.FileField(upload_to='cv/', blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']  # email required for createsuperuser
    
    @property
    def is_predefined_admin(self):
        return self.username in PREDEFINED_ADMINS

    def __str__(self):
        return self.username


class Service(models.Model):
    titre = models.CharField(max_length=100)
    img = models.ImageField(upload_to='services/')
    description = models.TextField()
    heure_cree = models.DateTimeField(auto_now_add=True)
    heure_modifiee = models.DateTimeField(auto_now=True)
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.titre


class Technology(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Realisation(models.Model):
    titre = models.CharField(max_length=100)
    img = models.ImageField(upload_to='realisations/')
    description = models.TextField()
    client = models.CharField(max_length=100)
    technologies = models.ManyToManyField(Technology)
    heure_cree = models.DateTimeField(auto_now_add=True)
    heure_modifiee = models.DateTimeField(auto_now=True)
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.titre


class Article(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
    heure_cree = models.DateTimeField(auto_now_add=True)
    heure_modifiee = models.DateTimeField(auto_now=True)
    auteur = models.CharField(max_length=100)

    def __str__(self):
        return self.titre


class Temoignage(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    img = models.ImageField(upload_to='temoignages/', blank=True)
    heure_cree = models.DateTimeField(auto_now_add=True)
    heure_modifiee = models.DateTimeField(auto_now=True)
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nom
