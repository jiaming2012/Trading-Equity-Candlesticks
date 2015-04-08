from django.db import models
from django.forms import ModelForm

class Account(models.Model):
    acct_num = models.IntegerField()
    acct_name = models.CharField(max_length=100)
    acct_server = models.CharField(max_length=100)

    def __unicode__(self):
        return str(self.acct_name)

class Equity(models.Model):
    acct_id = models.ForeignKey(Account)
    timestamp = models.DateTimeField('dbtime')
    open_lots = models.DecimalField(max_digits=6, decimal_places=2)
    equity_open = models.DecimalField(max_digits=10, decimal_places=2)
    equity_close = models.DecimalField(max_digits=10, decimal_places=2)
    equity_low = models.DecimalField(max_digits=10, decimal_places=2)
    equity_high = models.DecimalField(max_digits=10, decimal_places=2)

class EquityForm(ModelForm):
    class Meta:
        model = Equity
        fields = ['equity_open']
	   
