from datetime import date
from django.test import TestCase, Client
from django.urls import reverse
from django.forms.models import model_to_dict

from books.models import BookModel

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.books_url = reverse('home')
        self.search_url = self.books_url+'?title=app&language=eng'
        self.delete_url = reverse('delete', args=['1'])
        self.edit_url = reverse('edit')
        self.edit_url_1 = reverse('edit', args=['1'])
        self.rest_url = reverse('rest')
        self.import_url = reverse('import')

        self.book_1 = BookModel.objects.create(
            title='Books App',
            author='me',
            date="2020-03-03",
            isbn='1234567890123',
            pages=20,
            cover='http://google.com',
            language='eng'
        )
    def test_books_view(self):
        response = self.client.get(self.books_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books_view.html')

        response = self.client.get(self.search_url)
        self.assertEqual(response.status_code, 200)

    def test_edit_view_get(self):
        response = self.client.get(self.edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_view.html')

        response = self.client.get(self.edit_url_1)
        self.assertEqual(response.status_code, 200)

    def test_edit_view_post(self):
        test_dict = {
            'title': 'Test Title',
            'author': 'me',
            'date': date(2020, 3, 3),
            'isbn': '1112223334555',
            'pages': 111,
            'cover': 'http://google.com',
            'language': 'eng'
        }
        response = self.client.post(self.edit_url, test_dict)
        self.assertEqual(response.status_code, 302)
        obtained_dict = model_to_dict(BookModel.objects.get(id=2))
        obtained_dict.pop('id')
        self.assertEqual(obtained_dict, test_dict)

    def test_edit_view_1_post(self):
        test_dict = {
            'title': 'Books App Edited',
            'author': 'me',
            'date': date(2020, 3, 3),
            'isbn': '1234567890123',
            'pages': 20,
            'cover': 'http://google.com',
            'language': 'eng'
        }
        response = self.client.post(self.edit_url_1, test_dict)
        self.assertEqual(response.status_code, 302)
        obtained_dict = model_to_dict(BookModel.objects.get(id=1))
        obtained_dict.pop('id')
        self.assertEqual(obtained_dict, test_dict)

    def test_edit_view_no_data_post(self):
        response = self.client.post(self.edit_url_1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(BookModel.objects.count(), 1)

    def test_delete_view(self):
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(BookModel.objects.count(), 0)

    def test_search_view(self):
        BookModel.objects.create(
            title='Test title',
            author='me',
            date="2020-01-23",
            isbn='1234567890123',
            pages=220,
            cover='http://google.com',
            language='eng'
        )
        response = self.client.get(self.search_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['data'][0],
            BookModel.objects.get(id=1)
        )

    def test_import_view_get(self):
        response = self.client.get(self.import_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'import_view.html')

    def test_import_view_post(self):
        BookModel.objects.all().delete()
        response = self.client.post(self.import_url, {'q':'Poland'})
        self.assertEqual(response.status_code, 302)
        self.assertGreater(BookModel.objects.count(), 0)

    def test_import_view_no_data_post(self):
        BookModel.objects.all().delete()
        response = self.client.post(self.import_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(BookModel.objects.count(), 0)
    