from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'status', 'due_date', 'completed', 'created_at')
    list_filter = ('priority', 'status', 'completed')
    search_fields = ('title', 'description')
