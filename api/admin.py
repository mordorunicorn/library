from django.contrib import admin

from api import models


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'read')
    list_filter = ('read', 'genre', 'age_group')
    search_fields = ('title',)


admin.site.register(models.Author)
