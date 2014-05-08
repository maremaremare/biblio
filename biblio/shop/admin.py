from django.contrib import admin
from shop.models import Author, Category, Book, Payment, BookFile


class BookFileInline(admin.StackedInline):
    model = BookFile
    extra = 0


class CategoryInline(admin.StackedInline):
    model = Category
    extra = 0


class AuthorAdmin(admin.ModelAdmin):
    inlines = [
        CategoryInline
    ]


class BookAdmin(admin.ModelAdmin):
    inlines = [BookFileInline]


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('paymentid', 'status', 'paid_via', 'email', 'amount')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category)
admin.site.register(Book, BookAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(BookFile)
