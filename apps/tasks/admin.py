from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin configuration for Task model."""

    list_display = [
        'id',
        'title',
        'owner',
        'status',
        'priority',
        'due_date',
        'created_at',
    ]
    list_filter = ['status', 'priority', 'created_at']
    search_fields = ['title', 'owner__username']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']