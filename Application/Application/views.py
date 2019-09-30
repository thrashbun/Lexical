import spacy
from numpy import linalg as LA
import pickle
import itertools
import pathlib
from spacy.lang.en.stop_words import STOP_WORDS

from flask import render_template
from Application import app as flaskapp
from flask import request as flaskrequest
from flask import jsonify


nlp = spacy.load('/home/jcolbert/anaconda3/envs/lexical/lib/python3.6/site-packages/en_vectors_web_lg/en_vectors_web_lg-2.0.0')
for word in STOP_WORDS:
    for w in (word, word[0].capitalize(), word.upper()):
        lex = nlp.vocab[w]
        lex.is_stop = True

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
    query = nlp(form_data['word1'][0].lower())
    query=nlp(''.join([token.string for token in query if not token.is_stop]))
    scored_words = get_scored_words(query)[:10]
    scored_words = construct_table(scored_words)
    flaskapp.logger.info(query)
  return render_template("index.html", title = 'Home', scored_words = scored_words, query = query)

def construct_table(scored_words):
    res=''
    for scored_word in scored_words:
        res+='<tr><td>{word}</td><td class="text-right">{score:0.2f}</td></tr>'.format(word=scored_word[0],score=scored_word[1])
    return res

@flaskapp.route('/api',methods=['GET'])  
def api():
    scored_words = ''
    query = ''
    query = nlp(flaskrequest.args.get("query").lower())
    query=nlp(''.join([token.string for token in query if not token.is_stop]))
    scored_words = get_scored_words_dict(query)[:10]
    flaskapp.logger.info(query)
    return jsonify(scored_words)

def get_scored_words_dict(challenge):
    scores_map={token.text:challenge.similarity(token) for token in test_tokens}
    sorted_words = sorted(scores_map.items(), key=lambda kv: kv[1],reverse=True)
    return [{"word":scored_word[0],"score":scored_word[1]} for scored_word in sorted_words]
