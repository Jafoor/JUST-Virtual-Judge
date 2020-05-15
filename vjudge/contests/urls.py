from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^contest/$',views.contestpage, name = "contest"),
    url(r'^createcontest/$',views.createcontestpage, name = "createcontest"),
    url(r'^contesttask/(?P<pk>\d+)/$', views.contesttask, name = "contesttask"),
    url(r'^contest/tasks/(?P<pk>\d+)/$', views.tasks, name = "tasks"),
    url(r'^setproblem/(?P<pk>\d+)/$',views.setproblem, name = "setproblem"),
    url(r'^contest/(?P<pk1>\d+)/problem/(?P<pk2>\d+)/$', views.contestproblem, name = "contestproblem"),
    url(r'^ranklist/(?P<pk>\d+)/$',views.ranklist, name = "ranklist"),
    url(r'^submission/(?P<pk>\d+)/$',views.submission, name = "submission"),
    url(r'^viewsubmittedcode/(?P<pk>\d+)/$',views.viewsubmittedcode, name = "viewsubmittedcode"),
]
