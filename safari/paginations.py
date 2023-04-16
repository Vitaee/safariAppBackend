from rest_framework import pagination

class SafariPagination(pagination.PageNumberPagination):
    page_size = 5
    max_page_size = 1000
    page_query_param = 'page'

    def get_cache_key(self, request, queryset, view):
        # Include the current page number in the cache key
        page_number = request.query_params.get(self.page_query_param, 1)
        key_parts = [
            f"safari-{view.action}",
            f"page-{page_number}"
        ]
        return ":".join(key_parts)