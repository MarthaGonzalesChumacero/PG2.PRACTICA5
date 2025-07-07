from .singleton import LoggerSingleton  #  Asegurate de que esto esté arriba

class CafePersonalizadoBuilder:
    def __init__(self, cafe_base):
        self.base = cafe_base
        self.precio = cafe_base.precio_base()
        self.ingredientes = list(cafe_base.obtener_ingredientes_base())
        LoggerSingleton().registrar(f"Inicio construcción: base={self.base.__class__.__name__}")

    def agregar_ingrediente(self, ingrediente):
        precios = {
            "canela": 1,
            "chocolate": 2,
            "vainilla": 1.5,
            "azucar": 0.5,
            "leche extra": 2,
        }
        if ingrediente not in precios:
            raise ValueError(f"Ingrediente '{ingrediente}' no válido o no disponible.")
        self.ingredientes.append(ingrediente)
        self.precio += precios.get(ingrediente, 0)
        LoggerSingleton().registrar(f"Ingrediente agregado: {ingrediente} — subtotal={self.precio}")

    def ajustar_tamanio(self, tamaño):
        if tamaño == "mediano":
            self.precio *= 1.25
        elif tamaño == "grande":
            self.precio *= 1.5
        LoggerSingleton().registrar(f"Tamaño ajustado a '{tamaño}' — precio actualizado={self.precio}")

    def obtener_precio(self):
        total = round(self.precio, 2)
        LoggerSingleton().registrar(
            f"Pedido finalizado: ingredientes={self.ingredientes}, precio={total}"
        )
        return total

    def obtener_ingredientes_finales(self):
        return self.ingredientes


class CafeDirector:
    def __init__(self, builder):
        self.builder = builder

    def construir(self, ingredientes, tamaño):
        for i in ingredientes:
            self.builder.agregar_ingrediente(i)
        self.builder.ajustar_tamanio(tamaño)

    def construir_paquete_1(self):
        self.builder.agregar_ingrediente("canela")
        self.builder.agregar_ingrediente("chocolate")
        self.builder.ajustar_tamanio("mediano")

    def construir_paquete_2(self):
        self.builder.agregar_ingrediente("vainilla")
        self.builder.agregar_ingrediente("azucar")
        self.builder.ajustar_tamanio("grande")

    def construir_paquete_3(self):
        self.builder.agregar_ingrediente("leche extra")
        self.builder.agregar_ingrediente("canela")
        self.builder.ajustar_tamanio("pequeño")