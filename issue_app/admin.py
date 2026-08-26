"""
admin.py
---------
This file makes our models (Issue, Comment) visible and
editable inside the Django Admin panel at ../admin/
"""

from django.contrib import admin
from .models import Issue, Comment


class IssueAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'reported_by', 'created_at']
    list_filter = ['category', 'status']
    search_fields = ['title', 'description', 'location']


admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment)
