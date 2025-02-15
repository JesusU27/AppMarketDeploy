from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
import uuid


class Sale(models.Model):

    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100, blank=False, null=False)
    unitPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    image_url = models.CharField(max_length=250, blank=False, null=False)
    def __str__(self):
        return self.description

class User(AbstractUser):
    
    first_name = models.CharField(max_length=50, default=' ')
    last_name = models.CharField(max_length=50, default=' ')

    def __str__(self):
        return self.username


class Receipt(models.Model):
    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField(blank=False, null=False)
    linker = models.UUIDField(default=uuid.uuid4, editable=False)
    food = models.ForeignKey(Sale, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
