from rest_framework import serializers
from rest_framework.validators import ValidationError
from rest_framework.serializers import PrimaryKeyRelatedField
from .models import User
from django.contrib.auth.models import  Group 


class GroupSerializer(PrimaryKeyRelatedField, serializers.ModelSerializer):
    name = serializers.CharField(max_length=80)
    class Meta:
        model = Group
        fields = ['name']

class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=80)
    nombre = serializers.CharField(max_length= 50)
    password = serializers.CharField(min_length=8, write_only=True) 
    
    class Meta(object):
        model = User 
        fields = [ 'id', 'email', 'password', 'nombre', 'apellido', 'is_active']

    def validate(self, attrs):
        
        email_exists = User.objects.filter(email=attrs['email']).exists()
        if email_exists:
            raise ValidationError('El correo ya se encuentra en uso!')


        return super().validate(attrs)


