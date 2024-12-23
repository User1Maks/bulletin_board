from rest_framework.pagination import PageNumberPagination


class AdPaginator(PageNumberPagination):
    """Пагинация для объявлений"""
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 100
