from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from academico import views
from .views import GradoDetailView, becadoListCreateView, BecadoDetailView, ClienteDetailView, ClienteListCreateView, AlumnoListCreateView, AlumnoDetailView

urlpatterns = [
    # alumnos endpoints
    path('alumnos/', AlumnoListCreateView.as_view(), name='alumnos'),
    path('alumnos/<int:pk>/', AlumnoDetailView.as_view()),
    # grados endpoints
    path('grados/', views.GradoListCreateView.as_view()),
    path('grados/<int:pk>/', GradoDetailView.as_view()),
    # matriculas endpoints
    path('matricula/', views.MatriculaListCreateView.as_view()),
    path('matricula/<int:pk>/', views.MatriculaDetailView.as_view()),
    # grado endpoints
    path('grados/', views.grado_list),
    path('grados/<int:pk>/', views.grado_detail), 
    # beca endpoints
    path('beca/', views.BecaListCreateView.as_view()),
    path('beca/<int:pk>/', views.BecaDetailView.as_view()),
    # becados endpoints
    path('becado/', becadoListCreateView.as_view(), name='becado-list-create'),
    path('becado/<int:pk>/', BecadoDetailView.as_view(), name='becado-detalle'),
    path('becado/beca/<int:pk>/', views.becado_detail),
    # cliente endpoints
    path('cliente/', ClienteListCreateView.as_view()),
    path('cliente/<int:pk>/', ClienteDetailView.as_view()),
    # responsable endpoints
    path('responsable/', views.responsable_list),
    path('responsable/<int:pk>/', views.responsable_detail),
]

# urlpatterns = format_suffix_patterns(urlpatterns)