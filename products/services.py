from decimal import Decimal
from django.shortcuts import get_object_or_404
from .models import Product


class EstrategiaDescuento:
    def calcular(self, precio):
        raise NotImplementedError


class DescuentoElectronica(EstrategiaDescuento):
    def calcular(self, precio):
        return precio * Decimal('0.90')


class DescuentoRopa(EstrategiaDescuento):
    def calcular(self, precio):
        return precio * Decimal('0.80')


class SinDescuento(EstrategiaDescuento):
    def calcular(self, precio):
        return precio


def obtener_estrategia(categoria_nombre):
    estrategias = {
        'Electronica': DescuentoElectronica(),
        'Ropa': DescuentoRopa(),
    }
    return estrategias.get(categoria_nombre, SinDescuento())


def calcular_precio_final(pk):
    producto = get_object_or_404(
        Product.objects.select_related('category'), pk=pk)
    estrategia = obtener_estrategia(producto.category.name)
    precio_final = estrategia.calcular(producto.price)
    return {
        'producto': producto.name,
        'categoria': producto.category.name,
        'precio_original': str(producto.price),
        'precio_final': str(precio_final.quantize(Decimal('0.01'))),
    }
