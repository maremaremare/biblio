# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404

from django.views.generic import TemplateView, ListView, DetailView, View
from django.template.response import TemplateResponse
from .models import Author, Book, Category, Payment, BookFile
from pages.models import Page

import os
import tempfile
import zipfile
from datetime import datetime
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils import timezone
from urlcrypt import lib as urlcrypt
from taggit.models import Tag
from django.core.mail import send_mail
from django.core.signing import Signer
from django.core import signing


def view_cart(request):
    cart = request.session.get('cart', {})

    # rest of the view


def add_to_cart(request, item_id, quantity):
    cart = request.session.get('cart', {})
    cart[item_id] = quantity
    request.session['cart'] = cart
    # rest of the view


class CartView():

    def post(self, request, *args, **kwargs):
        if request.POST.has_key('email'):
            extensions = request.POST['extensions']
            import json
            ext_dict = json.loads(extensions)
            
            newpayment = Payment(email=request.POST['email'], )
            cart = request.session.get('cart', [])
            paymlog = ''
            newpayment.save()
            for x in cart:
                #y = Book.objects.get(id=x['book_id'])
                newpayment.books.add(Book.objects.get(id=x['book_id']))
            for k, v in ext_dict:
                bookid = k
                bookfiles = BookFile.objects.filter(book__id=bookid)
                for z in bookfiles:
                    if z.extension() == v:
                        newpayment.files.add(z)

            return TemplateResponse(request, 'payment.html', {'payment': newpayment, 'log': paymlog, 'amount': newpayment.get_amount()})

        elif request.POST.has_key('delete'):
            book_id = request.POST['delete']
            book = Book.objects.get(id=book_id)
            cart = request.session.get('cart', [])
            amount = request.session.get('amount', 0)
            if book.to_JSON() in cart:
                cart.remove(book.to_JSON())
                amount -= book.price
                request.session['cart'] = cart
                request.session['amount'] = amount
                request.session.modified = True

        elif request.POST.has_key('book_id'):
            book_id = request.POST['book_id']
            book = Book.objects.get(id=book_id)
            cart = request.session.get('cart', [])
            amount = request.session.get('amount', 0)

            if book.to_JSON() not in cart:
                cart.append(book.to_JSON())
                amount += book.price

            request.session['cart'] = cart
            request.session['amount'] = amount
            request.session.modified = True
        else:
            cart = request.session.get('cart', [])
            amount = request.session.get('amount', 0)

        return TemplateResponse(request, 'basket.html', {'cartitems': cart, 'amount': amount})
       # return HttpResponse(u'Книга добавлена в корзину')
    #template_name = "cart.html"

    def updatecart(self, cart):
        self.request.session['cart'] = cart

    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context

        context = super(CartView, self).get_context_data(**kwargs)

        cart = self.request.session.get('cart', {})

        context['cart'] = cart

        return context

    @ensure_csrf_cookie
    def dispatch(self, *args, **kwargs):
        return super(PaymentView, self).dispatch(*args, **kwargs)


class BookList(ListView, CartView):
    model = Book
    template_name = 'shoplist.html'

    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context

        context = super(BookList, self).get_context_data(**kwargs)
        context['authors'] = Author.objects.all()
        context['categories'] = Category.objects.all()
        context['books'] = Book.objects.all()
        return context


class TagView(BookList):

    def get_queryset(self):
        tag = self.kwargs['slug']
        return Book.objects.filter(tags__slug__in=[tag])

    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context

        context = super(BookList, self).get_context_data(**kwargs)

        context['authors'] = Author.objects.all()
        context['categories'] = Category.objects.all()
        context['books'] = Book.objects.all()
        context['tag'] = Tag.objects.get(slug=self.kwargs['slug']).name
        context['tagslug'] = self.kwargs['slug']

        return context


class AuthorBookList(ListView, CartView):

    def get_queryset(self):
        self.author = get_object_or_404(
            Author, slug=self.kwargs['author_slug'])
        if 'category_slug' in self.kwargs:
            return Book.objects.filter(category__slug=self.kwargs['category_slug'])
        else:
            return Book.objects.filter(author=self.author)

    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context

        context = super(AuthorBookList, self).get_context_data(**kwargs)
        context['authors'] = Author.objects.all()
        context['books'] = Book.objects.all()
        context['categories'] = Category.objects.all()
        context['author'] = Author.objects.get(
            slug=self.kwargs['author_slug'])
        if 'category_slug' in self.kwargs:
            context['category'] = Category.objects.get(
                slug=self.kwargs['category_slug'])
        return context


