from rest_framework import serializers
from rest_framework.validators import ValidationError 
from .models import User
from django.contrib.auth.models import  Group 


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=80)
    nombre = serializers.CharField(max_length= 50)
    password = serializers.CharField(min_length=8, write_only=True) 
    
    class Meta(object):
        model = User 
        fields = [ 'id', 'email', 'password', 'nombre', 'apellido', 'is_active']
    
    def validate(self, attrs):
        user_id = self.context['view'].kwargs['pk'] if 'pk' in self.context['view'].kwargs else None
        
        if user_id:
            if User.objects.exclude(id=user_id).filter(email=attrs['email']).exists():
                raise ValidationError('El correo ya se encuentra en uso!')
        elif User.objects.filter(email=attrs['email']).exists():
            raise ValidationError('El correo ya se encuentra en uso!')
        
        return super().validate(attrs)


class UserOutputSerializer(serializers.ModelSerializer): 
    password = serializers.CharField(write_only=True) 
    # group = serializers.SerializerMethodField()

    # def get_group(self, obj):
    #     try:
    #         group = obj.groups.get()
    #         return group.id
    #     except Group.DoesNotExist:
    #         return None
    class Meta(object):
            model = User 
            fields = '__all__' 

    
