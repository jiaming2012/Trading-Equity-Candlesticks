//+------------------------------------------------------------------+
//|                                          AutoSaveArrayString.mqh |
//|                                                         Carm Inc |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Carm Inc"
#property link      "https://www.mql5.com"
#property strict

#ifndef ARRAYSTRING
#define ARRAYSTRING
   #include <Arrays\ArrayString.mqh>
#endif

#ifndef ARRAYFILEPATH
   #define ARRAYFILEPATH               "DataTypes\ClassArrays\\"
#endif

class AutoSaveArrayString : public CArrayString
{
 private:
  string p_filename;
  
 public:
  bool Add(const string element);
  bool Update(const int index,const string element);
  bool Delete(const int index);
  bool DeleteFile();
  void AutoSaveArrayString(string filename);
  void AutoSaveArrayString(string filename, float max_array_age_in_minutes);
};
//---------------------------------------------
bool AutoSaveArrayString::DeleteFile()
{
  if(FileIsExist(p_filename))
   {
    return(FileDelete(p_filename));
   } 
  else   
   {
    Alert("Error: could not delete file '",p_filename,"' in ",__FUNCTION__," for file does not exist");
    return(false);
   }
}
//---------------------------------------------
bool AutoSaveArrayString::Delete(const int index)
{
  bool ans = CArrayString::Delete(index);
  
  if(!ans) {
   Alert("Error: unable to delete '",m_data[index],"', index = ",index," in ",__FUNCTION__);
   return(false);
  }
  
  int handle = FileOpen(p_filename,FILE_WRITE|FILE_TXT);
  
  if(handle >= 0)
   {
    FileWrite(handle,(int)TimeCurrent());
    FileWrite(handle,m_data_total);
    FileWriteArray(handle,m_data);
    FileClose(handle);
    return(true);
   }
  
  Alert("Error: unable to open ",p_filename," in ",__FUNCTION__," for e = ",GetLastError());
  
  return(false);
}
//---------------------------------------------
bool AutoSaveArrayString::Update(const int index,const string element)
{
  bool ans = CArrayString::Update(index, element);
  
  if(!ans) {
   Alert("Error: unable to update ",element,". Index = ",index," in ",__FUNCTION__);
   return(false);
  }
  
  int handle = FileOpen(p_filename,FILE_WRITE|FILE_TXT);
  
  if(handle >= 0)
   {
    FileWrite(handle,(int)TimeCurrent());
    FileWrite(handle,m_data_total);
    FileWriteArray(handle,m_data);
    FileClose(handle);
    return(true);
   }

  Alert("Error: unable to open ",p_filename," in ",__FUNCTION__," for e = ",GetLastError());
  
  return(false);
}
//---------------------------------------------
bool AutoSaveArrayString::Add(const string element)
{
  bool ans = CArrayString::Add(element);

  if(!ans) {
   Alert("Error: unable to add ",element," in ",__FUNCTION__); 
   return(false);
  }
  
  int handle = FileOpen(p_filename,FILE_WRITE|FILE_TXT);
  
  if(handle >= 0)
   {
    FileWrite(handle,(int)TimeCurrent());
    FileWrite(handle,m_data_total);
    FileWriteArray(handle,m_data);
    FileClose(handle);
    return(true);
   }

  Alert("Error: unable to open ",p_filename," in ",__FUNCTION__," for e = ",GetLastError());
  
  return(false);
}
//---------------------------------------------
void AutoSaveArrayString::AutoSaveArrayString(string filename)
{
  p_filename = ARRAYFILEPATH + filename;
  
  if(FileIsExist(p_filename))
  {
   int handle = FileOpen(p_filename,FILE_READ|FILE_TXT);
     
   FileSeek(handle,0,SEEK_SET);
   
   int last_save_timestamp = (int)FileReadString(handle);
     
   m_data_total = (int)FileReadString(handle);
     
   FileReadArray(handle, m_data);
   
   //--- re-initialize protected data
    m_data_max=ArraySize(m_data);
     
   FileClose(handle);
  }
}
//---------------------------------------------
void AutoSaveArrayString::AutoSaveArrayString(string filename, float max_array_age_in_minutes)
{
  p_filename = ARRAYFILEPATH + filename;
  
  if(FileIsExist(p_filename))
   {
     int handle = FileOpen(p_filename,FILE_READ|FILE_TXT);
     
     if(handle >= 0)
      {
          int last_save_timestamp = (int)FileReadString(handle);

          if(((int)TimeCurrent() - last_save_timestamp) / 60.0 < max_array_age_in_minutes)
           {
              m_data_total = (int)FileReadString(handle);
              
              FileReadArray(handle, m_data);
            
             //--- re-initialize protected data
              m_data_max=ArraySize(m_data);
              
              FileClose(handle);
              
              return;
          } //--- if false fall through
     }
    else
     {
       Alert("Error: could not access '",p_filename," for read, e: ",GetLastError()," in ",__FUNCSIG__);
       return;
     } 
     
    FileClose(handle);
   }
}