from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PedidoCafeViewSet, ver_logs

router = DefaultRouter()
router.register(r'pedidos_cafe', PedidoCafeViewSet, basename='pedidos_cafe')

urlpatterns = [
    path('', include(router.urls)),
    path('logs/', ver_logs, name='ver_logs'),
]