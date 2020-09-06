# Just-Justice
Referencing and researching past judgments is an important step in filing, fighting, or deciding a case. Just-Justice eliminates the need of sifting physically through the millions of documents available based on established law and legal proceedings and presents the users the top documents for any query they type! We believe that  Just-Justice can help everyone from Judges and Lawyers to citizens of our country. Lawyers would find it easy to research from existing case documents. By automating the process, their efficiency would be increased. Judges can stay ahead of the game by retrieving information about past judgments by date, geographical area, and other tags and other relevant details at a glance. By looking at past cases, judgments and related cases in their area, Citizens can make an informed decision before filing a case.
This is the README to work the fantastic-LegalSearchEngine repository, an official submission for the Netapp Women Innovathon(WIN)
The code has been tested on a dataset of legal cases procured online, and can be found at: https://drive.google.com/drive/folders/16-kGqOEBppr1hOQ2l7TkU2vTrvkpr9Fh?usp=sharing
<br>
List of libraries required and relevant links:
- flask - to install refer this link https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask
- nltk
https://www.nltk.org/install.html
- re
https://pypi.org/project/regex/
- networkx https://networkx.github.io/documentation/stable/install.html
- numpy
https://numpy.org/install/
- sklearn- https://scikit-learn.org/stable/install.html
- math 
- spellchecker- https://pypi.org/project/pyspellchecker/
- collections

$ git clone https://github.com/milonimittal/Legal-Search-Engine
$ cd Legal-Search-Engine
$ python3 api.py

Run http://127.0.0.1:5000/ on your web browser.  
Alternative link for dataset:
https://drive.google.com/drive/folders/16-kGqOEBppr1hOQ2l7TkU2vTrvkpr9Fh?usp=sharing
Document Describing the Project
https://docs.google.com/document/d/1MBZqOisDTiiMuO47uPI4mjBiuAk1AQND3fvP1FB2l8s/edit?usp=sharing
Presentation explaining the project
https://docs.google.com/presentation/d/1rRnhoRlBUsZAuftL2CYCsVZ_EA1pTHzvloFZPLHLPMU/edit?usp=sharing
Video Demo Link


Keep the dataset in the outer directory with python code and operate.

- api.py has 3 views/APIs and a homepage:
Home:           Lets user enter their search query and filter by data/Appeal Number/Appellate. The filtering is done on an or
                basis and will return results for (Query && (Date Or Appeal Number or Appellate))
            
api_query:      Takes text query and/or filter information from user and uses pre-computed posting lists to rank the document set. Filters are 
                implemented by writing individual logic to extract data/appeal number etc. Other features extracted which will be 
                integrated with the system in the future are: Citation, Citator Info, Whether the appeal was dismissed or allowed, Criminal/Civil Appellate Jurisdiction 
                By whom the Judgment of the Court was delivered by, Appellant, Respondent, Appeal number, Mention of constitutional acts, No order as to costs.
                This API returns the list of top 10 documents.

api_all:        API to return list of all docs available

download_file:  API for user to download the requested document


- templates has html files for basic UI. UI is to be updated and improved post midsem to include data visualisations and a short bullet-form view
of cumbersome legal reports

-netapp_test2.py contains pythonic code for legal feature extraction from case documents. Features like Citation, Citator Info, Whether the appeal was dismissed or allowed, Criminal/Civil Appellate Jurisdiction 
            By whom the Judgment of the Court was delivered by, Appellant, Respondent, Appeal number, Mention of constitutional acts, No order as to costs, Date etc are extracted. This code is later used to also filter
            the ranked documents according to features specified by the user.

-scan.py contains pythonic code for the vector space model which makes a posting list out of the dataset corpus. This file usually takes a long time to run but once run, does not need to be updated again.
It produces posting_list2.npy, titles2.npy, and norm2.npy which are results of the dataset directly used by the query code thus increasing speed.

-test_queries.py asks the users for the query and uses files prduced by scan.py- posting_list2.npy, titles2.npy, and norm2.npy to rank the documents according to relevance of query.

