from django.views.generic import TemplateView
from shop.models import Author, Book
from shop.views import CartView


class HomePageView(TemplateView, CartView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['authors'] = Author.objects.all()
        context['books'] = Book.objects.all()
        return context
