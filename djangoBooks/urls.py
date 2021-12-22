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
from django.urls import path
from books.rest_api.views import BooksRestView
from books.views import books_view, delete_view, edit_view, import_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', books_view, name ='home'),
    path('home/', books_view, name ='home'),
    path('edit/<int:book_id>', edit_view, name ='edit'),
    path('edit/', edit_view, name ='edit'),
    path('import/', import_view, name ='import'),
    path('delete/<int:book_id>', delete_view, name ='delete'),
    path('rest_books',BooksRestView.as_view(), name = 'rest')
]
