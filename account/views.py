from django.shortcuts import render,redirect
from book.models import Book,Author
from .models import Cart,CartItem
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
import stripe
from django.conf import settings
from django.urls import reverse



def listBooks(request):
    username=request.user.username
    books=Book.objects.all()
    paginator=Paginator(books,4)
    page_number=request.GET.get('page')
    try:
        page=paginator.get_page(page_number)
    except EmptyPage:
        page=paginator.page(page_number.num_pages)
    context={'books':books,'page':page,
             'username':username
            
             }
    return render(request,'user/list_book.html',context)

def detailBook(request,book_id):
    username=request.user.username
    book=Book.objects.get(id=book_id)
    context={
      
        'book':book,
        'username':username
    }
    return render(request,'user/detail_book.html',context)

def searchBook(request):
    username=request.user.username
    query=None
    books=None
    if 'name' in request.GET:
        query=request.GET.get('name')
        books=Book.objects.filter(Q(title__icontains=query) | Q(author__name__icontains=query))
    else:
        books=[]
    context={
        'books':books,
        'query':query,
        'username':username
        
        

    }
    return render(request,'user/search_book.html',context)


def userRegister(request):
    
    if request.method == 'POST':
        userName=request.POST.get('userName')
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        email=request.POST.get('email')
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')
       
        if password == cpassword :
            if User.objects.filter(username=userName).exists():
                messages.info(request,'User name already exist')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'email already exist')
                return redirect('register')
            else:
                user=User.objects.create_user(username=userName,first_name=fname,
                                              last_name=lname,email=email,password=password,
                                            )
                user.save()
                messages.info(request,'registered successfully')
                return redirect('login')
            
        else:
            messages.info(request,'password not match with confirm password')
            return redirect('register')
    return render(request,'account/register.html')

def userLogin(request):
    if request.method == 'POST':
        username=request.POST.get('username') 
        password=request.POST.get('password')
        user=auth.authenticate(username=username,password=password)
        print(user)
        if user is not None:
            if username == 'admin' and password == '1234':
                login(request,user)
                return redirect('list-book')
            
            else:
                login(request,user)
                return redirect('book-list-user')
        
            
        else:
            messages.info(request,'Invalid credential')
            return redirect('login')
    return render(request,'account/login.html')

def userLogout(request):
    logout(request)
    return redirect('login')
def add_to_cart(request,book_id):
    book=Book.objects.get(id=book_id)
    
    try:
        if request.user.is_authenticated:

            if book.quantity > 0:
                cart,created=Cart.objects.get_or_create(user=request.user)
                cart_item,item_created=CartItem.objects.get_or_create(cart=cart,book=book)
                if not item_created:
                    cart_item.quantity +=1
                    cart_item.save()
        return redirect('view-cart')
    except :
        messages.error('login required')
    
def view_cart(request):
    username=request.user.username
    cart,create=Cart.objects.get_or_create(user=request.user)
    cart_items=cart.cartitem_set.all()
    cart_item=CartItem.objects.all()
    total_price=sum(item.quantity * item.book.price  for item in cart_items)
    total_count=cart_items.count()
    context={
        'cart_item':cart_item,
        'cart_items': cart_items,
        'total_price':total_price,
        'total_count':total_count,
        'username':username

    }
    return render(request,'user/cart.html',context)

def increase_quantity(request,item_id):
    cart_item=CartItem.objects.get(id=item_id)

    if cart_item.quantity < cart_item.book.quantity :
        cart_item.quantity +=1
        cart_item.save()
    return redirect('view-cart') 

def decrease_quantity(request,item_id):
    cart_item=CartItem.objects.get(id=item_id)
    if cart_item.quantity >1 :
        cart_item.quantity -=1
        cart_item.save()
    return redirect('view-cart')

def delete_cart_item(request,item_id):
    try:
        cart_item=CartItem.objects.get(id=item_id)
        cart_item.delete()
    except cart_item.DoesNotExist:
        pass
    return redirect('view-cart')


def create_checkout_session(request):
    cart_items=CartItem.objects.all()
    if cart_items :
        stripe.api_key = settings.STRIPE_SECRET_KEY
        line_items=[]
        for cart_item in  cart_items:
            if cart_item.book :
                line_item = {
                    'price_data':{
                        'currency' : 'INR',
                        'unit_amount' : int(cart_item.book.price*100),
                        'product_data' : {
                            'name' : cart_item.book.title
                        }
                    },
                    'quantity' : cart_item.quantity
                }
                line_items.append(line_item)
        if line_items:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types= ['card'],
                line_items=line_items,
                mode='payment',
                success_url=request.build_absolute_uri(reverse('success')),
                cancel_url=request.build_absolute_uri(reverse('cancel')),
            )
            return redirect(checkout_session.url,code=303)
def success(request):
    cart_items=CartItem.objects.all()

    for cart_item in cart_items:
        product = cart_item.book
        if product.quantity >= cart_item.quantity:
            product.quantity -= cart_item.quantity
            product.save()
    cart_items.delete()
    return render(request,'cart/success.html')
def cancel(request):
    return render(request,'cart/cancel.html')





                

             

