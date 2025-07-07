from rest_framework import serializers
from pedidos_cafe.models import PedidoCafe
from pedidos_cafe.factory import CafeFactory
from pedidos_cafe.builder import CafePersonalizadoBuilder, CafeDirector
from api_patrones.logger import Logger

class PedidoCafeSerializer(serializers.ModelSerializer):
    precio_total = serializers.SerializerMethodField()
    ingredientes_finales = serializers.SerializerMethodField()

    class Meta:
        model = PedidoCafe
        fields = [
            "id",
            "cliente",
            "tipo_base",
            "ingredientes",
            "tamanio",
            "fecha",
            "precio_total",
            "ingredientes_finales",
        ]

    def validate_ingredientes(self, value):
        ingredientes_validos = {
            "leche", "azúcar", "canela",
            "chocolate", "vainilla", "caramelo", "miel"
        }
        if not isinstance(value, list):
            raise serializers.ValidationError("Los ingredientes deben ser una lista.")
        
        errores = []
        for ing in value:
            if ing not in ingredientes_validos:
                errores.append(f"Ingrediente inválido: {ing}")
        
        if errores:
            raise serializers.ValidationError(errores)
        
        return value

    def get_precio_total(self, obj):
        cafe = CafeFactory.obtener_base(obj.tipo_base)
        builder = CafePersonalizadoBuilder(cafe)
        director = CafeDirector(builder)
        director.construir(obj.ingredientes, obj.tamanio)
        Logger().registrar(f"Se registró el cálculo del precio para el pedido {obj.id}")
        return builder.obtener_precio()

    def get_ingredientes_finales(self, obj):
        cafe = CafeFactory.obtener_base(obj.tipo_base)
        builder = CafePersonalizadoBuilder(cafe)
        director = CafeDirector(builder)
        director.construir(obj.ingredientes, obj.tamanio)
        Logger().registrar(
            f"Se registró la obtención de ingredientes finales para el pedido {obj.id}"
        )
        return builder.obtener_ingredientes_finales()    