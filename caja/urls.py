from django.urls import path
from . import views



urlpatterns = [
    # timbrado endpoints
    path('timbrado/', views.TimbradoListCreateView.as_view()),
    path('timbrado/<int:pk>/', views.TimbradoDetailView.as_view()),

    # factura endpoints
    path('factura/', views.FacturaListCreateView.as_view()), 
    path('factura/<int:pk>', views.FacturaDetailView.as_view()),

    # factura endpoints
    path('comprobante/', views.ComprobanteListCreateView.as_view()), 
    path('comprobante/<int:pk>', views.ComprobanteDetailView.as_view()),
    
    # producto endpoints
    path('producto/', views.ProductoListCreateView.as_view()),
    path('producto/<int:pk>', views.ProductoDetailView.as_view()),

    # arancel endpoints
    path('arancel/', views.ArancelListCreateView.as_view() ),
    path('arancel/<int:pk>', views.ArancelDetailView.as_view()),
]