from django.shortcuts import render, redirect
from .models import Book,Borrowed_book
from django.contrib.auth.models import User
from .forms import bookform,Issue_book
from django.http import HttpResponseRedirect
from django.contrib import messages
import datetime 
#import pdf stuff
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

#import paginator stuff
from django.core.paginator import Paginator

app_name = 'books'


def welcome(request):
    return render(request,'books/welcome_page.html')


#Student views
def my_book(request):
    context={}
    return render(request,'books/My_books.html',context) 


def payments_student(request):
    return render(request,'books/payments_student.html')


def Home_student(request):
    books=Book.objects.all().order_by('Date_added')
    #Setup pagination
    p=Paginator(Book.objects.all(),5)
    page=request.GET.get('page')
    books_list=p.get_page(page)
    pages="p"*books_list.paginator.num_pages
    context={'books':books,
    'books_list':books_list,
    'pages':pages}
    return render(request,'books/home_student.html',context)


def search_books(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        books = Book.objects.filter(book_title__contains=searched)
        return render(request,'books/search_books.html',
        {'searched':searched,
        'books':books})
    else:
        return render(request,'books/search_books.html')

def book_student(request, pk):
    book=Book.objects.get(id=pk)
    context = {'book': book}      
    return render(request,'books/book_student.html',context)

def Borrow(request,id):
    book = Book.objects.get(id=id)

    return render(request,'books/borrow_book.html',{
        'book': book,
        'book_id': id,
        'title': 'Borrow a Book'
    })

def Borrow_book(request,id):
    user_id=request.user.id
    book=Book.objects.get(id=id)
    b=Book.objects.all()
    if b.status =="AVAILABLE":
        b.status=='UNAVAILABLE'
        b.save()
    user=User.objects.get(id=user_id)
    borrowed_book=Borrowed_book.objects.create(user=user,book=book,fine=0,date_borrowed=datetime.datetime.now())
    borrowed_book.save()
    
    messages.info(request,("book was borrowed successfully...."))
    return redirect('books:Home_student')

#Librarian views
def Home(request):
    books=Book.objects.all().order_by('Date_added')
    #Setup pagination
    p=Paginator(Book.objects.all(),5)
    page=request.GET.get('page')
    books_list=p.get_page(page)
    pages="p"*books_list.paginator.num_pages
    context={'books':books,
    'books_list':books_list,
    'pages':pages}
    return render(request,'books/home.html',context)

def add_book(request):
    submitted=False
    if request.method =="POST":
        form =bookform(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            #return redirect('books:Home')
            return HttpResponseRedirect('/add_book?submitted=True')
    else:
        form=bookform
        if 'submitted' in request.GET:
            submitted=True
    form=bookform   
    context={'form':form,'submitted':submitted}
    #messages.info(request,("book was added successfully...."))
    return render(request,'books/add_book.html',context)

def borrowed_books(request):
    Books=Borrowed_book.objects.all()
    context={'Books':Books}
    return render(request,'books/borrowed_books.html',context)

def requested_books(request):
    books=Borrowed_book.objects.all()
    context={'books':books}
    return render(request,'books/requested_books.html',context)


def book_librarian(request, pk):
    book=Book.objects.get(id=pk)
    context = {'book': book}      
    return render(request,'books/book_librarian.html',context)

def update_book(request,id):
    book=Book.objects.get(pk=id)
    form=bookform(request.POST or None,request.FILES or None,instance=book)
    if form.is_valid():
        form.save()
        #messages.info(request,("Book updated successfully...."))
        return redirect('books:Home')
    return render(request,'books/update_book.html',
    {'book':book,
    'form':form})   

def delete_book(request,id):
    book=Book.objects.get(pk=id)
    book.delete()
    return redirect('books:Home')

def search_books_librarian(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        books=Book.objects.filter(book_title__contains=searched)
        return render(request,'books/search_books_librarian.html',
        {'searched':searched,
        'books':books})
    else:
        return render(request,'books/search_books_librarian.html')  

def Issue(request,id):
    borrowed_book = Borrowed_book.objects.get(id=id)

    return render(request,'books/view_requested_book.html',{
        'book': borrowed_book,
        'book_id': id,
    })

def Issue_book(request):
    #book=Book.objects.get(pk=id)
    form=Issue_book

#generate a pdf file of booklist
def book_report(request):
    #create bytestream buffer
    buf=io.BytesIO()
    #create canvas
    canv=canvas.Canvas(buf,pagesize=letter,bottomup=0)
    #create text object
    textob= canv.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica",14)
  
    #designate model
    books=Book.objects.all()
    #blank list
    lines=[]
    for book in books:
        lines.append(book.book_title)
        lines.append(book.description)
        lines.append(book.author)
        lines.append(book.subject_area)
        lines.append("")
        
    #loop
    for line in lines:
        textob.textLine(line)

    #finish up
    canv.drawText(textob)
    canv.showPage()
    canv.save()
    buf.seek(0)

    #return response
    return FileResponse(buf,as_attachment=True,filename='report.pdf')    
