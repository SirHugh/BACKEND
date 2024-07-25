from django.urls import path
from . import views
 
urlpatterns = [
    # timbrado endpoints
    path('timbrado/', views.TimbradoListCreateView.as_view()),
    path('timbrado/<int:pk>/', views.TimbradoDetailView.as_view()),
 
    # Comprobante endpoints
    path('comprobante/', views.ComprobanteListCreateView.as_view()), 
    path('comprobante/<int:pk>/', views.ComprobanteDetailView.as_view()),
    
    # producto endpoints
    path('producto/', views.ProductoListCreateView.as_view()),
    path('producto/<int:pk>', views.ProductoDetailView.as_view()),
    
    # Baja de Inventario endpoints
    path('inventario/ajuste/', views.BajaInventarioListCreateView.as_view()),
    path('inventario/ajuste/<int:pk>', views.BajaInventarioDetailView.as_view()),

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

    # Flujo de Caja endpoints
    path('flujo_caja/', views.FlujoCajaListCreateView.as_view() ),
    path('flujo_caja/<int:pk>', views.FlujoCajaDetailView.as_view()),
    
    # Tipo Actividad endpoints
    path('actividad/tipo/', views.TipoActividadListCreateView.as_view() ),
    path('actividad/tipo/<int:pk>', views.TipoActividadDetailView.as_view()),
    
    # Actividad endpoints
    path('actividad/', views.ActividadListCreateView.as_view() ),
    path('actividad/<int:pk>', views.ActividadDetailView.as_view()),
    
    
    # Pago Actividad endpoints
    path('actividad/pago/', views.PagoActividadListView.as_view() ),
    path('actividad/pago/<int:pk>', views.PagoActividadDetailView.as_view()),
    path('actividad/pago/pendiente/', views.PendientePagoActividadView.as_view()),
    
    #Estado de cuenta endpoints
    path('estado_cuenta/<int:pk>', views.EstadoDeCuenta),
    
    #Forma de pago endpoints
    path('forma_pago/', views.FormaPagoListCreateView.as_view() ),
    path('forma_pago/<int:pk>', views.FormaPagoDetailView.as_view() ),
    
    path('send_email/', views.FileUploadView.as_view() ),
    
    # Reportes
    path('reports/products/', views.ProductCountsView.as_view() ),
    path('reports/flujo-caja/', views.CashFlowCountsView.as_view() ),
    
    
]