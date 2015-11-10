#coding:utf-8  
import sae  
  
from mytestsite1 import  wsgi                         
  
application = sae.create_wsgi_app(wsgi.application)  
