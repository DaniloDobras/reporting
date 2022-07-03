from autologging import traced
from django.http import JsonResponse
from rest_framework import views, permissions

from product.models import Product
from product.paginators import ProductPaginator
from product.serializer import ProductSerializer


class ProductApiView(views.APIView):
    http_method_names = ['get']
    permission_classes = (permissions.AllowAny,)
    serializer_class = ProductSerializer
    pagination_class = ProductPaginator

    @traced
    def get(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return JsonResponse(data=serializer.data, safe=False)


class SingleProductApiView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ProductSerializer

    @traced
    def get(self, request, product_id: str):
        queryset = Product.objects.filter(id=product_id).first()
        serializer = ProductSerializer(queryset)
        return JsonResponse(
            serializer.data,
            content_type="application/json"
        )


class SingleNameProductApiView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ProductSerializer

    @traced
    def get(self, request, name: str):
        queryset = Product.objects.filter(name=name).first()
        serializer = ProductSerializer(queryset)
        return JsonResponse(
            serializer.data,
            content_type="application/json"
        )


class SingleManufacturerApiView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ProductSerializer

    @traced
    def get(self, request, manufacturer: str):
        print(manufacturer)
        queryset = Product.objects.filter(manufacturer=manufacturer).first()
        serializer = ProductSerializer(queryset)
        return JsonResponse(
            serializer.data,
            content_type="application/json"
        )


class SingleClickManufacturerApiView(views.APIView):
    pass


class SingleClickNameApiView(views.APIView):
    pass


class SingleClickBaseUnitApiView(views.APIView):
    pass
