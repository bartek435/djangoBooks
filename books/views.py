import datetime
import json
import requests

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from .models import BookModel
from .forms import BookForm, SearchBookForm, ImportForm

# Create your views here.
def booksView(request,):
    query_dict = request.GET
    context = {'search_form': SearchBookForm(query_dict)}
    kwargs = {}
    if "Rest" in query_dict.get('get',''):
        return redirect("/rest_books?"+request.META['QUERY_STRING'])
    if context['search_form'].is_valid():
        for key, value in query_dict.items():
            if not value or key == 'get':
                continue
            if key == 'dateFrom':
                date = datetime.datetime.strptime(value,"%Y-%m-%d")
                kwargs['date__gte'] = date
            elif key == 'dateTo':
                date = datetime.datetime.strptime(value,"%Y-%m-%d")
                kwargs['date__lte'] = date
            else:
                kwargs['{}__icontains'.format(key)] = value
    context['data'] = BookModel.objects.all().filter(**kwargs)
    return render(request, "books_view.html", context)

def editView(request, id=None):
    if id is not None:
        book = get_object_or_404(BookModel,id=id)
        form = BookForm(request.POST or None, instance = book)
    else :
        form = BookForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect("/")

    return render(request,'edit_view.html', {'form':form, 'id': id})

def importView(request):
    form = ImportForm()
    if request.method == 'POST':
        form = ImportForm(request.POST)
        if form.is_valid():
            query_string = "q="+'&'.join(request.POST.get('q','').split(' '))
            query_keys = {
                'title': 'intitle',
                'author': 'inauthor',
                'isbn': 'isbn',
                'subject':
                'subject'
            }
            for key,value in request.POST.items():
                if key in ['get', 'q'] or not value or 'csrf' in key :
                    continue
                query_string += "+"+query_keys[key]+':'+value
            imported =  HttpResponse(
                requests.get(
                    "https://www.googleapis.com/books/v1/volumes?"+query_string
                    )
                )
            imported_dict = json.loads(imported.content)
            if 'items' in imported_dict:
                addImported(imported_dict['items'])
                return redirect('/')
    return render(request, "import_view.html", {'form': form})

def deleteView(request,id =None):
    if request.method == 'GET':
        if id == 0:
            BookModel.objects.all().delete()
        else:
            obj = get_object_or_404(BookModel,id=id)
            obj.delete()
    return redirect('/')

def addImported(data):
    for d in data:
        item = {}
        item['title'] = d['volumeInfo']['title']
        item['author'] = ', '.join(d['volumeInfo'].get('authors', ['']))
        item['date'] = d['volumeInfo'].get('publishedDate','')
        item['pages'] = d['volumeInfo'].get('pageCount',None)
        item['isbn'] = getISBN(d['volumeInfo'].get('industryIdentifiers',[]))
        item['cover'] = d['volumeInfo']['previewLink']
        item['language'] = d['volumeInfo']['language']
        form = BookForm(item)
        if form.is_valid():
            BookModel.objects.create(**item)

def getISBN(isbn_list):
    for data in isbn_list:
        if 'ISBN' in data['type']:
            return data['identifier']
    return ''
