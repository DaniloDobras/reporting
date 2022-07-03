from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from product import views

urlpatterns = [
    path('products/', views.ProductApiView.as_view()),
    path('products/<product_id>', views.SingleProductApiView.as_view()),
    path('products/name/<name>', views.SingleNameProductApiView.as_view()),
    path('products/manufacturer/<manufacturer>',
         views.SingleManufacturerApiView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)