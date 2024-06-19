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

    # Compra endpoints
    path('compra/', views.CompraListCreateView.as_view() ),
    path('compra/<int:pk>', views.CompraDetailView.as_view()),

    # Compra endpoints
    path('flujo_caja/', views.FlujoCajaListCreateView.as_view() ),
    path('flujo_caja/<int:pk>', views.FlujoCajaDetailView.as_view()),
]