
import datetime 
import calendar
import pandas as pd 
import os 
from threading import Thread 
import requests
from threading import Semaphore

from queue import Queue 
import time 
import hashlib
from contextlib import closing
def add_months(dt,months):
    dt=datetime.datetime.strptime(dt,'%Y-%m-%d')
    month = dt.month - 1 + months
    if month>=0:
         year = dt.year + int(month / 12)
    else:
          year = dt.year + int(month / 12)-1
    month = int(month % 12 + 1)
    day = min(dt.day,calendar.monthrange(year,month)[1])
    x=dt.replace(year=year, month=month, day=day)
    x=datetime.datetime.strftime(x,'%Y-%m-%d')
    return x 




class office_io:


    def __init__(self,path=None):
        if path is None:
          self.path="d:\\UserData\\lanmengfei\\Desktop\\myfile"
        else:
          self.path=path

    @staticmethod
    def log_time(func):
        def wrapper(*args,**kw):
          begin=datetime.datetime.now()
          a=func(*args,**kw)
          end=datetime.datetime.now()
          div=(end-begin).seconds
          print(func.__name__, div)
          return a
        return wrapper



    def mypath(self,wb_name,tail='xlsx'):
         
         path=self.path
         i=0
         name=path+'\\%s.'%wb_name+tail
         while os.path.exists(name):
              i+=1
              name=(path+'\\%s%d.'+tail)%(wb_name,i)
         print(name)
         return name

    def outdf(self,df,ws_name='Sheet1',wb_name='a'):
         wb_absname=self.mypath(wb_name)
         self._outdf(df,ws_name,wb_absname)
    def _outdf(self,df,ws_name,wb_absname):
         w=pd.ExcelWriter(wb_absname)
         df.to_excel(w,sheet_name=ws_name,index=False)
         wb=w.book
         ws=w.sheets[ws_name]
         fm=wb.add_format({'font_size':'10'})
         ws.set_column('A:AA',8.43,fm)
         w.save()

    def outdfs(self,dfs,ws_name='Sheet1',wb_name='a'):

         wb_absname=self.mypath(wb_name)
         self._outfs(dfs,ws_name,wb_absname)
    def _outdfs(self,dfs,ws_name,wb_absname):
         w=pd.ExcelWriter(wb_absname)
         n=0
         wb=w.book
         fm=wb.add_format({'font_size':'10'})

         for df in dfs:
                m=len(df)
                df.to_excel(w,sheet_name=ws_name,startrow=n,index=False)
                ws=w.sheets[ws_name]
                ws.set_column('A:AA',8.43,fm)
                n+=m+5
         w.save()

    def outdfss(self,dfss,ws_names,wb_name='a'):
         wb_absname=self.mypath(wb_name)
         self._outdfss(dfss,ws_names,wb_absname)
    def _outdfss(self,dfss,ws_names,wb_absname):
         w=pd.ExcelWriter(wb_absname)
         for i in range(len(dfss)):
              st=ws_names[i]
              n=0
              for df in dfss[i]:
                   m=len(df)
                   df.to_excel(w,sheet_name=st,startrow=n,index=False)
                   n+=m+5
                   wb=w.book
                   ws=w.sheets[st]
                   fm=wb.add_format({'font_size':'10'})
                   ws.set_column('A:AA',8.43,fm)
                   
              print('工作表-%s完成'%st)
         wb_name=os.path.basename(wb_absname)
         print('工作簿-%s完成'%wb_name)
         w.save()
    def outdfsss(self,dfsss,wdict1=None,wdict2=None,wb_path='xxx',tail='xlsx'):
         wb_abspath=os.path.join(self.path,wb_path)
         i=0
         dirname=wb_abspath
         while os.path.exists(dirname):
              i+=1
              dirname="%s(%d)"%(wb_abspath,i)
         os.mkdir(dirname)

         if wdict1 is None:
            #*wdict=['a1','a2'],[['Sheet1','Sheet2'],['Sheet1','Sheet2','Sheet3']]
            mm=len(dfsss)
            wdict1=['a%d'%(i+1) for i in range(i)]
         
         for ii in range(len(dfsss)):
            dfss=dfsss[ii]
            nn=len(dfss)
            if wdict2 is None:
              w_sheetsname=['Shheet%d'%(i+1) for i in range(nn)]
            else:
              w_sheetsname=wdict2[ii]
            wb_absname=os.path.join(dirname,'%s.%s'%(wdict1[ii],tail))
            
            self._outdfss(dfss,w_sheetsname,wb_absname)
            
def strQ2B(ustring):
    """把字符串全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if (inside_code >= 0x0021 and inside_code <= 0x7e)  :   #全角直接返回
            rstring += uchar
        else:
            if inside_code==0x3000:                         #全角角空格单独处理 
                inside_code = 0x0020
            else:                                           #其他的全角半角的公式为:半角 = 全角- 0xfee0
                inside_code -= 0xfee0
            
            rstring += chr(inside_code) if inside_code  in range(0x110000)  else uchar     
    return rstring



class mythread:


    def __init__(self,arr,f):
        self.sema=Semaphore(1)
        self.q=Queue()
        for w in arr:
            self.q.put(w)
        self.f=f 
        self.i=0

    def task(self):
        while not  self.q.empty():
            word=self.q.get(block=False)
            self.sema.acquire()
            self.i+=1
            print(self.i,str(word))
            self.sema.release()

            self.f(word)
            if self.q.empty():break
    def run(self,num):
        ths=[]
        for _ in range(num):
            t=Thread(target=self.task)
            ths.append(t)
        for t in ths:
            t.start()
        for t in ths:
            t.join()




def md5(s):
    m = hashlib.md5()

    b = s.encode(encoding='utf-8')
    m.update(b)
    s = m.hexdigest()
    return s


def down_file(url,file_src):

    headers={

        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    }
    print('开始下载文件 %s'%file_src)
    with closing (requests.get(url,stream=True,headers=headers,verify=False)) as res:
        count=0
        with open(file_src, 'wb') as fd:
            for chunk in res.iter_content(chunk_size=1024):
                if chunk:
                    fd.write(chunk)

                    count +=1
                    if count % 10240 == 0:
                        print('下载 %s MB'%(count//1024))

    print('下载完成,共下载 %.2f MB'%(count/1024))
    return True