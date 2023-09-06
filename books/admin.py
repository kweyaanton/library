from django.contrib import admin
from .models import Book,Borrowed_book,Issued_book


class BookAdmin(admin.ModelAdmin):
    list_display = ('book_title','author','edition','Date_added','subject_area')
    ordering=('book_title',)
    search_fields=('book_title','id')

admin.site.register(Book,BookAdmin)
admin.site.register(Borrowed_book)
admin.site.register(Issued_book)