from django.db import models

# Choix pour le rôle utilisateur
USER_ROLES = (
    ('admin', 'Admin'),
    ('user', 'Utilisateur'),
    ('guest', 'Visiteur')
)

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(choices=USER_ROLES, max_length=20, default='guest', editable=False)
    cv = models.FileField(upload_to='cv/')
    ip_address = models.GenericIPAddressField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    titre = models.CharField(max_length=100)
    img = models.ImageField(upload_to='services/')
    description = models.TextField()
    heure_cree = models.DateTimeField(auto_now_add=True)
    heure_modifiee = models.DateTimeField(auto_now=True)
    auteur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

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
    auteur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

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
    auteur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nom
