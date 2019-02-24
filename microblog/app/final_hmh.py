import six
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from sematch.semantic.similarity import WordNetSimilarity
import pandas as pd
import numpy as np
import re
from urllib.request import Request
from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import Counter
import operator
import json
import re

num_keywords=10

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


TRIGGERS = ["suicide"]
url="https://www.sfgate.com/bayarea/article/Investigators-Robin-Williams-hanged-himself-5683229.php"

def parse_my_url(url):
    req = Request(url, headers=hdr)

    try:
        page = urlopen(req)
        #html = urlopen(url).read()
        html = page.read()
        soup = BeautifulSoup(html,features="html.parser")

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = ' '.join(chunk for chunk in chunks if chunk)

        header = ""

        found_triggers = []
        found_triggers = has_trigger_words(text, found_triggers)
        
        print(header)

        print("triggers: %s" % (found_triggers))
        return (text, found_triggers)
    except:
        print("ERROR")

    return ("", [])

def has_trigger_words(text, found_triggers): 
    for t in TRIGGERS:
        if t in text:
            found_triggers.append(t) 
    return found_triggers

############################################################

def yhmh_nlp(url):
    text, triggers = parse_my_url(url)
    print("triggers2: %s" % (triggers))
    if text is "" or len(triggers) == 0:
        return ""

    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects entities in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    entities = client.analyze_entities(document).entities
    verbose=True
    counter=0
    counter2=0
    text_output_array=pd.DataFrame(np.zeros((len(entities), 3)))

    for entity in entities:
        entity_type = enums.Entity.Type(entity.type)
        if len(entity.name)<25 and '.' not in entity.name: 
            text_output_array.iloc[counter,0]=entity.name
            text_output_array.iloc[counter,1]=entity_type.name
            text_output_array.iloc[counter,2]=entity.salience
            counter+=1
        else:
            counter2+=1

    celebrity_status = 0
    if len(entities) > 0:
        if entities[0].metadata.get('wikipedia_url', '-') !='-' and text_output_array.iloc[0,1]=='PERSON':
            celebrity_status=1
        elif entities[1].metadata.get('wikipedia_url', '-') and text_output_array.iloc[1,1]=='PERSON':
            celebrity_status=1
        else:
            celebrity_status=0
    
    text_output_array=text_output_array.iloc[0:len(entities)-counter2,:]

    # Detects the sentiment of the text
    #sentiment = client.analyze_sentiment(document=document).document_sentiment


    wns = WordNetSimilarity()

    keywords_target=pd.Series.to_list(text_output_array[0])
    #keywords_target = list(set(keywords_target))

    #seen = set(keywords_target)
    #keywords_target = []
    #for x in keywords_target:
    #    if x not in seen:
    #        keywords_target.append(x)
    #        seen.add(x)
    #
    #keywords_target=seen
    forbidden_keywords=['medicine','drug','fun','hospital','suicide','death','mental','health','illness','insta',',man','woman','family','people','many','place','same','others','brain','all','end','statement','lot','condolences']

    regex = re.compile(r'([A-Z]([a-z])+)')
    selected_files = list(filter(regex.search, keywords_target))
    res=list(set(keywords_target) - set(selected_files))

    regex = re.compile(r'^@')
    selected_files = list(filter(regex.search, res))
    res=list(set(keywords_target) - set(selected_files))

    regex = re.compile(r"\b[A-Z][A-Z]+\b")
    selected_files = list(filter(regex.search, res))
    res=list(set(res) - set(selected_files))

    regex = re.compile(r'([A-Z]([a-z])+)')
    selected_files = list(filter(regex.search, res))
    res=list(set(res) - set(selected_files))
    for key in range(len(res)):
        if ' ' in res[key]:
            res[key]=res[key].split(' ')[0]

    for x in range(len(res)):
        for y in range(len(forbidden_keywords)):
            if res[x]==forbidden_keywords[y]:
                res[x]=[]
    res = list(filter(None, res))

    res_dictionary=Counter(res)

    res_output=res_dictionary.most_common(10)
    res_output=dict(res_output)
    res_output=list(res_output.keys())
        

    print(res_output)
    res=res_output[0:num_keywords]
    database=pd.read_csv('/Users/vmutai/Projects/HMH/admin/microblog/app/yhmh_curated_articles.csv')

    if celebrity_status ==1:
        database = database[database.celebrity == 1]
    elif celebrity_status ==0:
        database = database[database.celebrity == 0]
    similarity_ranks= pd.DataFrame(np.zeros(database.shape[0]))
    for z in range(database.shape[0]):
        newlist = []
        N_rows=len(res)
        keywords_source=database.iloc[z,4:4+num_keywords]
        keywords_source=pd.Series.tolist(keywords_source)
        N_cols=len(keywords_source)
        #similarity_list = pd.DataFrame(np.zeros((N_rows, N_cols)))
        foo= [1]
        for x in range(len(res)):
            for y in range(len(keywords_source)):
                value=wns.word_similarity(res[x], keywords_source[y], 'lin')
                #similarity_matrix.at[x,y]=value
                foo.append(value)
        matrix_average=sum(foo)/np.count_nonzero(foo)
        similarity_ranks.at[z,0]=matrix_average
    maximum=pd.DataFrame.idxmax(similarity_ranks)
    url_to_return=pd.Series.tolist(database.iloc[maximum,0])
    print(url_to_return)

    title=pd.Series.tolist(database.iloc[maximum,1])
    def output(title, res_output, url_to_return):
        a = {'header': title[0], 'keywords_list': res_output, 'url_recommendation': url_to_return[0] }
        print("JSON DUMP")
        print(a)

        try:
            return json.dumps(a)
        except:
            return "awesome2!"

    json_output = output(title, res_output, url_to_return)
    print(json_output)

    return json_output

    """
    'header': title,
            'keywords_list': res_output,
            'url_recommendation': url_to_return
            }
    """


#yhmh_nlp(url)
