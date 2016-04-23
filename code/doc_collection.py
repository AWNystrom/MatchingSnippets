from spacy.en import English
from itertools import izip
from simhash import SimhashIndex, Simhash
from code import interact
from ast import literal_eval as make_tuple

"""
ASSUMPTIONS:
The input is text.
The text is English.
We know the author of each of the original documents.


Improvements:
Track IDs for authors and titles to lower storage space.
Preprocess input to remove metadata (no cheating)
"""

from preprocess import preprocess

class DocCollection(object):
  def __init__(self, hash_size=128, hash_tol=4):
    """
    Params:
      hash_size : The number of output bits of the hash function used in SimHash
      hash_tol  : The number of bits that can differ for a candidate near-match in Simhash
    """
    self.hash_size = hash_size
    self.hash_tol = hash_tol
    self.nlp = English()
    self.simhash_index = SimhashIndex(objs=[], f=self.hash_size, k=self.hash_tol)
    self.simhasher = Simhash(u'', self.hash_size)
  
  def get_sents_and_hashes(self, doc):
    build_by_features = self.simhasher.build_by_features
    simhasher = self.simhasher
    nlp = self.nlp
    sents_and_hashes = []
    hash_size = self.hash_size
    
    #Parsing and tagging at the same time gives better parsing accuracy,
    #but we don't need entities
    i = -1
    
    parsed_doc = nlp(doc, parse=True, tag=True, entity=False)
    for sent in parsed_doc.sents:
      sent = parsed_doc[sent.start: sent.end]
      
      #Words will be used for document identification. Semantics are indicative of topic
      word_toks = [t.text for t in sent]
      
      sh = Simhash(u'', hash_size)
      sh.build_by_features(word_toks)
      
      i += 1
      sents_and_hashes.append((sent, sh, i))
      
    return sents_and_hashes
    
  def add(self, doc, title, author):
    add_to_index = self.simhash_index.add
    doc = preprocess(doc)
    
    #Index each sentence in the document
    for sent, simhash, sent_id in self.get_sents_and_hashes(doc):
      
      #Words will be used for document identification. Semantics are indicative of topic
      add_to_index((title, author, sent_id), simhash)
      
      #The parse is for authorship identification. Syntax is indicative of author.
      syntax_toks = [t.dep for t in sent]
        
  def get_best_match(self, snippet):
    matches_list = []
    get_matches = self.simhash_index.get_near_dups
    
    for sent, simhash, sent_id in self.get_sents_and_hashes(snippet):
      matches_list.append(get_matches(simhash))
    
    #Chance for improvement!
    #It's possible that the same doc matched in multiple places for a single sentence.
    #Since we store sentence number in the Simhash index, it's possible to find the best
    #alignment within a single doc.
    
    #Chance for improvement!
    #Prune matches with edit distance
    
    guess_to_match_count = {}
    for matches in matches_list:
      for match in matches:
        book, author, sent_id = make_tuple(match)
        k = (book, author)
        guess_to_match_count[k] = guess_to_match_count.get(k, 0) + 1
    print guess_to_match_count
    if not guess_to_match_count:
      return ((None, None), None)
    return max(guess_to_match_count.iteritems(), key=lambda item: item[1])

  def clear(self):
    self.simhash_index = SimhashIndex(objs=[], f=self.hash_size, k=self.hash_tol)