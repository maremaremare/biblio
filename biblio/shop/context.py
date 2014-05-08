from .models import Book, Payment
from django.db import models


def write_context(request):
    popular = Book.objects.all() \
        .annotate(payments=models.Count('payment')) \
        .order_by('-payments')
    return {'popular': popular[:5],  'new': Book.objects.all()[:5]}
