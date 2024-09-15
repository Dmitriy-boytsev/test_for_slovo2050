from django.contrib import admin

from tasks.models import ToDo


@admin.register(ToDo)
class ToDoAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'completed', 'user')
    list_filter = ('completed', 'user')
