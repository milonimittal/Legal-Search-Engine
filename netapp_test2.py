import regex as re
import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

"""Retrieve date of case"""

def date_check(line):
  words=line.split()
  length=len(line.split())
  if(length>=3):
      word=words[length-3]
      words[length-3]=word[1:]
      word=words[length-1]
      words[length-1]=word[:-1]
      return (words[length-3]+' '+words[length-2]+' '+words[length-1])
  else:
      return " "


def retrieve_firstdate(filename):
  if(filename=="No more Files"):
    return "-1"
  start='Prior_Cases/'
  f=open(start+filename,'r')
  lines = f.read()
  line=lines.splitlines()
  return date_check(line[0])



"""Retrieve Citatation line"""

def citation_check(lines):
  lines2=lines.splitlines()
  String='CITATION:'
  for x in lines2:
    ResSearch = re.search(String, x)
    if ResSearch:
      return (re.sub(r'^\W*\w+\W*', '', x))
  return None

def retrieve_citation(filename):
  start='Prior_Cases/'
  f=open(start+filename+'.txt','r')
  lines = f.read()
  return citation_check(lines)



"""Retrieve all the information under Held"""

def held_check(lines):
  lines2=lines.splitlines()
  flag=0
  String='HELD :'
  for x in lines2:
    ResSearch = re.search(String, x)
    if (ResSearch and flag==0):
      held = (re.sub(r'^\W*\w+\W*', '', x))
      flag = 1
      String = ' : '
    elif (ResSearch and flag==1):
      return held
    elif (flag==1):
      held = held + '\n' + x
  return None

def retrieve_held(filename):
  start='Prior_Cases/'
  f=open(start+filename+'.txt','r')
  lines = f.read()
  return held_check(lines)




"""If there is an appellate jurisdiction, return whether it is a civil or criminal appellate jurisdiction"""

def aj_check(lines):
  lines2=lines.splitlines()
  flag=0
  str1=""
  for line in lines2:
    if(flag==1):
      match=re.search(r'\d+', line)
      return str1 , match.group()
    String='CIVIL APPELLATE JURISDICTION'
    ResSearch = re.search(String, line)
    if ResSearch:
      str1=line.split()
      str1=str1[4:]
      str1=' '.join(str1)
      if(bool(re.search(r'\d', str1))):
        match=re.search(r'\d+', str1)
        return "CIVIL", match.group()
      else:
        str1="CIVIL"
        flag=1
    else:
      String='CRIMINAL APPELLATE JURISDICTION'
      ResSearch = re.search(String, line)
      if ResSearch:
        str1=line.split()
        str1=str1[4:]
        str1=' '.join(str1)
        if(bool(re.search(r'\d', str1))):
          match=re.search(r'\d+', str1)
          return "CRIMINAL", match.group()
        else:
          str1="CRIMINAL"
          flag=1
  return None,None

def retrieve_AppellateJurisdiction(filename):
  if(filename=="No more Files"):
    return "-1","-1"
  start='Prior_Cases/'
  f=open(start+filename,'r')
  lines = f.read()
  appellate_jurisdiction, appeal_no = aj_check(lines)
  return appellate_jurisdiction, appeal_no




""" Retrieve everything under the heading 'CITATOR' """

def citatorInfo_check(lines):
  lines2=lines.splitlines()
  flag=0
  String='CITATOR INFO :'
  for x in lines2:
    ResSearch = re.search(String, x)
    if (ResSearch and flag==0):
      str1=x.split()
      str1=str1[3:]
      cinfo=' '.join(str1)
      flag = 1
      String = ' : '
    elif (ResSearch and flag==1):
      return cinfo
    elif (flag==1):
      cinfo = cinfo + '\n' + x
  return None

def retrieve_citatorInfo(filename):
  start='Prior_Cases/'
  f=open(start+filename+'.txt','r')
  lines = f.read()
  return citatorInfo_check(lines)




"""If there was an appeal, check whether it was allowed or dismissed"""

def appeal_allowedOrDismissed(lines):
  lines2=lines.splitlines()
  for i in range(0,len(lines2)):
    lines2[i]= lines2[i].lower()
  for line in range((len(lines2)-1),-1,-1):
    String='appeal'
    ResSearch = re.search(String, lines2[line])
    if (ResSearch):
      if(re.search('allowed', lines2[line])):
        return 'allowed'
      elif(re.search('dismissed', lines2[line])):
        return 'dismissed'

