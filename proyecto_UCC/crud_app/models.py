from django.db import models
from django.contrib.auth.models import User

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    creado_el = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)  # Agrega este campo
    categoria = models.CharField(max_length=50, default='sin categoria')
    stock = models.PositiveIntegerField(default=0)
    marca = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.nombre
    
class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through='CarritoProducto')
    completado = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Carrito de {self.usuario.username}"


class CarritoProducto(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.producto.nombre} en el carrito de {self.carrito.usuario.username}"
    
class Compra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15)
    pais = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    direccion = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    productos = models.ManyToManyField(Producto, through='CompraProducto')

    def __str__(self):
        return f'Compra de {self.usuario.username} en {self.fecha_compra}'

class CompraProducto(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.producto.nombre} x {self.cantidad}'
    
    
# Create your models here.