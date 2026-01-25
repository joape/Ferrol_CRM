from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone

from core.models import BaseModel
from dealers.models import Dealer


class User(AbstractUser, BaseModel):
    """
    Usuario del sistema (Custom User).
    Siempre pertenece a un Dealer (multi-tenant SaaS).
    """

    dealer = models.ForeignKey(
        Dealer,
        on_delete=models.CASCADE,
        related_name="users",
        null=True,
        blank=True,
        help_text="Dealer al que pertenece el usuario (NULL solo para bootstrap)"
    )

    # 🔐 Sobrescribimos estos campos para evitar conflictos
    # con auth.User (E304 reverse accessor clash)
    groups = models.ManyToManyField(
        Group,
        related_name="accounts_user_set",
        blank=True,
        help_text="Grupos de permisos (Django auth)"
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="accounts_user_permissions_set",
        blank=True,
        help_text="Permisos específicos del usuario"
    )

    # 2FA
    is_2fa_enabled = models.BooleanField(default=False)
    two_factor_confirmed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def has_2fa_enabled(self) -> bool:
        return self.is_2fa_enabled is True

    def confirm_2fa(self) -> None:
        """
        Marca el 2FA como confirmado.
        """
        self.is_2fa_enabled = True
        self.two_factor_confirmed_at = timezone.now()
        self.save(update_fields=["is_2fa_enabled", "two_factor_confirmed_at"])

    def __str__(self) -> str:
        dealer_name = self.dealer.name if self.dealer else "NO-DEALER"
        return f"{self.username} ({dealer_name})"


# ======================================================
# ROLES (RBAC por automotora)
# ======================================================

class Role(BaseModel):
    """
    Rol funcional dentro de una automotora.
    Ejemplos:
    - OWNER
    - ADMIN
    - SALES
    - ACCOUNTING
    - VIEWER
    """

    name = models.CharField(
        max_length=50,
        help_text="Nombre del rol (ej: ADMIN, SALES)"
    )

    description = models.TextField(
        blank=True
    )

    dealer = models.ForeignKey(
        Dealer,
        on_delete=models.CASCADE,
        related_name="roles"
    )

    class Meta:
        unique_together = ("dealer", "name")
        verbose_name = "Role"
        verbose_name_plural = "Roles"

    def __str__(self) -> str:
        return f"{self.name} ({self.dealer.name})"


class UserRole(BaseModel):
    """
    Relación N:M entre usuarios y roles.
    Un usuario puede tener múltiples roles.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_roles"
    )

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name="role_users"
    )

    class Meta:
        unique_together = ("user", "role")
        verbose_name = "User Role"
        verbose_name_plural = "User Roles"

    def __str__(self) -> str:
        return f"{self.user.username} -> {self.role.name}"


# ======================================================
# 2FA (Two-Factor Authentication)
# ======================================================

class User2FASecret(BaseModel):
    """
    Secreto TOTP del usuario.
    El valor debe almacenarse cifrado (más adelante).
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="two_factor_secret"
    )

    secret = models.CharField(
        max_length=255,
        help_text="Secreto TOTP (base32 / cifrado)"
    )

    last_used_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self) -> str:
        return f"2FA Secret for {self.user.username}"


class User2FABackupCode(BaseModel):
    """
    Códigos de recuperación 2FA.
    Se almacenan como hash y son de un solo uso.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="backup_codes"
    )

    code_hash = models.CharField(
        max_length=255,
        help_text="Hash del código de recuperación"
    )

    is_used = models.BooleanField(default=False)

    def mark_as_used(self) -> None:
        """
        Marca el código como utilizado.
        """
        self.is_used = True
        self.save(update_fields=["is_used"])

    def __str__(self) -> str:
        status = "USED" if self.is_used else "ACTIVE"
        return f"BackupCode {status} for {self.user.username}"
