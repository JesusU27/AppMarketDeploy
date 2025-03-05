from rest_framework import serializers
from .models import Sale, User, Receipt

#change the python language to json language

#serializers.Serializer	-> Se usa cuando queremos control total sobre los campos.
#serializers.ModelSerializer ->	Serializa modelos de Django automáticamente.


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        #nombre de modelo que se quiere trabajar
        model = Sale
        #fields with which we want to work
        #fields = ('description', 'unitPrice')

        #if we want to work with all fields
        fields = '__all__' 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ReceiptSerializer(serializers.ModelSerializer):
    food = TaskSerializer()

    class Meta:
        model = Receipt
        fields = ['id', 'quantity', 'linker', 'food', 'user', 'created_at']

#Serializer personalizado solo para el POST del endpoint "Receipt"
    
class ReceiptPostSerializer(serializers.ModelSerializer):
    """
    Serializer para la creación de recibos (Receipt).

    Atributos:
        food_id (serializers.PrimaryKeyRelatedField):
            - Representa una relación con el modelo Sale.
            - Se almacena como la clave primaria (ID) de un objeto Sale.
            - En la API, el campo se llama `food_id`, pero internamente 
              está vinculado con el atributo `food` en el modelo Receipt.
            - Solo acepta valores existentes en la tabla Sale.
    """
    food_id = serializers.PrimaryKeyRelatedField(
        queryset=Sale.objects.all(), source='food'
    )

    class Meta:
        model = Receipt
        fields = ['id', 'quantity', 'food_id', 'user', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']


#serializer para el post de autenticación
class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30, write_only=True)
    
#serializer para el post de registro de usuarios
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30, write_only=True)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    
        