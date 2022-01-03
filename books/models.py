from django.db import models

# Create your models here.
class BookModel(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    date = models.DateField()
    isbn = models.CharField(max_length=13, blank=True, null=True)
    pages = models.PositiveSmallIntegerField()
    cover = models.URLField()
    language = models.CharField(max_length=25)
