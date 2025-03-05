from django.shortcuts import render
#import viewsets of CRUD
from rest_framework import viewsets, status
#import serializer
from .serializer import TaskSerializer, UserSerializer, ReceiptPostSerializer, ReceiptSerializer, AuthSerializer, RegisterSerializer
#import models
from .models import Sale, User, Receipt
#hachers
from django.contrib.auth.hashers import make_password, check_password

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


#logica
from collections import defaultdict
from uuid import uuid4



User = get_user_model()

# VIEW OF IAM


#SWAGGER UI
from drf_yasg.utils import swagger_auto_schema  # Importa swagger_auto_schema
from drf_yasg import openapi

class RegisterView(APIView):
    permission_classes = [AllowAny] #acceder sin permisos

    #decorador para mostrar el serializer en Swagger
    @swagger_auto_schema(
        request_body=RegisterSerializer,  # Indica el serializer que Swagger debe mostrar
        responses={201: openapi.Response('Usuario creado exitosamente')}
    )
    #metodo post para agregar usuario
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        
        if (serializer.is_valid()):
            #se toman los datos de la petición
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            first_name = serializer.validated_data.get('first_name', '')
            last_name = serializer.validated_data.get('last_name', '')

            #se filtra, si el username de la petición está en la base de datos
            if User.objects.filter(username=username).exists():
                return Response({'error': 'El usuario ya existe'}, status=status.HTTP_400_BAD_REQUEST)

            #de lo contrario, crea el usuario
            #@method create_user: crea el usuario y hashea la contraseña automáticamente
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)

            return Response({'message': 'Usuario creado exitosamente'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



            
class AuthView(APIView):

    permission_classes = [AllowAny]  # Permitir acceso sin autenticación

    #decorador para mostrar el serializer en Swagger
    @swagger_auto_schema(
        request_body=AuthSerializer,  # Indica el serializer que Swagger debe mostrar
        responses={201: openapi.Response('Usuario logueado exitosamente')}
    )

    def post(self, request, *args, **kwargs):
        serializer = AuthSerializer(data=request.data)

        if (serializer.is_valid()):
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']


            #autentica el usuario
            user = authenticate(username=username, password=password)
            
            #si lo encuentra:
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
    

"""
@param TokenRefreshView: clase de Django rest framework simple JWT,
usado para refrescar tokens de autenticación
"""
class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]
    
#permisos personalizados
from rest_framework.permissions import BasePermission

class IsSuperUser(BasePermission):
    """
    Permiso que permite acceso solo a usuarios con is_superuser=True
    """

    #metodo para verificar si el usuario tiene permisos (is_superuser=True)
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


#model viewset permite hacer las operaciones CRUD automáticamente
class TaskView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Sale.objects.all()

    # Añadir las clases de autenticación y permisos
    authentication_classes = [JWTAuthentication]  # Usar JWT para la autenticación
    
    def get_permissions(self):
        if self.action == 'list':  # GET (listar)
            return [IsAuthenticated()]  # Cualquiera con JWT puede acceder
        return [IsSuperUser()]  # Solo los usuarios con is_superuser=True pueden hacer POST, PUT, DELETE


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
        user = request.user #dato tomado de la petición en formato json del parametro "user"
        receipts = Receipt.objects.filter(user_id=user) #se filtra para ver si hay recibos vinculador al usuario


        if not receipts.exists():
            return Response({"message": "No hay recibos disponibles"}, status=status.HTTP_404_NOT_FOUND)

        #variable para almacenar y agrupar recibos
        grouped_receipts = defaultdict(list)

        #for each para la lista de recibos
        for receipt in receipts:
            #linker_str funciona como variables para guardar el dato "linker" del objeto que se esta iterando
            linker_str = str(receipt.linker)#se convierte en string 
            grouped_receipts[linker_str].append(ReceiptSerializer(receipt).data)

        return Response(grouped_receipts, status=status.HTTP_200_OK)
    
    def post(self, request):
        user = request.user

        # Agregamos el user automáticamente al request
        data = request.data.copy()

        if 'products' not in data or not isinstance(data['products'], list):
            return Response({"error": "Se requiere un array de productos"}, status=status.HTTP_400_BAD_REQUEST)

        #se genera un uuid4 y se transforma en string
        linker = str(uuid4())


        #como puede haber 1 o varios objetos a comprar al mismo tiempo, se mandan los productos en arrays
        
        for item in data['products']:
            item['user'] = user.id #todos los elementos tendran el user_id del User autenticado
            item['linker'] = linker #todos los elementos tendran el mismo uuid

        serializer = ReceiptPostSerializer(data=data['products'], many=True)    # Usamos el serializer de POST

        if serializer.is_valid():
            serializer.save(user=user, linker=linker) #se guarda los datos del campo user y linker
            #los otros campos ya estan llenos automáticamente (id: autogenerado, food_id: obtenido del request, created_at: autogenerado, quantity: obtenido del request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
