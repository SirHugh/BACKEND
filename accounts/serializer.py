from rest_framework import serializers
from rest_framework.validators import ValidationError 
from .models import User
from django.contrib.auth.models import  Group 


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class PasswordValidationSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

class UserSerializer(serializers.ModelSerializer):  
    cedula = serializers.CharField(required=False, allow_null=True)
    telefono = serializers.CharField(required=False, allow_null=True)
    direccion = serializers.CharField(required=False, allow_null=True)
    
    class Meta(object):
        model = User 
        fields = [ 'id', 'email', 'nombre', 'apellido', 'is_active', 'telefono', 'direccion', 'cedula']
    
    def validate(self, attrs):
        user_id = self.context['view'].kwargs['pk'] if 'pk' in self.context['view'].kwargs else None
        
        if not user_id:
            if  User.objects.filter(email=attrs['email']).exists():
                raise ValidationError('El correo ya se encuentra en uso!')
        
        return super().validate(attrs)


class UserOutputSerializer(serializers.ModelSerializer): 
    password = serializers.CharField(write_only=True) 
    
    class Meta(object):
            model = User 
            fields = '__all__' 

    
class UserProfilePhotoSerializer(serializers.ModelSerializer):
      
    class Meta:
        model = User
        fields = ['foto']