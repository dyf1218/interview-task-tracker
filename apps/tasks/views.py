from rest_framework import generics

from .filters import TaskFilter
from .models import Task
from .permissions import IsOwner
from .serializers import TaskSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    """View for listing and creating tasks."""

    serializer_class = TaskSerializer
    filterset_class = TaskFilter
    search_fields = ['title']
    ordering_fields = ['created_at', 'updated_at', 'due_date', 'priority']
    ordering = ['-created_at']

    def get_queryset(self):
        """Return only tasks owned by the current user."""
        return Task.objects.filter(owner=self.request.user).select_related('owner')

    def perform_create(self, serializer):
        """Set the owner to the current user when creating a task."""
        serializer.save(owner=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating, and deleting a single task."""

    serializer_class = TaskSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        """Return only tasks owned by the current user."""
        return Task.objects.filter(owner=self.request.user).select_related('owner')