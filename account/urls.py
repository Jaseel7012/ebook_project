from django.urls import path
from . import views
urlpatterns = [
    path('register/',views.userRegister,name='register'),
  path('',views.userLogin,name='login'),
  path('logout/',views.userLogout,name='user-logout'),
 path('user/book-list/',views.listBooks,name='book-list-user'),
   path('user/book-detail/<int:book_id> ',views.detailBook,name='book-detail'),
    path('user/search-book/ ',views.searchBook,name='search-books'),
path('view-cart/',views.view_cart,name='view-cart'),
path('increase/<int:item_id>',views.increase_quantity,name='increase-quantity'),
path('decrease/<int:item_id>',views.decrease_quantity,name='decrease-quantity'),
path('remove/<int:item_id>',views.delete_cart_item,name='romove-item'),
path('add-cart-item/<int:book_id>',views.add_to_cart,name='add-cart-item'),
path('create-checkout-session/',views.create_checkout_session,name='create-checkout-session'),
path('success/',views.success,name='success'),
path('cancel',views.cancel,name='cancel')

 
]