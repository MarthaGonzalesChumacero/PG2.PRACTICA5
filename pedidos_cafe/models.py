from django.db import models
from django.core.exceptions import ValidationError

class PedidoCafe(models.Model):
    BASE_CHOICES = [
        ("espresso", "Espresso"),
        ("americano", "Americano"),
        ("latte", "Latte"),
    ]

    TAMANIO_CHOICES = [
        ("pequenio", "Pequeño"),
        ("mediano", "Mediano"),
        ("grande", "Grande"),
    ]

    INGREDIENTES_VALIDOS = {
        "leche", "azúcar", "canela", "chocolate",
        "vainilla", "caramelo", "miel"
    }

    cliente = models.CharField(max_length=100)
    tipo_base = models.CharField(max_length=20, choices=BASE_CHOICES)
    ingredientes = models.JSONField(default=list)
    tamanio = models.CharField(max_length=10, choices=TAMANIO_CHOICES)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cliente} - {self.tipo_base} ({self.tamanio})"

    def clean(self):
        if not isinstance(self.ingredientes, list):
            raise ValidationError({"ingredientes": "Los ingredientes deben estar en formato de lista."})
        
        for ing in self.ingredientes:
            if ing not in self.INGREDIENTES_VALIDOS:
                raise ValidationError({"ingredientes": f"Ingrediente inválido: '{ing}' no está permitido."})
