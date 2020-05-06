from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^register/$',views.registerPage, name = "register"),
    url(r'^login/$',views.loginPage, name = "login"),
    url(r'^logout/$',views.logoutUser, name = "logout"),
    url(r'^about/$',views.aboutpage, name = "about"),
]
