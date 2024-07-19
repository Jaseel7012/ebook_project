from django.urls import path
from . import views
urlpatterns = [
 path('author/',views.addAuthor,name='add-author'),
    path('create/',views.createBook,name='add-book'),
    path('list/',views.listBook,name='list-book'),
    path('detail/<int:book_id>/',views.detailBook,name='detail-book'),
       path('delete/<int:book_id>/',views.deleteBook,name='delete-book'),
       path('update/<int:book_id>/',views.updateBook,name='book-update'),
       path('search',views.searchBook,name='search-book')
 
]