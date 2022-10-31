from api import models
from .existing_books import books

for book in books:
    author_list = []
    for author in book['authors']:
        author_obj, _ = models.Author.objects.get_or_create(
            first_name=author['first_name'], last_name=author['last_name']
        )
        author_list.append(author_obj)
    if series := book['series']:
        series, _ = models.Series.objects.get_or_create(name=series['name'])
    genre, _ = models.Genre.objects.get_or_create(name=book['genre']['name'])
    subgenre, _ = models.Subgenre.objects.get_or_create(name=book['subgenre']['name'], genre=genre)
    tag_list = []
    for tag in book['tags']:
        tag_obj, _ = models.Tag.objects.get_or_create(name=tag['name'])
        tag_list.append(tag_obj)
    book = models.Book.objects.create(
        title=book['title'],
        age_group=book['age_group'].replace('_', '-'),
        audiobook=book['audiobook'],
        cover_url=book['cover_url'],
        read=book['read'],
        series=series,
        series_num=book['series_number'],
        subgenre=subgenre,
        year=book['year'],
    )
    book.authors.set(author_list)
    book.tags.set(tag_list)
    book.save()
