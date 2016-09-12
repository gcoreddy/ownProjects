"""sqa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
import django

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import sqadashboard.views
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', sqadashboard.views.getQuery, name='getQuery'),

	url(r'^query/(?P<query_id>\d+)/detail.html$', sqadashboard.views.query_detail, name='query_detail'),
	url(r'^query/(?P<compare_id>\d+)/compare.html$', sqadashboard.views.compare_detail, name='compare_detail'),
	url(r'^query/(?P<plot_id>\d+)/graph.html$', sqadashboard.views.plot_detail, name='plot_detail'),
	#url(r'^graph.*$', sqadashboard.views.plot_detail, name='plot_detail'),
	# Link the view myblog.views.post_upload to URL post/upload.html
	url(r'^query/upload.html$', sqadashboard.views.getQuery, name='getQuery'),
	#url(r'^admin/doc/', include(django.contrib.admindocs.urls)),

    # Uncomment the next line to enable the admin:
	url(r'^admin/',admin.site.urls),
)