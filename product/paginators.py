from rest_framework.pagination import PageNumberPagination


class ProductPaginator(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000
    page_query_param = 'page'
