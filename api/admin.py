import csv
from django import forms
from django.contrib import admin
from django.db.utils import IntegrityError
from django.shortcuts import redirect, render
from django.urls import path

from io import StringIO

from api import models


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ("first_name", "last_name")


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    change_list_template = "admin/entities/books_changelist.html"

    list_display = ("title", "read", "author_display", "series", "series_num")
    list_filter = ("read", "subgenre", "age_group", "tags")
    search_fields = ("title", "authors__first_name", "authors__last_name", "series__name")
    fields = (
        "title",
        "year",
        "authors",
        "series",
        "series_num",
        "subgenre",
        "age_group",
        "audiobook",
        "read",
        "cover_url",
        "tags",
    )

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == 'POST':
            error_messages = []
            csv_file = StringIO(request.FILES['csv_file'].file.read().decode())
            reader = csv.DictReader(csv_file)
            for row in reader:
                if error := self._create_book(row):
                    error_messages.append(error)
            self.message_user(request, f'Your csv file has been imported {error_messages}')
            return redirect('..')
        form = CsvImportForm()
        payload = {'form': form}
        return render(request, 'admin/csv_form.html', payload)

    def _create_book(self, row):
        series, _ = models.Series.objects.get_or_create(name=row['Series']) if row['Series'] else (None, None)
        genre, _ = models.Genre.objects.get_or_create(name=row['Genre'])
        subgenre, _ = models.Subgenre.objects.get_or_create(genre=genre, name=row['Subgenre'])
        series_num = row['Series Number'] if row['Series Number'] else None
        try:
            book = models.Book.objects.create(
                title=row['Title'],
                year=row['Year'],
                series=series,
                series_num=series_num,
                subgenre=subgenre,
                age_group=row['Age Group'],
                audiobook=True if row['Audiobook'] == 'Y' else False,
                read=True if row['Read'] == 'Y' else False,
                cover_url=row['Cover Url'],
            )
            for idx in range(1, 4):
                if row[f'Author {idx} Last']:
                    author, _ = models.Author.objects.get_or_create(
                        first_name=row[f'Author {idx} First'], last_name=row[f'Author {idx} Last']
                    )
                    book.authors.add(author)
            for tag_name in row['Tags'].split(','):
                if tag_name != '':
                    tag, _ = models.Tag.objects.get_or_create(name=tag_name)
                    book.tags.add(tag)
        except IntegrityError:
            return f'Book {row["Title"]} not imported'


admin.site.register(models.Genre)
admin.site.register(models.Subgenre)
admin.site.register(models.Series)
admin.site.register(models.Tag)
