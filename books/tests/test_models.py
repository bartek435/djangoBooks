from django.test import TestCase
from books.models import BookModel

class TestBookModel(TestCase):

    def setUp(self):
        self.book = BookModel.objects.create(
            title = 'Books App',
            author = 'me',
            date = "2020-03-03",
            isbn = '1234567890123',
            pages = 20,
            cover = 'http://google.com',
            language = 'eng'
        )
