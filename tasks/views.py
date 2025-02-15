from django.shortcuts import render
#import viewsets of CRUD
from rest_framework import viewsets, status
#import serializer
from .serializer import TaskSerializer, UserSerializer, ReceiptPostSerializer, ReceiptSerializer, AuthSerializer, RegisterSerializer
#import models
from .models import Sale, User, Receipt

from django.contrib.auth.hashers import make_password, check_password

# para hacer vistas "swagger" de la API REST de un metodo en especifico
from rest_framework.views import APIView

from rest_framework.decorators import action


#JWT
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenRefreshView


#response
from rest_framework.response import Response
from collections import defaultdict
from uuid import uuid4



User = get_user_model()

# VIEW OF IAM

class RegisterView(APIView):
    permission_classes = [AllowAny]

     #post method register an User
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)

        if (serializer.is_valid()):
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            first_name = serializer.validated_data.get('first_name', '')
            last_name = serializer.validated_data.get('last_name', '')

            if User.objects.filter(username=username).exists():
                return Response({'error': 'El usuario ya existe'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)

            return Response({'message': 'Usuario creado exitosamente'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



            
class AuthView(APIView):

    permission_classes = [AllowAny]  # Permitir acceso sin autenticación

    def post(self, request, *args, **kwargs):
        serializer = AuthSerializer(data=request.data)

        if (serializer.is_valid()):
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)
            
            if user is not None:
                # Generar el JWT (RefreshToken y AccessToken)
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token

                # Devuelve ambos tokens
                return Response({
                    'refresh': str(refresh),  # El token de actualización
                    'access': str(access_token),  # El token de acceso
                    'username': user.username
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Credenciales inválidas'
                }, status=status.HTTP_400_BAD_REQUEST)

            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]
    
# Create your views here.

class TaskView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Sale.objects.all()

    # Añadir las clases de autenticación y permisos
    authentication_classes = [JWTAuthentication]  # Usar JWT para la autenticación
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder


class UserView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response({
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name

        })



class ReceiptView(APIView):
    
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    def get(self, request):
        user = request.user
        receipts = Receipt.objects.filter(user_id=user)

        if not receipts.exists():
            return Response({"message": "No hay recibos disponibles"}, status=status.HTTP_404_NOT_FOUND)

        grouped_receipts = defaultdict(list)

        for receipt in receipts:
            linker_str = str(receipt.linker) 
            grouped_receipts[linker_str].append(ReceiptSerializer(receipt).data)

        return Response(grouped_receipts, status=status.HTTP_200_OK)
    
    def post(self, request):
        user = request.user

        # Agregamos el user automáticamente al request
        data = request.data.copy()

        if 'products' not in data or not isinstance(data['products'], list):
            return Response({"error": "Se requiere un array de productos"}, status=status.HTTP_400_BAD_REQUEST)
    
        linker = str(uuid4())

        for item in data['products']:
            item['user'] = user.id
            item['linker'] = linker


        serializer = ReceiptPostSerializer(data=data['products'], many=True)    # Usamos el serializer de POST

        if serializer.is_valid():
            serializer.save(user=user, linker=linker)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
