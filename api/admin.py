import csv, datetime

from django import forms
from django.contrib import admin
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import path

from io import StringIO

from api import models


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


def mark_read(BookAdmin, request, queryset):
    for obj in queryset:
        obj.read = True
        obj.save()


mark_read.short_description = 'Mark as Read'


def process_authors_for_csv(book, data_row):
    authors = list(book.authors.all())
    if len(authors) > 0:
        data_row.append(authors[0].first_name)
        data_row.append(authors[0].last_name)
    else:
        data_row.extend(['', ''])

    if len(authors) > 1:
        data_row.append(authors[1].first_name)
        data_row.append(authors[1].last_name)
    else:
        data_row.extend(['', ''])

    if len(authors) > 2:
        data_row.append(authors[2].first_name)
        data_row.append(authors[2].last_name)
    else:
        data_row.extend(['', ''])

    return data_row


def export_to_csv(BookAdmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;' 'filename=book_output.csv'
    writer = csv.writer(response)
    fields = [
        'Title',
        'Year',
        'Author 1 First',
        'Author 1 Last',
        'Author 2 First',
        'Author 2 Last',
        'Author 3 First',
        'Author 3 Last',
        'Series',
        'Series Number',
        'Genre',
        'Subgenre',
        'Age Group',
        'Audiobook',
        'Read',
        'Cover Url',
        'Tags',
    ]

    # Write a first row with header information
    writer.writerow(fields)
    queryset = models.Book.objects.all()
    # Write data rows
    for book in queryset:
        data_row = [book.title, book.year]
        data_row = process_authors_for_csv(book, data_row)
        data_row.append(book.series.name if book.series else '')
        data_row.append(book.series_num or '')
        data_row.extend(
            [
                book.subgenre.genre.name,
                book.subgenre.name,
                book.age_group,
                'Y' if book.audiobook else 'N',
                'Y' if book.read else 'N',
                book.cover_url,
                ','.join([tag.name for tag in book.tags.all()]),
            ]
        )

        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Export ALL as CSV'


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ("first_name", "last_name")


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    change_list_template = "admin/entities/books_changelist.html"

    actions = (mark_read, export_to_csv)
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
