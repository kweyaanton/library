from django import forms
from django.forms import ModelForm
from .models import Book,Issued_book


#create an add book form
class bookform(ModelForm):
    class Meta:
        model=Book
        fields=('book_title','description','ISBN','author','book_cover','added_by','edition','subject_area')

    def __init__(self,*args,**kwargs):
        super(bookform,self).__init__(*args,**kwargs)

        self.fields['book_title'].widget.attrs['class']='form-control'
        self.fields['description'].widget.attrs['class']='form-control'
        self.fields['author'].widget.attrs['class']='form-control'
        self.fields['book_cover'].widget.attrs['class']='form-control'
        self.fields['added_by'].widget.attrs['class']='form-control'
        self.fields['edition'].widget.attrs['class']='form-control'
        self.fields['subject_area'].widget.attrs['class']='form-control'

class Issue_book(ModelForm):
    class Meta:
        model=Issued_book
        fields=('user','book','return_date','fine','return_status')

 