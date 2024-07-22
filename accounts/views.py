from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializer import UserSerializer, UserOutputSerializer, GroupSerializer, UserProfilePhotoSerializer, UserInputSerializer
from rest_framework import status, generics, filters
from .models import User

import qrcode
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated 
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth.models import Group
from django.utils import timezone
import json
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
import random
from django.core.mail import send_mail

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        # Add custom claims
        token['nombre'] = user.nombre
        token['groups'] = [group.name for group in user.groups.all()]
        # ...

        return token
    
class ValidatePasswordView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordValidationSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=request.user.username, 
                password=serializer.validated_data['password']
            )
            if user is not None:
                return Response({'detail': 'Password is valid'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdatePasswordView(APIView):
    def post(self, request, pk):
        user = User.objects.get(pk=pk)
        print(request.data)
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if not user.check_password(old_password):
            return Response({'message': 'La contraseña actual es incorrecta'}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({'message': 'La confimacion y la nueva contraseña no son iguales'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'message': 'Contaseña actualizada!'}, status=status.HTTP_200_OK)
    
class QRCodeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        token = AccessToken.for_user(request.user) 
        url = 'http://localhost:5174/Inscripci%C3%B3n/?auth='  + str(token) 
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        response = HttpResponse(content_type='image/png')
        img.save(response, 'PNG')

        return  response

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def reset_passkey(request, pk):  
    try:
        user = User.objects.get(pk=pk) 
    except User.DoesNotExist:
         return Response({"error": "El usuario no existe"}, status=status.HTTP_404_NOT_FOUND)
    
    # Generate a random six-digit password
    password = str(random.randint(100000, 999999)) 

    # Send the password to the user's email
    subject = 'Contraseña temporal'
    message = f'Tu contraseña temporal es: {password}' 
    to_email = user.email 
    
    try:
        send_mail(subject, message, None, [to_email], fail_silently=False)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #saving
    user.set_password(password)
    user.save()
    
    return Response({'message':'Clave de Acceso Cambiada'}, status=status.HTTP_201_CREATED)
    
class UsersListCreateView(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = User.objects.all().order_by("-is_active")
    serializer_class = UserSerializer 
    pagination_class = None

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserOutputSerializer
        else:
            return self.serializer_class

    def create(self, request, *args, **kwargs):
        user_data = request.data.get("user")  
        serializer = UserInputSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)

        # Generate a random six-digit password
        password = str(random.randint(100000, 999999)) 
        user = serializer.save() 

        # Send the password to the user's email
        subject = 'Contraseña temporal'
        message = f'Tu contraseña temporal es: {password}' 
        to_email = user.email 
        
        try:
            send_mail(subject, message, None, [to_email], fail_silently=False)
        except Exception as e:
                    return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
        #saving
        user.set_password(password)
        user.save()

        groups_data = request.data.pop('groups')
        for group_data in groups_data: 
            group = Group.objects.get(id=group_data)
            user.groups.add(group)  
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers) 

class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer 
    pagination_class = None
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserOutputSerializer
        else:
            return self.serializer_class
        
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        user_data = request.data.get("user") 
        print("userdata", user_data)
        print("user", user)
        serializer = self.get_serializer(user, data=user_data, partial=True)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer) 
        if user_data.get('password'):
            user.set_password(user_data['password'])
            user.save() 
        groups_data = request.data.pop('groups') or None
        if groups_data is not None:
            user.groups.clear()
            for group_data in groups_data: 
                group = Group.objects.get(id=group_data)
                user.groups.add(group) 
        return Response(serializer.data, status=status.HTTP_201_CREATED )

class UpdateUserProfilePhotoView(APIView):
    # permission_classes = (IsAuthenticated,)
    parser_class = (MultiPartParser, FormParser)

    def put(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserProfilePhotoSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GroupDetailView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer 
    pagination_class = None