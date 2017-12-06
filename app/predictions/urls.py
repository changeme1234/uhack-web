from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^start_end$', views.StartEnd.as_view(), name="start_end"),
    url(r'^history$', views.History.as_view(), name="history"),
    url(r'^companies$', views.CompanyList.as_view(), name="companies"),
    url(r'^date$', views.GenerateDate.as_view(), name="date"),
    url(r'^save$', views.Save.as_view(), name="save"),
    url(r'^balance$', views.GetBalance.as_view(), name="balance"),
    url(r'^$', views.Index.as_view(), name='index'),
]
