from spacy.en import English
from re import compile
from preprocess import preprocess

#Yeah, this will be shared with anything that imports it. No multiprocessing, OK?

nlp = English()
para_re = compile(u'\n{2,}')

def extract_paragraphs(doc):
  doc = preprocess(doc)
  
  #Some of these will be section names/numbers etc. Could do better than this.
  paras = [p.strip() for p in para_re.split(doc)]
  paras = [p for p in paras if p]
  return paras

def tokenize(doc):
  return [t.text for t in nlp(doc, tag=False, parse=False, entity=False)]