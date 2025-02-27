from rest_framework.pagination import PageNumberPagination


class MyPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'current_page'
    page_size_query_param = 'page_size'
    max_page_size = 100