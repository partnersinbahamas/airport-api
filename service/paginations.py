from rest_framework.pagination import PageNumberPagination

class FlightListPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "size"
    page_query_param = "page"
