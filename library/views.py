from django.shortcuts import redirect, render
from catalog.models import BookInstance, Book, Author, Language, Genre


def index(request):
    return redirect('catalog/login')