def retrieve_appealAllowedOrDismissed(filename):
  start='Prior_Cases/'
  f=open(start+filename+'.txt','r')
  lines = f.read()
  return appeal_allowedOrDismissed(lines)




"""Retrieve the name of the judge"""

def judge_check(lines):
  match = re.search(r'Judgment of the Court was delivered by (\S+)', lines)
  if match:
      judge = match.group(1)
      judge = re.sub(r'[^\w\s]','',judge)
      return format(judge)

def retrieve_judge(filename):
  start='Prior_Cases/'
  f=open(start+filename+'.txt','r')
  lines = f.read()
  return judge_check(lines)




"""Retrieve the names of the appellants"""

def appellant_check(lines):
  lines2=lines.splitlines()
  ResSearch=0
  appellant=[]
  for line in lines2:
    if('for appellant.' in line):
      ResSearch = 1
    if('for Appellant.' in line):
      ResSearch = 1
    if('for the appellant.' in line):
      ResSearch = 1
    if('for the Appellant.' in line):
      ResSearch = 1
    if('for appellant No.' in line):
      ResSearch = 1
    if('for Appellant No.' in line):
      ResSearch = 1
    if('for the appellant No.' in line):
      ResSearch = 1
    if('for the Appellant No.' in line):
      ResSearch = 1
    if(ResSearch):
      ResSearch=0
      words=re.split(',', line)
      words2=re.split(' and ', words[-1])
      if words:
        words=words[:((len(words))-1)]
      else:
        continue
      for x in words2:
        words.append(x)
      words2=re.split(' for ', words[-1])
      
      if words:
        words=words[:((len(words))-1)]
      else:
        continue
      
      if words2[0]:
        words.append(words2[0])
      else:
        continue
      tagged=nltk.pos_tag(words)
      for i in range ( 0, len(tagged)):
        if(tagged[i][1]=='NNP'):
          appellant.append(tagged[i][0])
  if appellant:            
    return appellant
  else:
    return None

def retrieve_appellant(filename):
  start='Prior_Cases/'
  f=open(start+filename+'.txt','r')
  lines = f.read()
  return appellant_check(lines)




"""Retrieve names of respondents"""

def respondent_check(lines):
  lines2=lines.splitlines()
  respondent=[]
  ResSearch=0
  for line in lines2:
    if('for respondent.' in line):
      ResSearch = 1
    if('for Respondent.' in line):
      ResSearch = 1
    if('for the respondent.' in line):
      ResSearch = 1
    if('for the Respondent.' in line):
      ResSearch = 1
    if('for respondent No.' in line):
      ResSearch = 1
    if('for Respondent No.' in line):
      ResSearch = 1
    if('for the respondent No.' in line):
      ResSearch = 1
    if('for the Respondent No.' in line):
      ResSearch = 1
    if(ResSearch):
      ResSearch=0
      words=re.split(',', line)
      words2=re.split(' and ', words[-1])
      if words:
        words=words[:((len(words))-1)]
      else:
        continue
      for x in words2:
        words.append(x)
      words2=re.split(' for ', words[-1])
      
      if words:
        words=words[:((len(words))-1)]
      else:
        continue
      
      if words2[0]:
        words.append(words2[0])
      else:
        continue
      tagged=nltk.pos_tag(words)
      for i in range ( 0, len(words)):
        if(tagged[i][1]=='NNP'):
          respondent.append(tagged[i][0])
  if respondent:            
    return respondent
  else:
    return None

def retrieve_respondents(filename):
  start='Prior_Cases/'
  f=open(start+filename+'.txt','r')
  lines = f.read()
  return respondent_check(lines)




"""Retrieve order as to costs line """

def order_to_costs_check(lines):
  lines2=lines.splitlines()
  for line in range((len(lines2)-1),-1,-1):
    String='order as to cost'
    ResSearch = re.search(String, lines2[line])
    if (ResSearch):
      ResSearch2 = nltk.tokenize.sent_tokenize(lines2[line])
      for i in range(0,len(ResSearch2)):
        ResSearch = re.search(String, ResSearch2[i])
        if(ResSearch):
          return ResSearch2[i]
  return None

def retrieve_orderAsToCosts(filename):
  start='Prior_Cases/'
  f=open(start+filename+'.txt','r')
  lines = f.read()
  order_to_costs = order_to_costs_check(lines)
  return order_to_costs




"""Retrieve final judgement"""

def final_judgement(lines):
  lines2=lines.split(". ")
  return lines2[-5] + ". " + lines2[-4]+ ". " + lines2[-3]+ ". " + lines2[-2]

