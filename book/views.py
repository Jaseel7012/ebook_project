from django.shortcuts import render,redirect
from .models import Author,Book
from django.contrib import messages
from . import forms
from django.core.paginator import Paginator,EmptyPage
from django.db.models import Q
from django.contrib.auth import logout

# Create your views here.
#Author View
def addAuthor(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        author=Author(name=name)

        author.save()
        messages.success(request,'Author Added Successfully')
        return redirect('add-author')

    return render(request,'author/add_author.html')



#Book view
def createBook(request):
    if request.method == 'POST':
        form=forms.BookCreateForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Book Added Successfully')
            return redirect('list-book')
        else:
            form=forms.BookCreateForm()
    else:
        form=forms.BookCreateForm()
    return render(request,'book/create.html',{'form':form})

def listBook(request):
    books=Book.objects.all()
    paginator=Paginator(books,4)
    page_number=request.GET.get('page')
    try:
        page=paginator.get_page(page_number)
    except EmptyPage:
        page=paginator.page(page_number.num_pages)

    return render(request,'book/list.html',{'books':books,'page':page})


def detailBook(request,book_id):
    book=Book.objects.get(id=book_id)
    print(book.title)
    return render(request,'book/detail.html',{'book':book})


def updateBook(request,book_id):
    book=Book.objects.get(id=book_id)
    if request.method == 'POST':
        form=forms.BookCreateForm(request.POST,request.FILES,instance=book)

        if form.is_valid():
            form.save()
            messages.success(request,'Updated Successfully')
            return redirect('list-book')
        
    else:
        form=forms.BookCreateForm(instance=book)



    return render(request,'book/update.html',{'form':form})


def deleteBook(request,book_id):
    book=Book.objects.get(id=book_id)
    if request.method == 'POST':

        book.delete()
        messages.info(request,'Deleted successfully')
        return redirect('list-book')
    return render(request,'book/delete.html',{'book':book})


def searchBook(request):
    query=None
    books=None
    if 'name' in request.GET:
        query=request.GET.get('name')
        books=Book.objects.filter(Q(title__icontains=query) | Q(author__name__icontains=query))
    else:
        books=[]
    context={
        'books':books,
        'query':query
    }
    return render(request,'book/search_book.html',context)
#base view

def adminLogout(request):
    logout(request)
    return redirect('login-user')
def index(request):
    return render(request,'base.html')