from django.contrib import admin
from .models import Employee, Task

admin.site.register(Employee)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'status', 'priority', 'due_date')
    list_filter = ('status', 'priority')
    search_fields = ('title', 'assigned_to__username')