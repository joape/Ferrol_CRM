from django.db import models
from core.models import BaseModel


class Dealer(BaseModel):
    """
    Representa una automotora (tenant del SaaS).
    Todos los datos del sistema cuelgan de un Dealer.
    """
    name = models.CharField(max_length=255)
    rut = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=30)
    whatsapp = models.CharField(max_length=30)
    email = models.EmailField()
    default_margin_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Margen de ganancia por defecto (%)"
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Dealer"
        verbose_name_plural = "Dealers"

    def __str__(self) -> str:
        return self.name
