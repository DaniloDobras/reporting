import datetime
import json

import pandas as pd

from autologging import traced
from django.db.models import Count
from django.http import JsonResponse
from rest_framework import views, permissions

from clickhousepy import Client
from product.models import Product
from product.paginators import ProductPaginator
from product.serializer import ProductSerializer, \
    ManufacturerAggregateSerializer, ActiveAggregateSerializer


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
        queryset = Product.objects.filter(id=product_id)
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
        queryset = Product.objects.filter(name=name)
        serializer = ProductSerializer(queryset, many=True)
        return JsonResponse(
            serializer.data,
            content_type="application/json",
            safe=False
        )


class SingleManufacturerApiView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ProductSerializer

    @traced
    def get(self, request, manufacturer: str):
        queryset = Product.objects.filter(manufacturer=manufacturer)
        serializer = ProductSerializer(queryset, many=True)
        return JsonResponse(
            serializer.data,
            content_type="application/json",
            safe=False
        )


class CountManufacturer(views.APIView):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = ManufacturerAggregateSerializer

    @traced
    def get(self, request):
        queryset = (Product.objects.values('manufacturer')
                    .annotate(count=Count('manufacturer'))
                    .order_by()
                    )
        serializer = ManufacturerAggregateSerializer(queryset, many=True)
        return JsonResponse(
            serializer.data,
            content_type="application/json",
            safe=False
        )


class CountActive(views.APIView):
    serializer_class = ActiveAggregateSerializer

    @traced
    def get(self, request):
        queryset = (Product.objects.values('active')
                    .annotate(count=Count('active'))
                    .order_by()
                    )
        serializer = ActiveAggregateSerializer(queryset, many=True)
        return JsonResponse(
            serializer.data,
            content_type="application/json",
            safe=False
        )


# Click house api views

class SingleClickProductApiView(views.APIView):

    @traced
    def get(self, request, product_id: str):
        client = Client(host='localhost')
        query = f"""SELECT * FROM product.product 
                                                where id = '{product_id}'"""
        result, columns = client.execute(query, with_column_types=True)
        df = pd.DataFrame(result, columns=[tuple[0] for tuple in columns])
        df_json = df.to_json(orient='records')
        json_object = json.loads(df_json)
        return JsonResponse(
            json_object[0],
            content_type="application/json",
            safe=False
        )


class SingleClickNameApiView(views.APIView):
    @traced
    def get(self, request, name: str):
        client = Client(host='localhost')
        query = f"""SELECT * FROM product.product 
                                            where name = '{name}'"""
        result, columns = client.execute(query, with_column_types=True)
        df = pd.DataFrame(result, columns=[tuple[0] for tuple in columns])
        df_json = df.to_json(orient='records')
        json_object = json.loads(df_json)
        return JsonResponse(
            json_object,
            content_type="application/json",
            safe=False
        )


class SingleClickManufacturerApiView(views.APIView):
    @traced
    def get(self, request, manufacturer: str):
        client = Client(host='localhost')
        query = f"""SELECT * FROM 
                                      product.product 
                                      where manufacturer = '{manufacturer}'"""
        result, columns = client.execute(query, with_column_types=True)
        df = pd.DataFrame(result, columns=[tuple[0] for tuple in columns])
        df_json = df.to_json(orient='records')
        json_object = json.loads(df_json)
        return JsonResponse(
            json_object,
            content_type="application/json",
            safe=False
        )


class SingleClickCountActive(views.APIView):
    @traced
    def get(self, request):
        client = Client(host='localhost')
        query = """SELECT  count(*) as count, active 
                        from product.product 
                        group by active"""
        result, columns = client.execute(query, with_column_types=True)
        df = pd.DataFrame(result, columns=[tuple[0] for tuple in columns])
        df_json = df.to_json(orient='records')
        json_object = json.loads(df_json)
        return JsonResponse(
            json_object,
            content_type="application/json",
            safe=False
        )
