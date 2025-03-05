from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
import uuid



"""
Entidad Sale:

-descripción: entidad que describe al objeto a vender

@param description: nombre del objeto a vender

@param unitPrice: precio unitario

@para image_url: direccion de imagen en string



"""

class Sale(models.Model):

    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100, blank=False, null=False)
    unitPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    image_url = models.CharField(max_length=250, blank=False, null=False)
    def __str__(self):
        return self.description

"""
@AbstractUser: es el modelo base de Django para usuarios 

de por si "first_name" y "last_name" viene en el modelo base
pero se agregró para editar las caracteristicas como el tamaño maximo, etc

"""
class User(AbstractUser):
    
    first_name = models.CharField(max_length=50, default=' ')
    last_name = models.CharField(max_length=50, default=' ')

    def __str__(self):
        return self.username


"""
Entidad Receipt

-descripción: entidad encargada de unir los recibos de determinados objetos
para cada usuario

@param quantity: cantidad
@param linker: uuid4 encargado de linkear distintos datos en un solo recibo
@param food: llave foranea de objeto "Sales"
@param user: llave foranea de objeto "User"
@created_at: dato guardado en formato de fecha


"""



class Receipt(models.Model):
    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField(blank=False, null=False)
    linker = models.UUIDField(default=uuid.uuid4, editable=False)
    food = models.ForeignKey(Sale, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
