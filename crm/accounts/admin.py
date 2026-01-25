from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User, Role, UserRole, User2FASecret, User2FABackupCode


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Información personal", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permisos",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Fechas importantes", {"fields": ("last_login", "date_joined")}),
        (
            "SaaS / Seguridad",
            {
                "fields": (
                    "dealer",
                    "is_2fa_enabled",
                    "two_factor_confirmed_at",
                )
            },
        ),
    )

    list_display = (
        "username",
        "email",
        "dealer",
        "is_2fa_enabled",
        "is_active",
    )

    list_filter = (
        "dealer",
        "is_2fa_enabled",
        "is_active",
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "dealer")
    list_filter = ("dealer",)
    search_fields = ("name",)


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ("user", "role")
    list_filter = ("role",)


@admin.register(User2FASecret)
class User2FASecretAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "last_used_at")
    readonly_fields = ("created_at",)


@admin.register(User2FABackupCode)
class User2FABackupCodeAdmin(admin.ModelAdmin):
    list_display = ("user", "is_used", "created_at")
    list_filter = ("is_used",)
