from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from shop.views import Download_file, test, BookList, AuthorBookList, BookView, BuyView, PageView, TagView, PaymentView
from homepage.views import HomePageView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.http import HttpResponse

admin.autodiscover()


def yandex(request):
    return HttpResponse('500b3fb7d9ea')


urlpatterns = patterns('',
                       # url(r'^payment?ik_co_id=(?P<ik_co_id>\S+)&ik_inv_id=(?P<ik_inv_id>\S+)&ik_inv_st=(?P<ik_inv_st>\S+)&ik_inv_crt=(?P<ik_inv_crt>\S+)&ik_inv_prc=(?P<ik_inv_prc>\S+)&ik_pm_no=(?P<ik_pm_no>\S+)&ik_pw_via=(?P<ik_pw_via>\S+)&ik_am=(?P<ik_am>\S+)&ik_cur=(?P<ik_cur>\S+)&ik_co_rfn=(?P<ik_co_rfn>\S+)&ik_ps_price=(?P<ik_ps_price>\S+)&ik_desc=(?P<ik_desc>\S+)$)',
                       url(r'^$',
                           HomePageView.as_view()),
                       url(r'^shop/tags/(?P<slug>\w+)$',
                           TagView.as_view(), name='tags'),
                       url(r'^shop/books/(?P<slug>\w+)/buy/$',
                           BuyView.as_view(), name='buy'),
                       url(r'^shop/books/(?P<slug>\w+)$',
                           BookView.as_view(), name='book'),
                       url(r'^shop$', ensure_csrf_cookie(BookList.as_view(template_name='shoplist.html')),
                           name='shop'),

                       url(r'^shop/(?P<author_slug>\w+)$',
                           AuthorBookList.as_view(
                               template_name='shoplist.html'), name='shop-author'),
                       url(r'^shop/(?P<author_slug>[\w-]+)/(?P<category_slug>[\w-]+)$',
                           AuthorBookList.as_view(
                               template_name='shoplist.html'), name='shop-author-category'),
                       url(r'^pages/(?P<slug>\w+)$',
                           PageView.as_view(template_name='page.html')),
                       url(r'^payment$', PaymentView.as_view()),
                       url(r'^payment/(?P<encrypted_id>\S+)$',
                           PaymentView.as_view()),
                       url(r'^download/(?P<encrypted_id>\S+)/$',
                           Download_file.as_view()),
                       url(r'^test$',
                           test),
                       url(r'^b2087c774862.html$', yandex),
                       # grappelli URLS
                       url(r'^grappelli/', include('grappelli.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       )
