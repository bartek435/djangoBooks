from rest_framework.response import Response
from rest_framework.views import APIView

from books.models import BookModel
from books.views import get_data_from_query
from .serializers import BookSerializer

class BooksRestView(APIView):
    def get(self, request):
        kwargs = get_data_from_query(request.GET.items())
        kwargs.pop('format__icontains', '')
        books = BookModel.objects.all().filter(**kwargs)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
