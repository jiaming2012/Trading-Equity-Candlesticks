from django.db import models
from django.forms import ModelForm
import datetime

#class Market(): 
#    Start = models.TimeField(default='17:00:00')
#    EOD = models.TimeField(default='17:00:00')    

class Account(models.Model):
    acct_num = models.IntegerField()
    acct_name = models.CharField(max_length=100)
    acct_server = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100, default='')
    Start = models.TimeField(default='17:00:00')
    EOD = models.TimeField(default='21:00:00')    
    
    def equity_at_day_start(self, days_ago=0):
	candle_list = self.equity_set.filter(timestamp__gte = day_start(days_ago))[:1]
	
	#handles weekend session gaps
	if len(candle_list) == 0:
	    candle_list = self.equity_set.filter(timestamp__gte = last_thursday_start())[:1]	
	
	
	if len(candle_list) > 0:	
	    return candle_list[0].equity_open
	else:
	    return None   

    def equity_at_week_start(self, weeks_ago=0):
	candle_list = self.equity_set.filter(timestamp__gte = week_start(weeks_ago))[:1]
	
	if len(candle_list) > 0:
	    return candle_list[0].equity_open
 	else:
	    return None

    def equity_at_month_start(self):
	candle_list = self.equity_set.filter(timestamp__gte = month_start())[:1]
	
	if len(candle_list) > 0:
	    return candle_list[0].equity_open
	else:
	    return None
    
    def equity_at_start(self):
	candle = self.equity_set.earliest('timestamp')
	return candle.equity_open

    def equity_now(self):
	candle = self.equity_set.latest('timestamp')
	return candle.equity_close
    
    def equity_now_currency(self):
	return format(self.equity_now(), '')
	
    def start_date(self):
	candle = self.equity_set.earliest('timestamp')
	return candle.timestamp

    def __unicode__(self):
        return str(self.acct_name)

class Equity(models.Model):
    acct_id = models.ForeignKey(Account)
    timestamp = models.DateTimeField('dbtime')
    open_lots = models.FloatField()
    equity_open = models.IntegerField()
    equity_close = models.IntegerField()
    equity_low = models.IntegerField()
    equity_high = models.IntegerField()

class EquityForm(ModelForm):
    class Meta:
        model = Equity
        fields = ['equity_open']

def day_start(days_ago=0): 	#Time: EOD
    dt = datetime.datetime.utcnow()

    if dt.hour < 21:
    	dt -= datetime.timedelta(days=days_ago+1)
    else:
	dt -= datetime.timedelta(days=days_ago)

    start_date = dt.replace(hour=21, minute=0, second=0, microsecond=0)
   
    return start_date


def last_thursday_start():
    dt = datetime.datetime.utcnow()

    while dt.weekday() != 3:
	dt -= datetime.timedelta(days=1)

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
    start_date = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    return start_date
