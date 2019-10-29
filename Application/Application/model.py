import spacy
from numpy import linalg as LA
import pickle
import itertools
import pathlib
from spacy.lang.en.stop_words import STOP_WORDS

print("start loading model")

nlp = spacy.load('/home/jcolbert/anaconda3/envs/lexical/lib/python3.6/site-packages/en_vectors_web_lg/en_vectors_web_lg-2.0.0')
for word in STOP_WORDS:
    for w in (word, word[0].capitalize(), word.upper()):
        lex = nlp.vocab[w]
        lex.is_stop = True
        
test_words = pickle.load(open('../PSUTherapy/words.p','rb'))
test_words=list(itertools.chain.from_iterable([test_words[key] for key in test_words.keys()]))
test_tokens=[nlp(word)[0] for word in test_words]
test_tokens=[token for token in test_tokens if token.vector_norm>.0001]

print("finished loading model")


def get_scored_words(challenge):
    scores_map={token.text:challenge.similarity(token) for token in test_tokens}
    sorted_words = sorted(scores_map.items(), key=lambda kv: kv[1],reverse=True)
    return sorted_words

def construct_table(scored_words):
    res=''
    for i, scored_word in enumerate(scored_words):
        res+='<tr><td>{i}</td><td>{word}</td><td class="text-right">{score:0.2f}</td></tr>'.format(i=i+1,word=scored_word[0],score=scored_word[1])
    return res

def get_table_from_query(query):
    query = nlp(query.lower())
    query=nlp(''.join([token.string for token in query if not token.is_stop]))
    scored_words = get_scored_words(query)[:10]
    table= construct_table(scored_words)
    return table

def get_scored_words_dict(query):
    query = nlp(query)
    query=nlp(''.join([token.string for token in query if not token.is_stop]))
    scores_map={token.text:query.similarity(token) for token in test_tokens}
    sorted_words = sorted(scores_map.items(), key=lambda kv: kv[1],reverse=True)
    return [{"word":scored_word[0],"score":scored_word[1]} for scored_word in sorted_words]
