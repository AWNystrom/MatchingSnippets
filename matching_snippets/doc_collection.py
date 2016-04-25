from spacy.en import English
from itertools import izip, chain
from simhash import SimhashIndex, Simhash, logging
from ast import literal_eval as make_tuple
from editdistance import eval as levenshtein
from random import choice, shuffle
from code import interact

logging.disable(logging.warning)

from author_identifier import AuthorIdentifier
from utils import all_min_or_max
from tokenization import extract_paragraphs, tokenize

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
from spelling import SpellingCorrector

class DocCollection(object):
  def __init__(self, hash_size=64, hash_tol=2):
    """
    Params:
      hash_size : The number of output bits of the hash function used in SimHash.
                  Higher values -> able to handle more noise.
      hash_tol  : The number of bits that can differ for a candidate near-match in Simhash
    """
    self.hash_size = hash_size
    self.hash_tol = hash_tol
    self.simhash_index = SimhashIndex(objs=[], f=self.hash_size, k=self.hash_tol)
    #self.author_identifier = AuthorIdentifier()
  
  def generate_simhash(self, tokens):
    #Generate a Simhash from Spacy tokens.
    sh = Simhash(u'', f=self.hash_size) #silly interface...
    sh.build_by_features(tokens)
    return sh
    
  def add(self, doc, title, author):
    add_to_index = self.simhash_index.add
    doc = preprocess(doc)
    #author_identifier = self.author_identifier
    
    #Index each paragraph in the document into the simhash index
    for para in extract_paragraphs(doc):
      tokens = [t.text for t in tokenize(para)]
      if not tokens:
        continue
      sh = self.generate_simhash(tokens)
      self.simhash_index.add((tokens, title, author), sh)
        
  def get_best_match(self, snippet):
    get_near_dups = self.simhash_index.get_near_dups
    generate_simhash = self.generate_simhash
    title_author_to_count = {}
    
    paras = extract_paragraphs(snippet)
    shuffle(paras)
    
    #For each paragraph, get the closest matching previously encountered paragraphs.
    #If multiple matches, prune via edit distance.
    #The work of art that matches the most paragraphs is the winner (if it matches enough)
    for paras_done, para in enumerate(paras, 1):
      print title_author_to_count
      #Check for early stopping if we're sure enough
      if paras_done >= 10:
        if not title_author_to_count:
          #We've seen 10 paragraphs and still have no idea. Probably out of sample.
          break
        vals = title_author_to_count.values()
        if len(title_author_to_count) == 1:
          #We've seen this many and have guessed the same work every time
          break
        #OK, we've seen more than one guess, but are we way more sure about one than the rest?
        vals.sort(reverse=True)
        others = sum(vals[1:])
        if vals[0] >= 2*others:
          break #yeah, we're pretty sure it's this one.
        
      
      tokens = [t.text for t in tokenize(para)]
      sh = generate_simhash(tokens)
      candidates = [make_tuple(match) for match in get_near_dups(sh)]
      print 'len(candidates)', len(candidates)
      
      """if not candidates:
        continue
      elif len(candidates) > 1:
        #Prune the candidates via edit distance
        dists = [levenshtein(tokens, other_tokens) for other_tokens, _, _ in candidates]
        best_candidate_inds = zip(*all_min_or_max(enumerate(dists), min, lambda item: item[1]))[0]
        if len(best_candidate_inds) > 1:
          #Ties? Just pick one...
          best_candidate_ind = choice(best_candidate_inds)
        else:
          best_candidate_ind = best_candidate_inds[0]
        best_match = candidates[best_candidate_ind]
      else:
        #This was the only candidate
        best_match = candidates[0]"""
      
      for candidate in candidates:
        _, title, author = candidate
        k = (title, author)
        title_author_to_count[k] = title_author_to_count.get(k, 0) + 1
      #Increment the count of this work
      #_, title, author = best_match
      #k = (title, author)
      #title_author_to_count[k] = title_author_to_count.get(k, 0) + 1
    
    #author_guess = self.author_identifier.predict_author(elem[0] for elem in sents_and_hashes)
    
    if not title_author_to_count:
      return ((None, None), 0.)
    
    #OK, what work was the most frequent, and what was that frequency?
    (title, author), f = max(title_author_to_count.iteritems(), key=lambda item: item[1])
    
    score = 1.*f/paras_done
    if score >= 0.3:
      return (title, author), score
    
    return ((None, None), score)

  def clear(self):
    self.simhash_index = SimhashIndex(objs=[], f=self.hash_size, k=self.hash_tol)