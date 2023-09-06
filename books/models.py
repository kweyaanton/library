from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


class Book(models.Model):

    class BookStatusChoices(models.TextChoices):
        AVAILABLE = "AVAILABLE", ("Available")
        UNAVAILABLE = "UNAVAILABLE", ("Unavailable")
        BOOKED = "BOOKED", ("Booked")

    book_title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    edition = models.CharField(max_length=255)
    Date_added = models.DateField(auto_now_add=True)
    subject_area = models.CharField(max_length=255)
    book_cover = models.ImageField(upload_to = 'images/')
    added_by=models.CharField(max_length=100,null=True,blank=True)
    date_updated=models.DateTimeField(auto_now=True)
    ISBN= models.CharField(null=True, blank= True,max_length=200)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, default="AVAILABLE", choices=BookStatusChoices.choices)
    def __str__(self):
        return self.book_title

    def delete(self,*args,**kwargs):
        self.book_cover.delete()
        super().delete(*args,**kwargs)    


class Borrowed_book(models.Model):

    class ReturnStatusChoices(models.TextChoices):
        BOOKED = "BOOKED", ("Booked")

    user=models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    date_borrowed=models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, default="BOOKED", choices=ReturnStatusChoices.choices) 


class Issued_book(models.Model):

    class ReturnStatusChoices(models.TextChoices):
        BOOKED = "BOOKED", ("Booked")
        TAKEN = "TAKEN", ("Taken")
        RETURNED = "RETURNED", ("Returned")

    user=models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    book = models.ForeignKey(Borrowed_book,on_delete=models.CASCADE)
    date_issued=models.DateTimeField(auto_now_add=True)
    return_date=models.DateTimeField(null=True)
    date_returned=models.DateTimeField(null=True)
    fine = models.IntegerField(null=True, blank=True)
    return_status = models.CharField(max_length=15, default="BOOKED", choices=ReturnStatusChoices.choices)

'''    def Fine_calc(self):
        Issued_book.return_date+=1
        days=Issued_book.date_returned - Issued_book.return_date
        if days>=3:
            return Issued_book.fine==5000

        elif days>=10:
            return Issued_book.fine==15000
        else:
            return Issued_book.fine==0 
        Issued_book.save()
'''