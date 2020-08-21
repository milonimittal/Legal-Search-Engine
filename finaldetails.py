from test_queries import *
from netapp_test2 import *
from mySummarizer import *

def getdetails(filename):
    details=[]
    details.append(filename)
    ipcs=retrieve_ipcs(filename)
    if (ipcs is None):
       details.append("No IPCs in this file")
    else:
       ipcs1=' ' 
       count=0
       for val in ipcs:
           if count <len(ipcs)-1:
               ipcs1=ipcs1+ val+", " 
           else:
               ipcs1=ipcs1+ val
           count+=1
       details.append(ipcs1) 
    details.append(generate_summary( filename, 2))
    details.append("Indian Penal Codes: ")
    details.append("Summary:")
    return details