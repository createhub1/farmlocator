from django.urls import path
from .views import ConsumerDashboardView, ProductComparisonView, CategoryProductsView, AddToCartView, ShowCartView, RemoveProductView, ReviewsViews, UpdateCartAddressView, UpdateQuantityView

urlpatterns = [
    path('', ConsumerDashboardView.as_view(), name='consumer_dashboard'),
    path('compare-products/', ProductComparisonView.as_view(), name='compare-products'),
    path('category-products/<str:category>/', CategoryProductsView.as_view(), name='category-products'),
    path('add-to-cart/<int:product_id>/', AddToCartView.as_view(), name='add-to-cart'),
    path('show-cart/', ShowCartView.as_view(), name='show-cart'),
    path('remove-product/<int:cart_item_id>/', RemoveProductView.as_view(), name='remove-product'),
    path('reviews/<int:product_id>/', ReviewsViews.as_view(), name="reviews"),
    path('update-cart-address/', UpdateCartAddressView.as_view(), name='update_cart_address'),
    path('cart/update/<int:cart_id>/', UpdateQuantityView.as_view(), name='update_quantity'),
]
