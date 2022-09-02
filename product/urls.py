from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from product import views

urlpatterns = [
    path('products/',
         views.ProductApiView.as_view()),
    path('products/<product_id>',
         views.SingleProductApiView.as_view()),
    path('products/name/<name>',
         views.SingleNameProductApiView.as_view()),
    path('products/manufacturer/<manufacturer>',
         views.SingleManufacturerApiView.as_view()),
    path('products/count_man/',
         views.CountManufacturer.as_view()),
    path('products/count_active/',
         views.CountActive.as_view()),
    path('products/count_sales_unit/',
         views.CountSalesUnit.as_view()),
    path('products/count_manufacturer/',
         views.CountManufacturer.as_view()),

    # click house paths
    path('products/click/<product_id>',
         views.SingleClickProductApiView.as_view()),
    path('products/click_manufacturer/<manufacturer>',
         views.SingleClickManufacturerApiView.as_view()),
    path('products/click_name/<name>',
         views.SingleClickNameApiView.as_view()),
    path('products/click_count_active/',
         views.ClickCountActive.as_view()),
    path('products/click_count_sales_unit/',
         views.ClickCountSalesUnit.as_view()),

    # comparisons
    path('products/comparison_count/',
         views.ComparisonAggregateApiView.as_view()),
    path('products/comparison_name/<name>',
         views.ComparisonNameApiView.as_view()),

    # statistic
    path('products/statistic/',
         views.StatisticApiView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)

# TODO: make group by endpoints sales_unit_pkg and comparison endpoint for manufacturer
