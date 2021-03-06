from django.conf.urls import patterns, include, url
from django.contrib import admin
import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'colewood.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^(?P<acct_num>\d+)/(?P<acct_server>.*)/$', views.set_equity, name='set_equity'),
    #url(r'^(\d+)/(.*)/$', views.MyView, name='test_equity'),
    url(r'^equity/(?P<account_number>\d+)/$', views.candle_chart, name='candle_chart'),
    url(r'^equity/compare/$', views.comparison_chart, name='comparison_chart'),
    url(r'^equity/$', views.homepage, name='homepage'),
    url(r'^test/$', views.homepagedev, name='homepagedev'),
    url(r'^javascript', views.myjavascript, name='myjavascript'),
    url(r'^accounts/login', views.login, name='login'),
    url(r'^accounts/setequity', views.setequity, name='setequity'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
