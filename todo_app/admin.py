from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'priority', 'progress', 'due_date', 'created_date')
    list_filter = ('status', 'priority', 'user')
    search_fields = ('title', 'description')
    ordering = ('-created_date',)
    date_hierarchy = 'created_date'
