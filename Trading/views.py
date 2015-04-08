from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from models import Account, EquityForm
from django.views.generic import View
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework.response import Response

def validate(myDict, keyList):
    for key in keyList:
	if key not in myDict:
	    return "POST keys = %s does not match expected keys = %s" % (myDict.keys(), keyList)
    return True

def home(request):
#    ret = ''
#    for e in a.equity_set.all():
#	ret += "%s=%s<br>" % (e.timestamp, e.equity_close)
#
    return HttpResponse("Welcome")

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

