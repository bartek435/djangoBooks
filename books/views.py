import datetime
import json
import requests

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from .models import BookModel
from .forms import BookForm, SearchBookForm, ImportForm

def books_view(request):
    query_dict = request.GET
    context = {'search_form': SearchBookForm(query_dict)}
    if "Rest" in query_dict.get('get', ''):
        return redirect("/rest_books?"+request.META['QUERY_STRING'])
    if context['search_form'].is_valid():
        kwargs = get_data_from_query(query_dict.items())
    context['data'] = BookModel.objects.all().filter(**kwargs)
    return render(request, "books_view.html", context)

def get_data_from_query(query):
    kwargs = {}
    for key, value in query:
        if not value or key == 'get':
            continue
        if key == 'dateFrom':
            date = datetime.datetime.strptime(value, "%Y-%m-%d")
            kwargs['date__gte'] = date
        elif key == 'dateTo':
            date = datetime.datetime.strptime(value, "%Y-%m-%d")
            kwargs['date__lte'] = date
        else:
            kwargs['{}__icontains'.format(key)] = value
    return kwargs

def edit_view(request, book_id=None):
    if book_id is not None:
        book = get_object_or_404(BookModel, id=book_id)
        form = BookForm(request.POST or None, instance=book)
    else:
        form = BookForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect("/")

    return render(request, 'edit_view.html', {'form':form, 'id': id})

def import_view(request):
    form = ImportForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        query_string = get_import_query_string(request.POST)
        imported = HttpResponse(
            requests.get(
                "https://www.googleapis.com/books/v1/volumes?"+query_string
            )
        )
        imported_dict = json.loads(imported.content)
        if 'items' in imported_dict:
            add_imported(imported_dict['items'])
            return redirect('/')
    return render(request, "import_view.html", {'form': form})

def get_import_query_string(post):
    query_string = "q="+'&'.join(post.get('q', '').split(' '))
    keys = ['q', 'intitle', 'inauthor', 'isbn', 'subject']
    for key in keys:
        query_string += "+{}:{}".format(key, post.get(key, ''))
    return query_string

def delete_view(request, book_id=None):
    if request.method == 'GET':
        if book_id == 0:
            BookModel.objects.all().delete()
        else:
            obj = get_object_or_404(BookModel, id=book_id)
            obj.delete()
    return redirect('/')

def add_imported(imported_data):
    for data in imported_data:
        item = {}
        item['title'] = data['volumeInfo']['title']
        item['author'] = ', '.join(data['volumeInfo'].get('authors', ['']))
        item['date'] = data['volumeInfo'].get('publishedDate', '')
        item['pages'] = data['volumeInfo'].get('pageCount', None)
        item['isbn'] = get_isbn(data['volumeInfo'].get('industryIdentifiers', []))
        item['cover'] = data['volumeInfo']['previewLink']
        item['language'] = data['volumeInfo']['language']
        form = BookForm(item)
        if form.is_valid():
            BookModel.objects.create(**item)

def get_isbn(isbn_list):
    for data in isbn_list:
        if 'ISBN' in data['type']:
            return data['identifier']
    return ''
