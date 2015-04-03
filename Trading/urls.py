from django.conf.urls import patterns, include, url
from django.contrib import admin
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'colewood.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^(?P<acct_num>\d+)/(?P<acct_server>.*)/$', views.set_equity, name='set_equity'),
    #url(r'^(\d+)/(.*)/$', views.MyView, name='test_equity'),
    url(r'^insert/equity/', views.equity_test, name='equity_test'),
    url(r'^admin/', include(admin.site.urls)),
    
)
