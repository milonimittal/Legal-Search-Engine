import flask
from flask import request, jsonify
from test_queries import *
from netapp_test2 import *
from flask import Flask, send_file, render_template
	
app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/search1', methods=['GET'])
def api_search1():
    return render_template("search1.html")
@app.route('/about1', methods=['GET'])
def api_aboutus():
    return render_template("aboutus.html")
@app.route('/', methods=['GET'])
def home():
    #    return '''<h1>NetApp</h1>
#<p>Retrieval of legal docs.</p>'''
    return render_template('frontpage.html')
    # return '''<h1><center>turingTonks</center></h1>'''

@app.route('/askquery', methods=['GET'])
def api_query():
   text1=""
   text2=""
   text3=""
   text4=""
   text5=""
   text6=""
   text7=""
   text8=""
   text9=""
   text10=""
   text11=""
   text12=""
   if 'query' in request.args:
       ret=test_query(request.args['query'])
       fin=[]
       flag=0
       if 'date' in request.args:
           for i in ret:
               if (retrieve_firstdate(i)==request.args['date']):
                   fin.append(i)
           if(request.args['date']):
               flag=1
       if 'appeal_no' in request.args:
           for i in ret:
               appellate_jurisdiction, appeal_num=retrieve_AppellateJurisdiction(i)
               if (appeal_num==request.args['appeal_no']):
                   fin.append(i)
           if(request.args['appeal_no']):
               flag=1
       if 'appellate' in request.args:
           ret1=request.args['appellate']
           ret1=ret1.lower()
           for i in ret:
               appellate_jurisdiction, appeal_num=retrieve_AppellateJurisdiction(i)
               if(appellate_jurisdiction):
                   if (appellate_jurisdiction.lower()==ret1):
                       fin.append(i)
           if(request.args['appellate']):
               flag=1
       if flag!=1:
           fin=ret
       if len(fin)==0:
           text1= "No relevant document found."
   else:
       text2= "Error: No query provided. Please specify query."
   ct=0
   cleanlist=[]
   [cleanlist.append(x) for x in fin if x not in cleanlist]   
   fin=cleanlist 

   if(ct<len(fin)):
       text3=fin[0]
   ct=ct+1
   if(ct<len(fin)):
       text4=fin[1]
   ct=ct+1
   if(ct<len(fin)):
       text5=fin[2]
   ct=ct+1
   if(ct<len(fin)):
       text6=fin[3]
   ct=ct+1
   if(ct<len(fin)):
       text7=fin[4]
   ct=ct+1
   if(ct<len(fin)):
       text8=fin[5]
   ct=ct+1
   if(ct<len(fin)):
       text9=fin[6]
   ct=ct+1
   if(ct<len(fin)):
       text10=fin[7]
   ct=ct+1
   if(ct<len(fin)):
       text11=fin[8]
   ct=ct+1
   if(ct<len(fin)):
       text12=fin[9]
   ct=ct+1

   return render_template("new_index.html",text1=text1,text2=text2,text3=text3,text4=text4,text5=text5,text6=text6,text7=text7,text8=text8,text9=text9,text10=text10,text11=text11,text12=text12)

@app.route('/docwise')
def api_docwise():
    try:
        print("HERE1")
        if 'document' in request.args:
                ret=retrieve_finalJudgement(request.args.get('document', 0, type=str))
        else:
            return jsonify(result="Error: No document number provided. Please specify.")
        return jsonify(result=ret)
    except Exception as e:
        return str(e)  
@app.route('/docwise2')
def api_docwise2():
    try:
        print("HERE1")
        if 'document' in request.args:
                ret=retrieve_penalCodes(request.args.get('document', 0, type=str))
        else:
            return jsonify(result="Error: No document number provided. Please specify.")
        return jsonify(result=ret)
    except Exception as e:
        return str(e)  
@app.route('/docwise3')
def api_docwise3():
    try:
        print("HEREDate")
        if 'document' in request.args:
            ret=retrieve_firstdate(request.args.get('document', 0, type=str)+'.txt')
        else:
            return jsonify(result="Error: No document number provided. Please specify.")
        return jsonify(result=ret)
    except Exception as e:
        return str(e)  
@app.route('/docwise4')
def api_docwise4():
    try:
        print("HERE1")
        if 'document' in request.args:
                ret=retrieve_AppellateJurisdiction(request.args.get('document', 0, type=str)+'.txt')
        else:
            return jsonify(result="Error: No document number provided. Please specify.")
        return jsonify(result=ret)
    except Exception as e:
        return str(e)  

@app.route('/alldocs', methods=['GET'])
def api_all():
    ret=all_docs();
    return jsonify(ret)

@app.route('/download')
def download_file():
	if 'doc' in request.args:
		path = "Prior_Cases/"+request.args['doc']+'.txt'
	else:
		return "Enter document name."
	#path = "sample.txt"
	return send_file(path, as_attachment=True)


#@app.route('/response', methods=['POST'])
#def response():
#    fname = request.form.get("fname")
#    note = request.form.get("note")
#    return render_template("index.html", name=fname, note=note)

@app.route('/background_process')
def background_process():
    try:
        if 'query' in request.args:
            ret=test_query(request.args['query'])
            fin=[]
            flag=0
            if 'date' in request.args:
                for i in ret:
                    if (retrieve_firstdate(i)==request.args['date']):
                        fin.append(i)
                        print(i)
                if(request.args['date']):
                    flag=1
            if 'appeal_no' in request.args:
                for i in ret:
                    appellate_jurisdiction, appeal_num=retrieve_AppellateJurisdiction(i)
                    if (appeal_num==request.args['appeal_no']):
                        fin.append(i)
                if(request.args['appeal_no']):
                    flag=1
            if 'appellate' in request.args:
                ret1=request.args['appellate']
                ret1=ret1.lower()
                for i in ret:
                    appellate_jurisdiction, appeal_num=retrieve_AppellateJurisdiction(i)
                    if(appellate_jurisdiction):
                        if (appellate_jurisdiction.lower()==ret1):
                            fin.append(i)
                if(request.args['appellate']):
                    flag=1
            if flag!=1:
                fin=ret
#            if len(fin)==0:
#                text1= "No relevant document found."
        else:
            fin.append( "Error: No query provided. Please specify query.")
        ct=0
        cleanlist=[]
        [cleanlist.append(x) for x in fin if x not in cleanlist]   
        fin=cleanlist 
#        print(fin)
        for i in range (len(fin),10):
            fin.append(" ")
#        print(fin)
        return jsonify(result = fin)
    except Exception as e:
        return str(e)

app.run()