def retrieve_finalJudgement(filename):
  start='Prior_Cases/'
  f=open(start+filename+'.txt','r')
  lines = f.read()
  judgement=final_judgement(lines)
  return judgement




"""Retrieve IPCs"""

def checker_code(codeno,codestr):
    if codestr=='Indian Penal Code':
        if (codeno>511):
            return None
        else:
            return 1
    else:
        return 1


def ipc_cpc_check(lines):
  lines2=lines.splitlines()
  pc=[]
  ResSearch=0
  for line in lines2:
    code=[]
    nltk_tokens = nltk.word_tokenize(line)  	
    bigramsl=list(nltk.bigrams(nltk_tokens))
    for term in bigramsl:
        if(re.search('ipc' , term[0].lower())):
            ResSearch = 1
            code.append('Indian Penal Code')
        if(re.search('indian' ,  term[0].lower())):
            if(re.search('penal' ,  term[1].lower())):
                ResSearch = 1
                code.append('Indian Penal Code')
        if(re.search('cpc' ,  term[0].lower())):
                ResSearch = 2
                code.append('Criminal Procedure Code')
        if(re.search('criminal' ,  term[0].lower())):
            if(re.search('procedure' ,  term[1].lower())):
                ResSearch = 2
                code.append('Criminal Procedure Code')
        if(re.search('civil' ,  term[0].lower())):
            if(re.search('procedure' ,  term[1].lower())):
                ResSearch = 3
                code.append('Civil Procedure Code')
        
    if(ResSearch):
        codecount=0
        for term in bigramsl:
            if ((term[0].lower()=='s.') or (term[0].lower()=='section')):
                if (re.search(r'\d+', term[1])):
                    match=re.search(r'\d+', term[1])
                    if(checker_code(int(match.group()),code[codecount]) is not None):
                        pc.append(('s. '+match.group(),code[codecount]))
                        if (codecount+1 != len(code) ):
                            codecount+=1
             
    ResSearch=0
  pc = list(dict.fromkeys(pc))
  return pc


def retrieve_penalCodes(filename):
  start='Prior_Cases/'
  f=open(start+filename,'r')
  lines = f.read()
  codes = ipc_cpc_check(lines)
  
  return codes


def getchapter(ipcno):
    if ipcno>=1 and ipcno<=5:
        return("Chapter I")
    elif ipcno>=6 and ipcno<=52:
        return("Chapter II")
    elif ipcno>=53 and ipcno<=75:
        return("Chapter III")
    elif ipcno>=76 and ipcno<=106:
        return("Chapter IV")
    elif ipcno>=107 and ipcno<=120:
        return("Chapter V")
    elif ipcno>=120 and ipcno<=120:
        return("Chapter VA")
    elif ipcno>=121 and ipcno<=130:
        return("Chapter VI")
    elif ipcno>=131 and ipcno<=140:
        return("Chapter VII")
    elif ipcno>=141 and ipcno<=160:
        return("Chapter VIII")
    elif ipcno>=161 and ipcno<=170:
        return("Chapter IX")
    elif ipcno>=171 and ipcno<=171:
        return("Chapter IXA")
    elif ipcno>=172 and ipcno<=190:
        return("Chapter X")
    elif ipcno>=191 and ipcno<=229:
        return("Chapter XI")
    elif ipcno>=230 and ipcno<=263:
        return("Chapter XII")
    elif ipcno>=264 and ipcno<=267:
        return("Chapter XIII")
    elif ipcno>=268 and ipcno<=294:
        return("Chapter XIV")
    elif ipcno>=295 and ipcno<=298:
        return("Chapter XV")
    elif ipcno>=299 and ipcno<=377:
        return("Chapter XVI")
    elif ipcno>=378 and ipcno<=462:
        return("Chapter XVII")
    elif ipcno>=463 and ipcno<=489:
        return("Chapter XVIII")
    elif ipcno>=490 and ipcno<=492:
        return("Chapter XIX")
    elif ipcno>=493 and ipcno<=498:
        return("Chapter XX")
    elif ipcno>=499 and ipcno<=502:
        return("Chapter XXI")
    elif ipcno>=503 and ipcno<=510:
        return("Chapter XXII")
    elif ipcno==511:
        return("Chapter XXIII")
    else:
        return(None)


def retrieve_ipcs(filename):
    newfile=[]
    pc=retrieve_penalCodes(filename)
    for ipc, codename in pc:
      if codename == 'Indian Penal Code':
          newfile.append(ipc)
    if len(newfile)==0:
        return None
    return newfile
    

