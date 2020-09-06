from test_queries import *
from netapp_test2 import *
from mySummarizer import *
import re
import h5py

def getdetails(filename, count_file):
    f=h5py.File('Summary.hdf5','r')
    details=[]
    match=re.search(r'\d+', filename)
    name="Case #"+match.group()
    file=match.group()
    details.append(name)
    ipcs=retrieve_ipcs(file)
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
    summary= generate_summary( filename, 2)
    if(filename in f.keys() ):
        mid=f[filename]
        summary=mid[...]
    else:
        summary= generate_summary( filename, 2)
    if summary is not None:
        details.append(summary)
    else:
        details.append(retrieve_finalJudgement(file))
    details.append("Indian Penal Codes: ")
    details.append("Summary:")
    details.append(filename)
    details.append(str(count_file)+". ")
    return details
