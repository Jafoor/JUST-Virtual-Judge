from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^dashboard/$',views.dashboard, name = "dashboard"),
    url(r'^addproblem/$',views.addproblem, name = "addproblem"),
    url(r'^allproblems/$',views.allproblems, name = "allproblems"),
    url(r'^viewproblems/$',views.viewproblems, name = "viewproblems"),
    url(r'^problem/(?P<pk>\d+)/$',views.problem, name = "problem"),
    url(r'^submit/$',views.submit, name = "submit"),
]
