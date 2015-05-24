from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from catalog.views import *

urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='catalog_index'),
    url(r'^categories/(?P<slug>[\w-]+)/$', CategoryBooksView.as_view(), {'page_num': 1}, name='catalog_category'),
    url(r'^categories/(?P<slug>[\w-]+)/(?P<page_num>\d+)/$', CategoryBooksView.as_view(), name='catalog_category'),
    url(r'^publishers/(?P<slug>[\w-]+)/$', PublishersBooksView.as_view(),
        {'page_num': 1}, name='catalog_publisher'),
    url(r'^publisher/(?P<slug>[\w-]+)/(?P<page_num>\d+)/$',
        PublishersBooksView.as_view(), name='catalog_publisher'),
    url(r'^search/$', SearchBooksView.as_view(), {'page_num': 1}, name='catalog_search'),
    url(r'^search/(?P<page_num>\d+)/$', SearchBooksView.as_view(), name='catalog_search'),
    url(r'^book/(?P<book_id>\d+)/(?P<slug>[\w-]+)/$', BookDetailView.as_view(), name='catalog_book'),
    url(r'^change_currency/$', ChangeCurrencyView.as_view(), name='catalog_change_currency'),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
