from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from models import Account, Equity
from django.views.generic import View
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework.response import Response
from django.template import RequestContext, loader
import json

def validate(myDict, keyList):
    for key in keyList:
	if key not in myDict:
	    return "POST keys = %s does not match expected keys = %s" % (myDict.keys(), keyList)
    return True

def myjavascript(request):
    template = loader.get_template('jscript.js')
    context = RequestContext(request, {'equity':'5000'})

    return HttpResponse(template.render(context))

def homepage(request):
    accounts = Account.objects.all()
    template = loader.get_template('homepage.html')
    context = RequestContext(request, {'accounts': accounts})
    return HttpResponse(template.render(context))

def candle_chart(request, account_number):
    account = get_object_or_404(Account, acct_num = account_number)
    equity = account.equity_set.order_by('timestamp')
    
    #iterate equity list to JSON
    my_list_candle = []
    my_list_volume = []
    for e in equity:
	tstamp = int(e.timestamp.strftime('%s000'))
	my_list_candle.append([tstamp, e.equity_open, e.equity_high, e.equity_low, e.equity_close])
	my_list_volume.append([tstamp, e.open_lots])
    
    data1 = json.dumps(my_list_candle)
    data2 = json.dumps(my_list_volume)
    template = loader.get_template('tester.html')
    context = RequestContext(request, {'equity': equity, 'candle': data1, 'lots': data2})    

    return HttpResponse(template.render(context))

@csrf_exempt
@api_view(['GET', 'POST'])
@require_POST
def setequity(request):
    if request.method == 'POST':
	equityOpen = -1
	equityLow = -1
	equityHigh = -1
	equityClose = -1
	isValid = validate(request.data, [u'timestamp', u'openLots', u'acctNumber', u'acctServer', u'equityOpen', u'equityLow', u'equityHigh', u'equityClose'])
	
	if(isValid == True):
	    try:
		acctNumber = int(request.data["acctNumber"])
	    except ValueError:
		return HttpResponseBadRequest("acctNumber must be an integer value")	
	    
	    try:
		equityOpen = float(request.data["equityOpen"])
		equityLow = float(request.data["equityLow"])
		equityHigh = float(request.data["equityHigh"])
		equityClose = float(request.data["equityClose"])
		openLots = float(request.data["openLots"])
	    except ValueError:
		return HttpResponseBadRequest("equityOpen, equityLow, equityHigh and equityClose must be of numeric type")

	    acctServer = request.data['acctServer']	    

	    a = get_object_or_404(Account, acct_num=acctNumber, acct_server=acctServer)  
	    
	    tstamp = request.data['timestamp'] 
            a.equity_set.create(timestamp=tstamp, open_lots=openLots, equity_open=equityOpen, equity_low=equityLow, equity_high=equityHigh, equity_close=equityClose)    
 
	    return HttpResponse("POST Successful")
	else:
            return HttpResponseBadRequest(isValid)	
	  
    return HttpResponseBadRequest("HTTP POST expected")

@api_view(['GET', 'POST'])
def login(request):
    if request.method == 'POST':
    	isValid =  validate(request.data, [u'acctNumber', u'acctName', u'acctServer'])
	
	if(isValid == True):
	    try:
		acctNumber = int(request.data["acctNumber"])
		acctName = request.data["acctName"]
		acctServer = request.data["acctServer"]
		
		try:
		    Account.objects.get(acct_num=acctNumber, acct_server=acctServer)
		    return Response("Login successful")
		except Account.DoesNotExist:
		    a = Account(acct_num=acctNumber, acct_name=acctName, acct_server=acctServer)
		    a.save()
		    return Response("New account created")
		
	    except ValueError:
		return Response("acctNumber must be an integer value")
	else:
	    return Response(isValid)

    return Response("HTTP POST expected")

