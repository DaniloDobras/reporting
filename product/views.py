import logging
import time
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
    ManufacturerAggregateSerializer, ActiveAggregateSerializer, \
    SalesUnitSerializer


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


class CountSalesUnit(views.APIView):
    serializer_class = ActiveAggregateSerializer

    @traced
    def get(self, request):
        queryset = (Product.objects.values('sales_unit_pkgg')
                    .annotate(count=Count('sales_unit_pkgg'))
                    .order_by()
                    )
        serializer = SalesUnitSerializer(queryset, many=True)
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


class ClickCountActive(views.APIView):
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


class ClickCountSalesUnit(views.APIView):
    @traced
    def get(self, request):
        client = Client(host='localhost')
        query = """SELECT  count(*) as count, sales_unit_pkgg 
                        from product.product 
                        group by sales_unit_pkgg"""
        result, columns = client.execute(query, with_column_types=True)
        df = pd.DataFrame(result, columns=[tuple[0] for tuple in columns])
        df_json = df.to_json(orient='records')
        json_object = json.loads(df_json)
        return JsonResponse(
            json_object,
            content_type="application/json",
            safe=False
        )


# comparisons

class ComparisonAggregateApiView(views.APIView):
    @traced
    def get(self, request):
        click_start_time = round(time.time() * 1000)
        client = Client(host='localhost')
        query = """SELECT  count(*) as count, active 
                                from product.product 
                                group by active"""
        result, columns = client.execute(query, with_column_types=True)
        df = pd.DataFrame(result, columns=[tuple[0] for tuple in columns])
        df_json = df.to_json(orient='records')
        json_object = json.loads(df_json)
        logging.info(json_object)
        click_end_time = round(time.time() * 1000)

        rel_start_time = round(time.time() * 1000)
        queryset = (Product.objects.values('active')
                    .annotate(count=Count('active'))
                    .order_by()
                    )
        serializer = ActiveAggregateSerializer(queryset, many=True)
        logging.info(serializer)
        rel_end_time = round(time.time() * 1000)
        click_time = click_end_time - click_start_time
        rel_time = rel_end_time - rel_start_time
        response = {
            "click_time": click_time,
            "rel_time": rel_time
        }
        return JsonResponse(
            response,
            content_type="application/json",
            safe=False
        )


class ComparisonNameApiView(views.APIView):
    @traced
    def get(self, request, name):
        click_start_time = round(time.time() * 1000)
        client = Client(host='localhost')
        query = f"""SELECT * from product.product where name = '{name}'"""
        result, columns = client.execute(query, with_column_types=True)
        df = pd.DataFrame(result, columns=[tuple[0] for tuple in columns])
        df_json = df.to_json(orient='records')
        json_object = json.loads(df_json)
        logging.info(json_object)
        click_end_time = round(time.time() * 1000)

        rel_start_time = round(time.time() * 1000)
        queryset = (Product.objects.filter(name=name)
                    )
        serializer = ProductSerializer(queryset, many=True)
        logging.info(serializer)
        rel_end_time = round(time.time() * 1000)
        click_time = click_end_time - click_start_time
        rel_time = rel_end_time - rel_start_time
        response = {
            "click_time": click_time,
            "rel_time": rel_time
        }
        return JsonResponse(
            response,
            content_type="application/json",
            safe=False
        )


class StatisticApiView(views.APIView):
    @traced
    def get(self, request):
        df = pd.read_csv("reporting_mjerenja_diplomski.csv")
        df_json = df.to_json(orient='records')
        json_response = json.loads(df_json)
        return JsonResponse(
            json_response,
            content_type="application/json",
            safe=False
        )


