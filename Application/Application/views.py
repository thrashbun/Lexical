from flask import render_template
from Application import app as flaskapp
from flask import request as flaskrequest
from flask import jsonify

from Application import model

@flaskapp.route('/',methods=['GET','POST'])
@flaskapp.route('/index',methods=['GET','POST'])    
def index():
  scored_words = ''
  query = ''
  if flaskrequest.method == 'POST':
    form_data=dict(flaskrequest.form)
    query = form_data['word1'][0].lower()
    scored_words = model.get_table_from_query(scored_words)
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
    query = flaskrequest.args.get("query").lower()
    scored_words = model.get_scored_words_dict(query)[:10]
    flaskapp.logger.info(query)
    response=jsonify(scored_words)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
