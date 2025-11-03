from django.contrib import admin
from .models import ActivityLog

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    """
    Admin configuration for the ActivityLog model.
    """
    list_display = ('user', 'date', 'category', 'value', 'carbon_equivalent')
    list_filter = ('date', 'category', 'user')
    search_fields = ('user__username', 'category')
    date_hierarchy = 'date'
    ordering = ('-date',)

    fieldsets = (
        (None, {
            'fields': ('user', 'date', 'category', 'value')
        }),
        ('Calculated Values', {
            'fields': ('carbon_equivalent',)
        }),
    )

    # Make calculated field read-only
    readonly_fields = ('carbon_equivalent',)