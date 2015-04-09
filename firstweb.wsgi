import os
import sys
sys.path = ['/home/jcole/Desktop/bin/Trading-Equity-Candlesticks/Trading'] + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'Trading.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

