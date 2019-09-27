import spacy
from numpy import linalg as LA
import pickle
import itertools
import pathlib


from flask import render_template
from Application import app as flaskapp
from flask import request as flaskrequest


nlp = spacy.load('/home/jcolbert/anaconda3/envs/lexical/lib/python3.6/site-packages/en_vectors_web_lg/en_vectors_web_lg-2.0.0')


test_words = pickle.load(open('../PSUTherapy/words.p','rb'))
flaskapp.logger.info(len(test_words))
test_words=list(itertools.chain.from_iterable([test_words[key] for key in test_words.keys()]))
test_tokens=[nlp(word)[0] for word in test_words]
test_tokens=[token for token in test_tokens if token.vector_norm>.0001]

def get_scored_words(challenge):
    scores_map={token.text:challenge.similarity(token) for token in test_tokens}
    sorted_words = sorted(scores_map.items(), key=lambda kv: kv[1],reverse=True)
    return sorted_words

@flaskapp.route('/',methods=['GET','POST'])
@flaskapp.route('/index',methods=['GET','POST'])    
def index():
  scored_words = ''
  query = ''
  if flaskrequest.method == 'POST':
    form_data=dict(flaskrequest.form)
    print(form_data['word1'])
    query = form_data['word1']
    scored_words = get_scored_words(nlp(form_data['word1'][0]))[:10]
    scored_words = construct_table(scored_words)
    flaskapp.logger.info(form_data['word1'][0][:10])
  return render_template("index.html", title = 'Home', scored_words = scored_words, query = query)

def construct_table(scored_words):
    res=''
    for scored_word in scored_words:
        res+='<tr><td>{word}</td><td class="text-right">{score:0.2f}</td></tr>'.format(word=scored_word[0],score=scored_word[1])
    return res