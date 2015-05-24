from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
import os, sys
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ideapub.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include('catalog.urls')),
    url(r'^sales/', include('sales.urls')),
    url(r'^payments/', include('payments.urls')),
    url(r'^pages/', include('pages.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url (r'^ckeditor/', include('ckeditor.urls')),
    url(r'^media/(?P<path>.*)$', 
        'django.views.static.serve', 
        {'document_root': os.path.join(os.path.dirname (__file__), 'media') }),

    url (r'^admin/', include(admin.site.urls)),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
