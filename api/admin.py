from django.contrib import admin

from api import models


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ("first_name", "last_name")


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author_display", "series")
    list_filter = ("read", "subgenre", "age_group")
    search_fields = ("title", "authors__first_name", "authors__last_name", "series__name")
    fields = (
        "title",
        "year",
        "authors",
        "series",
        "series_num",
        "subgenre",
        "age_group",
        "read",
        "cover_url",
    )


admin.site.register(models.Genre)
admin.site.register(models.Subgenre)
admin.site.register(models.Series)