class PageView(DetailView):
    model = Page
    slug_field = 'url'


class BookView(DetailView, CartView):
    model = Book
    slug_field = 'slug'
    template_name = 'book.html'

    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context

        context = super(BookView, self).get_context_data(**kwargs)
        context['authors'] = Author.objects.all()
        context['categories'] = Category.objects.all()
        context['books'] = Book.objects.all()
        return context


class BuyView(BookView):
    template_name = 'buy.html'


def send_file(file, request):
    """                                                                         
    Send a file through Django without loading the whole file into              
    memory at once. The FileWrapper will turn the file object into an           
    iterator for chunks of 8KB.                                                 
    """
    filename = 'file'  # __file__ # Select your file here.
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type='text/plain')
    response['Content-Length'] = os.path.getsize(filename)
    return response


def send_zipfile(file, request):
    """                                                                         
    Create a ZIP file on disk and transmit it in chunks of 8KB,                 
    without loading the whole file into memory. A similar approach can          
    be used for large dynamic PDF files.
    """
    temp = tempfile.TemporaryFile()
    archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
    for index in range(10):
        filename = 'file'  # __file__ # Select your files here.
        archive.write(filename, 'file%d.txt' % index)
    archive.close()
    wrapper = FileWrapper(temp)
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=test.zip'
    response['Content-Length'] = temp.tell()
    temp.seek(0)
    return response


class Download_file(TemplateView):
    template_name = 'payment.html'

    def get(self, request, *args, **kwargs):
        payment = Payment.objects.get(token=self.kwargs['encrypted_id'])
        payment.link_activated = True
        payment.save()
        temp = tempfile.TemporaryFile()
        archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
        for bfile in payment.files.all():
            # __file__ # Select your files here.
            filename = bfile.bookfile
            archive.write(filename.path, filename.name)
        archive.close()
        wrapper = FileWrapper(temp)
        response = HttpResponse(wrapper, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=biblioland.zip'
        response['Content-Length'] = temp.tell()
        temp.seek(0)
        return response


def test(request):

    request.session.set_test_cookie()
    return HttpResponse('hi!')


class PaymentView(TemplateView):

    template_name = 'payment.html'

    def get_link(self, payment):

        if payment.status == u'success' and (not payment.link_activated):

            if (not payment.token) or (payment.token_expires < timezone.now()):
                payment.generate_token()

        return payment.get_link()

    def get_template(self, payment):
        if payment.status == 'success':
            return 'payment_success.html'
        elif payment.status == 'canceled':
            return 'payment_canceled.html'
        elif payment.status == 'waitAccept':
            return 'payment_pending.html'
        else:
            return 'payment_error.html'

    def sendmail(self, payment):

        __dir__ = os.path.dirname(os.path.abspath(__file__))

        if payment.status == 'success':
            mailfile = "mailsuccess.txt"
            status = "оплачен"
        if payment.status == 'waitAccept':
            mailfile = "mailpending.txt"
            status = "в обработке"
        if payment.status == 'canceled':
            mailfile = "mailcancel.txt"
            status = "отменен"

        signer = Signer()
        value = signing.dumps({"id": payment.paymentid})

        link = 'http://biblio.land/payment/' + value

        with open(os.path.join(__dir__, mailfile), "r") as myfile:
            message = myfile.read().format(
                link, payment.email, payment.paymentid)

        send_mail('Магазин электронных книг Библиоленд. Заказ №{0} {1}.'.format(
            payment.paymentid, status), message, 'shop@biblio.land', (payment.email,))

    def post(self, request):

        if request.POST['ik_pm_no']:
            payment_id = request.POST['ik_pm_no']
            payment = Payment.objects.get(paymentid=payment_id)
            payment.status = request.POST['ik_inv_st']
            payment.system = request.POST['ik_pw_via']
            payment.amount = request.POST['ik_am']

            payment.save()
            self.sendmail(payment)
            response = TemplateResponse(
                request, self.get_template(payment), {'payment': payment, 'link': self.get_link(payment), })
            response.status_code = '200'
            return response

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(PaymentView, self).dispatch(*args, **kwargs)

    def get(self, *args, **kwargs):
        signer = Signer()
        value = signing.loads(self.kwargs['encrypted_id'])
        paymentid = value['id']
        payment = Payment.objects.get(paymentid=paymentid)
        response = TemplateResponse(
            self.request, self.get_template(payment), {'payment': payment, 'link': self.get_link(payment), })
        return response
