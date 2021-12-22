from django.test import SimpleTestCase
from django.urls import reverse, resolve

from books.views import  books_view, delete_view, edit_view, import_view
from books.rest_api.views import BooksRestView

class TestUrls(SimpleTestCase):

    def test_books_url_resolved(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, books_view)

    def test_edit_url_resolved(self):
        url = reverse('edit')
        self.assertEqual(resolve(url).func, edit_view)

    def test_import_url_resolved(self):
        url = reverse('import')
        self.assertEqual(resolve(url).func, import_view)

    def test_delete_url_resolved(self):
        url = reverse('delete', args=['0'])
        self.assertEqual(resolve(url).func, delete_view)

    def test_rest_url_resolved(self):
        url = reverse('rest')
        self.assertEqual(resolve(url).func.view_class, BooksRestView)
