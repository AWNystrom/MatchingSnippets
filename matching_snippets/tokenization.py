from spacy.en import English
from re import compile
from preprocess import preprocess

#Yeah, this will be shared with anything that imports it. No multiprocessing, OK?
nlp = English()

para_re = compile(u'(\r\n|\n){2,}')

possible_endings = u'.!?"'

def extract_paragraphs(doc):
  
  paras = [p.strip() for p in para_re.split(doc)]
  paras = [p for p in paras if p and p[-1] in possible_endings]
  return paras

def tokenize(doc):
  return [t.text for t in nlp(doc, tag=False, parse=False, entity=False)]