from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Service, Technology, Realisation, Article, Temoignage

# Enregistrement des autres modèles
admin.site.register(Service)
admin.site.register(Technology)
admin.site.register(Realisation)
admin.site.register(Article)
admin.site.register(Temoignage)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['email', 'role', 'is_active', 'is_verified']

    # Organisation des champs dans la page de détail d'un utilisateur
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('cv', 'username')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'role', 'is_verified', 'groups', 'user_permissions')
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('IP Tracking'), {'fields': ('ip_address',)}),
    )

    # Champs affichés lors de la création d'un nouvel utilisateur dans l'admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role'),
        }),
    )

    search_fields = ('email',)
