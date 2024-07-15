from rest_framework.urls import path
from . import views

urlpatterns = [
    # Stock Control Endpoints
    path('stock_control/', views.ControlListView.as_view()),
    path('stock_control/<int:pk>', views.ControlDatailView.as_view()),
    path('initiate_stock_control/', views.InitiateStockControlView.as_view()),
    path('stock_control/<int:pk>/close', views.CloseStockControlView.as_view()),
    
    # Detalle Stock Control Endpoints
    path('detalle_stock_control/', views.DetalleControlListView.as_view()),
    path('detalle_stock_control/<int:pk>', views.DetalleControlDetailView.as_view()),
    
]
