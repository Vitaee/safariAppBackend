from rest_framework import pagination

class SafariPagination(pagination.PageNumberPagination):
    page_size = 2
    max_page_size = 10
    page_query_param = 'page'