from django.urls import path  
from .views import OrganizationView 

urlpatterns = [ 
    # Organization endpoints
    path('organization/', OrganizationView.as_view()),
]