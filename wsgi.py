import os
import sys
import site

#Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/home/jcole/Desktop/bin/python2.7/site-packages')

#Add the app's directory to the PYTHONPATH
sys.path.append('/home/jcole/Desktop/bin/Trading-Equity-Candlesticks')

#sys.path = ['/home/jcole/Desktop/bin/Trading-Equity-Candlesticks/Trading'] + sys.path

os.environ['DJANGO_SETTINGS_MODULE'] = 'Trading.settings'

#Activate your virtual env
activate_env = os.path.expanduser("/home/jcole/Desktop/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

