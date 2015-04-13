from django.db import models
from django.forms import ModelForm
import datetime
#master branch doesnt this defeat the purpose
#separte file please
#pretty please
class Market(models.Model): 
    Start = models.TimeField(defult='17:00:00')
    EOD = models.TimeField(default='17:00:00')    

class Account(Market):
    acct_num = models.IntegerField()
    acct_name = models.CharField(max_length=100)
    acct_server = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100, default='')
   
    def __unicode__(self):
        return str(self.acct_name)

class Equity(models.Model):
    acct_id = models.ForeignKey(Account)
    timestamp = models.DateTimeField('dbtime')
    open_lots = models.DecimalField(max_digits=6, decimal_places=2)
    equity_open = models.IntegerField()
    equity_close = models.IntegerField()
    equity_low = models.IntegerField()
    equity_high = models.IntegerField()

    def at_day_start(self, days_ago=1):
	equity = self.objects.filter(timestamp__gte = day_start())
	return equity

class EquityForm(ModelForm):
    class Meta:
        model = Equity
        fields = ['equity_open']

def day_start(days_ago=1): 	#Time: EOD
    dt = datetime.datetime.utcnow()
    dt -= datetime.timedelta(days=days_ago)
    start_date = dt.replace(hour=17, minute=0, second=0, microsecond=0)
    return start_date

def week_start(weeks_ago=0): 	#Time: Start
    dt = datetime.datetime.utcnow()
    day = dt.isoweekday()
    start_date = dt - datetime.timedelta(weeks=weeks_ago, days=day)
    start_date = start_date.replace(hour=17, minute=0, second=0, microsecond=0)
    return start_date

def month_start():		#Time: EOD
    dt = datetime.datetime.utcnow()
    start_date = start_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return start_date
