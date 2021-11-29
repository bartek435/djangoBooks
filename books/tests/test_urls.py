from django.test import SimpleTestCase
from django.urls import reverse, resolve

from books.views import  booksView, deleteView, editView, importView
from books.rest_api.views import BooksRestView

class TestUrls(SimpleTestCase):

    def testBooksUrlResolved(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, booksView)

    def testEditUrlResolved(self):
        url = reverse('edit')
        self.assertEquals(resolve(url).func, editView)

    def testImportUrlIsResolved(self):
        url = reverse('import')
        self.assertEquals(resolve(url).func, importView)

    def testDeleteUrlResolved(self):
        url = reverse('delete',args=['0'])
        self.assertEquals(resolve(url).func, deleteView)

    def testRestUrlResolved(self):
        url = reverse('rest')
        self.assertEquals(resolve(url).func.view_class, BooksRestView)
