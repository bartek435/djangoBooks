"""djangoBooks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from books.rest_api.views import BooksRestView
from books.views import booksView, deleteView, editView, importView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', booksView, name ='home'),
    path('home/', booksView, name ='home'),
    path('edit/<int:id>', editView, name ='edit'),
    path('edit/', editView, name ='edit'),
    path('import/', importView, name ='import'),
    path('delete/<int:id>', deleteView, name ='delete'),
    path('rest_books',BooksRestView.as_view(), name = 'rest')
]
