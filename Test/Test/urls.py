"""Test URL Configuration

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
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from weibo import views

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index),
    url(r'^mylogin/', views.mylogin),
    url(r'^mysignup/', views.mysignup),
    url(r'^mylogout/', views.mylogout),
    url(r'^send/', views.send),
    url(r'^discover/', views.discover),
    url(r'^getprofile/?', views.getprofile),
    url(r'^follow/', views.follow),
    url(r'^comment/?', views.comment),
    url(r'^scomment/', views.sendcomment),
    url(r'^listfollow/?$', views.listfollow),
    url(r'^listfollower/?$', views.listfollower),
    url(r'^delcontent/?$', views.delcontent),
    url(r'^delcomment/?$', views.delcomment),
    url(r'^editprofile/$', views.editprofile),
    url(r'^updateprofile/$', views.updateprofile),
]
