from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from rosetta import urls as rosetta_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail_feeds.feeds import BasicFeed, ExtendedFeed
from wagtail.core import views

from .views import robots, error_404, worker
from .cms.amp import urls as wagtail_amp_urls

views.serve.csrf_exempt = True

urlpatterns = [
    url(r'^robots\.txt$', robots),
    url(r'^404$', error_404),
    url(r'^sitemap\.xml$', sitemap),
    url(r'^worker(?P<version>.+).js$', worker),
    url(r'^admin_W3cJ32mq63V45CLvmjNbsqSJ32mq63V45CL/', admin.site.urls),
    url(r'^rosetta_WoQtYMRmgLV9iId6VEfAn1VxpH7aoOUeg/', include(rosetta_urls)),
    url(r'^wagtail_WSQtYMxmgLV9iIn6VE3An1VxpH9aoOUeg/', include(wagtailadmin_urls)),
    url(r"^amp/", include(wagtail_amp_urls)),
    url(r"^", include(wagtail_urls)),
    url(r'^articles/rss/basic$', BasicFeed(), name='basic_feed'),
    url(r'^articles/rss/extended$', ExtendedFeed(), name='extended_feed'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
