from rest_framework.response import Response
from rest_framework.views import APIView
from.models import Organization
from.serializers import OrganizationSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, DjangoObjectPermissions

class OrganizationView(APIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Organization.objects.all()
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        organization = Organization.load()
        serializer = OrganizationSerializer(organization)
        return Response(serializer.data)

    def put(self, request):
        organization = Organization.load()
        serializer = OrganizationSerializer(organization, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)