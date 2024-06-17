from django.urls import path
from . import views
 
urlpatterns = [
    # timbrado endpoints
    path('timbrado/', views.TimbradoListCreateView.as_view()),
    path('timbrado/<int:pk>/', views.TimbradoDetailView.as_view()),
 
    # Comprobante endpoints
    path('comprobante/', views.ComprobanteListCreateView.as_view()), 
    path('comprobante/<int:pk>', views.ComprobanteDetailView.as_view()),
    
    # producto endpoints
    path('producto/', views.ProductoListCreateView.as_view()),
    path('producto/<int:pk>', views.ProductoDetailView.as_view()),

    # arancel endpoints
    path('arancel/', views.ArancelListCreateView.as_view() ),
    path('arancel/<int:pk>', views.ArancelDetailView.as_view()),

    # Venta endpoints
    path('venta/', views.VentaListCreateView.as_view() ),
    path('venta/<int:pk>', views.VentaDetailView.as_view()),

    # PagoVenta endpoints
    path('venta/pago/', views.PagoVentaListView.as_view() ),
    path('venta/pago/<int:pk>', views.PagoVentaDetailView.as_view()),

]