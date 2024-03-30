from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from academico import views
from .views import becadoListCreateView, BecadoDetailView, ClienteDetailView, ClienteListCreateView

urlpatterns = [
    path('alumnos/', views.alumno_list),
    path('alumnos/<int:pk>/', views.alumno_detail),
    path('grados/', views.grado_list),
    path('grados/<int:pk>/', views. grado_detail),
    path('matricula/', views.matricula_list),
    path('matricula/<int:pk>/', views.matricula_detail),
    path('grados/', views.grado_list),
    path('grados/<int:pk>/', views. grado_detail),
    path('matricula/', views.matricula_list),
    path('matricula/<int:pk>/', views.matricula_detail),
    path('beca/', views.beca_list),
    path('beca/<int:pk>/', views.beca_detail),
    path('becado/', becadoListCreateView.as_view(), name='becado-list-create'),
    path('becado/<int:pk>/', BecadoDetailView.as_view(), name='becado-detalle'),
    path('becado/beca/<int:pk>/', views.becado_detail),
    path('cliente/', ClienteListCreateView.as_view()),
    path('cliente/<int:pk>/', ClienteDetailView.as_view()),
    path('responsable/', views.responsable_list),
    path('responsable/<int:pk>/', views.responsable_detail),
]

# urlpatterns = format_suffix_patterns(urlpatterns)