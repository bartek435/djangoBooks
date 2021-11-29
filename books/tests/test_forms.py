from django.test import TestCase
from books.forms import BookForm, SearchBookForm, ImportForm

class TestForms(TestCase):
    def testBookForm_valid(self):
        form = BookForm(data={
            'title': 'Test Title',
            'author': 'me',
            'date': '2020-12-1',
            'isbn': '1112223334555',
            'pages': 220,
            'cover': 'http://google.com',
            'language': 'eng'
        })
        self.assertTrue(form.is_valid())
    def testBookForm_invalid(self):
        forms = []
        forms.append(BookForm(data={
            'title': 'Test Title',
            'author': 'me',
            'date': '2020-12-0',
            'isbn': '1112223334555',
            'pages': 111,
            'language': 'eng'
        }))
        forms.append(BookForm(data={
            'title': 'Test Title',
            'author': 'me',
            'date': '2020-12',
            'isbn': '1112223334555',
            'pages': 111,
            'cover': 'http://google.com',
        }))
        forms.append(BookForm(data={
            'title': 'Test Title',
            'author': 'me',
            'date': '2020-12',
            'isbn': '1112223334555',
            'pages': 111,
            'cover': 'http://google.com',
            'language': 'eng'
        }))
        forms.append(BookForm(data={
            'title': 'Test Title',
            'author': 'me',
            'date': '2020-12',
            'isbn': None,
            'pages': 'absd',
            'cover': 'http://google.com',
            'language': 'eng'
        }))
        forms.append(BookForm(data={
            'author': 'me',
            'date': '2020-22-1',
            'isbn': '1112223334555',
            'pages': 111,
            'cover': 'http://google.com',
            'language': 'eng'
        }))
        for form in forms:
            self.assertFalse(form.is_valid())
    def testSearchForm_valid(self):
        form = SearchBookForm(data={
            'title': 'Test Title',
            'dateFrom': '1995-12-2'
        })
        self.assertTrue(form.is_valid())
    def testSearchForm_invalid(self):
        form = SearchBookForm(data={
            'title': 'Test Title',
            'dateFrom': '1995-12-2',
            'dateTo': '1995-2-1'
        })
        self.assertFalse(form.is_valid())
    def testImportForm_valid(self):
        form = ImportForm(data={
            'title': 'Test Title',
            'q': 'test'
        })
        self.assertTrue(form.is_valid())
    def testImportForm_invalid(self):
        form = ImportForm(data={
            'title': 'Test Title',
            'q': 'test',
            'isbn': 123
        })
        self.assertFalse(form.is_valid())
