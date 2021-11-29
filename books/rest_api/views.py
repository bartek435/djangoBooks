import datetime

from rest_framework.response import Response
from rest_framework.views import APIView

from books.models import BookModel
from .serializers import BookSerializer

class BooksRestView(APIView):
    def get(self, request):
        kwargs = {}
        for key,value in request.GET.items():
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
        books = BookModel.objects.all().filter(**kwargs)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
