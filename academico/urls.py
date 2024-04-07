from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from academico import views
from .views import GradoListCreateView, GradoDetailView, becadoListCreateView, BecadoDetailView, ClienteDetailView, ClienteListCreateView, AlumnoListCreateView, AlumnoDetailView

urlpatterns = [
    # alumnos endpoints
    path('alumnos/', AlumnoListCreateView.as_view(), name='alumnos'),
    path('alumnos/<int:pk>/', AlumnoDetailView.as_view()),
    # grados endpoints
    path('grados/', GradoListCreateView.as_view()),
    path('grados/<int:pk>/', GradoDetailView.as_view()),
    # matriculas endpoints
    path('matricula/', views.matricula_list),
    path('matricula/<int:pk>/', views.matricula_detail),
    path('grados/', views.grado_list),
    path('grados/<int:pk>/', views.grado_detail),
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