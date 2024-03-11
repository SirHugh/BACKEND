from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from academico import views

urlpatterns = [
    path('alumnos/', views.alumno_list),
    path('alumnos/<int:pk>/', views.alumno_detail),
    path('grados/', views.grado_list),
    path('grados/<int:pk>/', views. grado_detail),
    path('matricula/', views.matricula_list),
    path('matricula/<int:pk>/', views.matricula_detail),
    
]

# urlpatterns = format_suffix_patterns(urlpatterns)