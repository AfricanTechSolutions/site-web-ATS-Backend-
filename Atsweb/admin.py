from django.contrib import admin
from .models import User, Service, Technology, Realisation, Article, Temoignage

admin.site.register(User)
admin.site.register(Service)
admin.site.register(Technology)
admin.site.register(Realisation)
admin.site.register(Article)
admin.site.register(Temoignage)
