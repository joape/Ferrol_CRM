from typing import TYPE_CHECKING

from django.db import models
from core.models import BaseModel
from django.db.models import Sum
from decimal import Decimal


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
    
class Vehicle(BaseModel):
    """
    Vehículo perteneciente a una automotora.
    Puede ser propio o en consignación.
    """

    class Currency(models.TextChoices):
        UYU = "UYU", "Pesos Uruguayos"
        USD = "USD", "Dólares"

    class Ownership(models.TextChoices):
        DEALER = "DEALER", "Propio de la automotora"
        CONSIGNMENT = "CONSIGNMENT", "En consignación"

    dealer = models.ForeignKey(
        Dealer,
        on_delete=models.CASCADE,
        related_name="vehicles"
    )

    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()

    ownership_type = models.CharField(
        max_length=20,
        choices=Ownership.choices,
        default=Ownership.DEALER
    )

    purchase_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Precio de compra o valor base del vehículo"
    )

    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.USD
    )

    is_active = models.BooleanField(default=True)
    

    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.brand} {self.model} ({self.year})"
    
    def total_services_cost(self) -> Decimal:
        """
        Total de servicios PAGADOS POR LA AUTOMOTORA.
        Los servicios pagados por el dueño NO cuentan.
        """
        total = self.services.filter(
            payer=VehicleService.Payer.DEALER,
            is_active=True
        ).aggregate(
            total=Sum("amount")
        )["total"]

        return total or Decimal("0.00")

    def total_cost(self) -> Decimal:
        """
        Costo total real del vehículo para la automotora.
        Compra + servicios propios.
        """
        return (self.purchase_price or Decimal("0.00")) + self.total_services_cost()

    def suggested_sale_price(self) -> Decimal:
        """
        Precio sugerido según margen por defecto del dealer.
        """
        margin = self.dealer.default_margin_percentage or Decimal("0.00")
        factor = Decimal("1") + (margin / Decimal("100"))
        return self.total_cost() * factor

class VehicleService(BaseModel):
    """
    Servicio / gasto realizado a un vehículo.
    Puede ser pagado por la automotora o por el dueño (consignación).
    """

    class Payer(models.TextChoices):
        DEALER = "DEALER", "Automotora"
        OWNER = "OWNER", "Dueño del vehículo"

    vehicle = models.ForeignKey(
        "dealers.Vehicle",
        on_delete=models.CASCADE,
        related_name="services"
    )

    description = models.CharField(
        max_length=255,
        help_text="Ej: Cambio de aceite, Chapa y pintura, Lavado, Repuesto"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Costo del servicio"
    )

    payer = models.CharField(
        max_length=10,
        choices=Payer.choices,
        default=Payer.DEALER
    )

    service_date = models.DateField()

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Vehicle Service"
        verbose_name_plural = "Vehicle Services"
        ordering = ["-service_date"]

    def __str__(self) -> str:
        return f"{self.vehicle} - {self.description}"     
    