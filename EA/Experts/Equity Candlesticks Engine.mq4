//+------------------------------------------------------------------+
//|                                   Equity Candlesticks Engine.mq4 |
//|                                                         Carm Inc |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Carm Inc"
#property link      "https://www.mql5.com"
#property version   "1.00"
#property strict

#ifndef AUTOSAVEARRAYSTRING
#define AUTOSAVEARRAYSTRING
   #include <Arrays/AutoSaveArrayString.mqh>
#endif 

#define OK_200         200

class EquityCandle
{
 private:
  string m_timestamp;
  
 public:
  double high;
  double low;
  double open;
  double close;
  string GetTimestamp() { return m_timestamp; }
  void reset();
  
  EquityCandle() { reset(); }
};

input string IP_ADDRESS = "50.116.48.28";
string FILENAME_BACKLOG = "Equity_Candlesticks_Backlog.txt";
string PATH_LOGIN = "/accounts/login";
string PATH_SET_EQUITY = "/accounts/setequity";
string FILE_DELIMITER = "\n";
AutoSaveArrayString* backlog;
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- create timer
   EventSetTimer(1);
   
  //--- pointer initialization
   backlog = new AutoSaveArrayString(FILENAME_BACKLOG);
   
  //--- login to server or create a new account
   string headers;
   char post[], result[];
   string data = "acctNumber=" + (string)AccountNumber() + ";acctServer=" + AccountServer() + ";acctName=" + AccountName() + ";";
   
   ResetLastError();
   
   StringToCharArray(data, post, 0, WHOLE_ARRAY, CP_UTF8);
   
   int res = WebRequest("POST", "http://" + IP_ADDRESS + PATH_LOGIN, "", NULL, 10000, post, ArraySize(post), result, headers);

   Alert("Status code: " , res);
   
   Print("Header: ", headers);
  
   if(res!=OK_200)
    Alert("Error: ", GetLastError());
  
   Alert("Server response: ", CharArrayToString(result));
//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//--- destroy timer
   EventKillTimer();
      
   delete backlog;
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
//---
   
  }
//+------------------------------------------------------------------+
//| Timer function                                                   |
//+------------------------------------------------------------------+
void OnTimer()
  {
//---
   static EquityCandle candle;
   double equity = AccountEquity();
   
   if(equity < candle.low)    
    candle.low = equity;
      
   if(equity > candle.high)   
    candle.high = equity;
   
   BackLogCleanUp();
   
   if(NewMinuteCandle())
   {
    POSTEquity(candle.open, candle.low, candle.high, equity, OpenLots());
    candle.reset();
   }
  }
//+------------------------------------------------------------------+
void EquityCandle::reset()
{
  double equity = AccountEquity();
  
 //--- set new timestamp
  m_timestamp = SQLTimeCurrent();
  
 //--- reset candle
  open = equity;
  high = equity;
  low = equity;
  close = equity;
}
//+------------------------------------------------------------------+
void POSTEquity(double open, double low, double high, double close, double volume)
{
 //--- Attempt 1: post equity to server
  string headers;
  char post[], result[];
  string data = "acctNumber=" + (string)AccountNumber() + ";acctServer=" + AccountServer();
  data += ";timestamp=" + SQLTimeCurrent();
  data += ";openLots=" + DoubleToStr(volume, 2);
  data += ";equityOpen=" + DoubleToStr(open,2) + ";equityLow=" + DoubleToStr(low,2) + ";equityHigh=" + DoubleToStr(high,2) + ";equityClose=" + DoubleToStr(close,2) + ";";
  
  StringToCharArray(data, post, 0, WHOLE_ARRAY, CP_UTF8);
   
  int response = WebRequest("POST", "http://" + IP_ADDRESS + PATH_SET_EQUITY, "", NULL, 3000, post, ArraySize(post), result, headers);
  
  if(response==OK_200)
   return; 
   
  Print("Error: ", GetLastError());
  Print("Status code: ", response);
  Print("Header: ", headers);
  Print("Server response: ", CharArrayToString(result));
  
 //--- Attempt 2: save to auto save array
  if(backlog.Add(data))
   return;
  
 //--- Error message
  Alert("Critical error: unable to post equity to server nor save to file");
  Print(data);
  return;
}
//+------------------------------------------------------------------+
void BackLogCleanUp()
{
 string headers;
 char post[], result[];
 
 for(int i=0; i<backlog.Total(); i++)
 {
  string data = backlog[i];
  
  StringToCharArray(data, post, 0, WHOLE_ARRAY, CP_UTF8); 
  
  int response = WebRequest("POST", "http://" + IP_ADDRESS + PATH_SET_EQUITY, "", NULL, 3000, post, ArraySize(post), result, headers);
  
  if(response==OK_200)
  {
   backlog.Delete(i);
   i--;
   ArrayFree(post);
   ArrayFree(result);
   continue;
  }
  
  break;
 }
}
//+------------------------------------------------------------------+
double OpenLots()
{
 int total = OrdersTotal();
 double lots = 0;
 
 for(int i=0; i<total; i++)
 {
  if(OrderSelect(i,SELECT_BY_POS))
   lots += OrderLots();
 }
 
 return lots;
}
//+------------------------------------------------------------------+
bool NewMinuteCandle()
{
 static MqlDateTime prev_tstamp;
 MqlDateTime tstamp;
 
 TimeCurrent(tstamp);

 if(tstamp.sec < prev_tstamp.sec)
 {
  prev_tstamp = tstamp;
  return true;
 }
 
 prev_tstamp = tstamp;
 
 return false;
}
//+------------------------------------------------------------------+
string SQLTimeCurrent()
{
 string time = (string)TimeCurrent();
 
 StringReplace(time,".","-");
 
 return time;
}