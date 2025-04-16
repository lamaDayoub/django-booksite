from django.urls import path
from .views import BookDetailView,BookList,BookshelveView

urlpatterns=[
    path('shelve/',BookshelveView.as_view(),name='shelve-book'),
    path('',BookList.as_view(),name='list-books'),
    path('<int:id>/',BookDetailView.as_view(),name='book-detail'),
]