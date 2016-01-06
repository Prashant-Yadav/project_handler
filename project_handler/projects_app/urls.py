from . import views

from django.conf.urls import url


urlpatterns = [
				url(r'^$', views.index, name='index'),
				url(r'^header/$', views.header_info, name='header_info'),
				url(r'^footer/$', views.footer_info, name='footer_info'),
				url(r'^registration/$', views.registration, name='registration'),
				url(r'^login/$', views.login, name='login'),
				url(r'^logout/$', views.login, name='logout'),
				]