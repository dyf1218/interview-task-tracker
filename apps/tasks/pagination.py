from rest_framework.pagination import PageNumberPagination


class TaskPagination(PageNumberPagination):
    """Custom pagination class for tasks."""

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100