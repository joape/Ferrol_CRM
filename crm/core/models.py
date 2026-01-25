from django.db import models

class BaseModel(models.Model):
    """
    Modelo base abstracto.
    Agrega timestamps estándar a todos los modelos del sistema.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

