from django.urls import path
from .views import FarmerDashboardView, UpdateProductView, ProductListView, DeleteProductView, SettingsView, ShowReviewView, OrderView

urlpatterns = [
    path('', FarmerDashboardView.as_view(), name='farmer_dashboard'),
    path('dashboard/', FarmerDashboardView.as_view(), name='farmer_dashboard'),
    path('dashboard/update/<int:product_id>/', UpdateProductView.as_view(), name='update_product'),
    path('dashboard/delete/<int:product_id>/', DeleteProductView.as_view(), name='delete_product'),
    path('product/', ProductListView.as_view(), name="product"),
    path('settings/', SettingsView.as_view(), name="settings"),
    path('show-review', ShowReviewView.as_view(), name="show-review"),
    path('orders/', OrderView.as_view(), name="orders")
]
