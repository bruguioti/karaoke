from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Cantor, Banner, CustomUser, Promocao

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('cpf', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('cpf',)
    ordering = ('cpf',)
    fieldsets = (
        (None, {'fields': ('cpf', 'password')}),
        (_('Permissões'), {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Datas importantes'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('cpf', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

admin.site.register(Cantor)
admin.site.register(Banner)
admin.site.register(Promocao)
