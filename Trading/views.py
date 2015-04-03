from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from models import Account
from django.views.generic import View

def set_equity(request, acct_num, acct_server):
    #my_acct = Account.objects.get(acct_num=acct_num, acct_server=acct_server)
    my_acct = get_object_or_404(Account, acct_num=acct_num, acct_server=acct_server)
    my_acct
    return HttpResponse("Msg from #%s from %s!!!" % (acct_num, acct_server))

def equity_test(request):
    return HttpResponse("This test worked!!!")

class MyView(View):
    
    def get(self, request, *args, **kwargs):
        return HttpResponse('This is GET request')

    def post(self, request, *args, **kwargs):
        return HttpResponse('This is POST request')
