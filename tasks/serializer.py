from rest_framework import serializers
from .models import Sale, User, Receipt

#change the python language to json language

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        #name of entity with which we want to work
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

class ReceiptPostSerializer(serializers.ModelSerializer):
    food_id = serializers.PrimaryKeyRelatedField(
        queryset=Sale.objects.all(), source='food'
    )

    class Meta:
        model = Receipt
        fields = ['id', 'quantity', 'food_id', 'user', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30, write_only=True)
    
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30, write_only=True)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    
        