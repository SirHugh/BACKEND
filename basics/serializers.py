from rest_framework import serializers
from.models import Organization

class OrganizationSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(required=False)
    class Meta:
        model = Organization
        fields = '__all__'

    def create(self, validated_data):
        if Organization.objects.exists():
            organization = Organization.objects.get()
            organization.name = validated_data['name']
            organization.address = validated_data['address']
            organization.save()
            return organization
        else:
            return super().create(validated_data)
    
    def get_photo_url(self, Organization):
        request = self.context.get('request')
        photo_url = Organization.photo.url
        return request.build_absolute_uri(photo_url)