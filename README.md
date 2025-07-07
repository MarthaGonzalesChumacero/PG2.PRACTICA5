# PG2.PRACTICA5
# Práctica 5

## PEDIDOS DE CAFE - PATRONES DE DISEÑO

Este proyecto es una API hecha con Django y Django REST Framework que sirve para pedir café de forma personalizada. Los usuarios pueden elegir el tipo de café, el tamaño y agregar ingredientes extra. El sistema se encarga de calcular el precio total automáticamente y confirmar que todo lo que se pidió tenga sentido. Toda esta lógica está bien organizada usando patrones de diseño, lo que hace que el proyecto sea fácil de mantener y escalar. También se puede manejar desde el panel de administración de Django, así que es útil tanto para el usuario como para quien gestiona los pedidos.

### Pasos para a seguir

1. Configurar e instalar dependencias

   ```bash
   .requirements.txt
   django==5.2
   django-extensions==4.1
   djangorestframework==3.16.0
   .gitignore, manage.py,
   python -m venv env
   .\env\Scripts\activate  # En Windows
   # source env/bin/activate  # En Linux/Mac
   pip install -r requirements.txt
   ```
2. Crear proyecto Django y migraciones

    ```bash
    django-admin startproject api_patrones .
    python manage.py startapp pedidos_cafe
    pip install djangorestframework
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
    ```

3.  Configurar la base de datos en settings.py para usar SQLite.

    ```python
    INSTALLED_APPS = [
    ...
    'django_extensions',
    'rest_framework',
    'pedidos_cafe',
    ]
    ```
4. Crear y/o configurar modelos.py, serializers.py, views.py, urls.py

### EXPLICACION PATRONES DE DISEÑO

## 1. Factory
Se utilizo este patron Factory para encapsular la creacion de distintas bases de cafe (Americano,Expresso, Latte).
El codigo esta implementado en el archivo `pedidos_cafe/factory.py`.

```python
from pedidos_cafe.base import Espresso, Americano, Latte
class CafeFactory:
    @staticmethod
    def obtener_base(tipo):
        if tipo == "espresso":
            cafe = Espresso()
        elif tipo == "americano":
            cafe = Americano()
        elif tipo == "latte":
            cafe = Latte()
        else:
            raise ValueError("Tipo de café no válido")

        cafe.inicializar()
        return cafe
El uso del patron se evidencia en serializers.py
```
## 2. Builder

Se utilizo este patron Builder ya que es el encargado de construir el pedido personalizado, separando el proceso de armado del café de su presentación final. Ideal para mantener una arquitectura limpia y flexible.
El codigo esta implementado en el archivo `pedidos_cafe/builder.py`.
````python
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
````
## 3. SINGLETON
Este patrón asegura que solo exista una instancia compartida de la clase Logger a lo largo de toda la aplicación, permitiendo registrar eventos importantes como el cálculo de precios o la composición final del pedido de café.
El codigo esta implementado en el archivo `api_patrones/logger.py`.

````python
class Logger:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.logs = []
        return cls._instancia

    def registrar(self, mensaje):
        self.logs.append(mensaje)

    def obtener_logs(self):
        return self.logs
````
### 6. VALIDACION DE INGREDIENTES EXTRA EN EL REGISTRO DE PEDIDOS
Se realizó la implementacion para `admin y API`, asegurandonos que los ingredientes seleccionados sean válidos.

Validacion de ingredientes dentro de `pedidos_cafe/models.py dsede el panel de administracion Django`.
````python
def clean(self):
    validos = {"leche", "azúcar", "canela", "chocolate", "vainilla", "caramelo", "miel"}
    if not isinstance(self.ingredientes, list):
        raise ValidationError({"ingredientes": "deben ser una lista."})
    for ing in self.ingredientes:
        if ing not in validos:
            raise ValidationError({"ingredientes": f"ingrediente inválido: {ing}"})
````
Validación de ingredientes dentro de `pedidos_cafe/serializers.py`
````python
def validate_ingredientes(self, value):
    ingredientes_validos = {
        "leche", "azúcar", "canela", "chocolate", "vainilla", "caramelo", "miel"
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
````
### 7. PROBANDO
## Acceder al panel de administración

### Sitio panel de admin http://127.0.0.1:8000/admin/pedidos_cafe/pedidocafe/add/

![Admin](Imagenes/admin.png)

____

### Sitio API http://127.0.0.1:8000/api/pedidos_cafe/
![Api](Imagenes/api.png)