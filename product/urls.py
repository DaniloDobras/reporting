from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from product import views

urlpatterns = [
    path('products/', views.ProductApiView.as_view()),
    path('products/<product_id>', views.SingleProductApiView.as_view()),
    path('products/name/<name>', views.SingleNameProductApiView.as_view()),
    path('products/manufacturer/<manufacturer>',
         views.SingleManufacturerApiView.as_view()),
    path('products/count_man/', views.CountManufacturer.as_view()),
    path('products/count_active/', views.CountActive.as_view()),
    # click house paths
    path('products/click/<product_id>',
         views.SingleClickProductApiView.as_view()),
    path('products/click_manufacturer/<manufacturer>',
         views.SingleClickManufacturerApiView.as_view()),
    path('products/click_name/<name>',
         views.SingleClickNameApiView.as_view()),
    path('products/click_count_active/',
         views.SingleClickCountActive.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
