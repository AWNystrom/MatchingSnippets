from spacy.en import English
from itertools import izip, chain
from simhash import SimhashIndex, Simhash, logging
from ast import literal_eval as make_tuple
from editdistance import eval as levenshtein
from random import choice, shuffle
from code import interact

logging.disable(logging.warning)

from author_identifier import LanguageModelAuthorIdentifier
from utils import all_min_or_max
from tokenization import extract_paragraphs, tokenize

"""
Improvements:
Preprocess input to remove metadata
"""

from preprocess import preprocess
from spelling import SpellingCorrector

class DocCollection(object):
  def __init__(self, hash_size=64, hash_tol=1):
    """
    Params:
      hash_size : The number of output bits of the hash function used in SimHash.
                  Higher values -> able to handle more noise.
      hash_tol  : The number of bits that can differ for a candidate near-match in Simhash
    """
    self.hash_size = hash_size
    self.hash_tol = hash_tol
    self.simhash_index = SimhashIndex(objs=[], f=self.hash_size, k=self.hash_tol)
    self.author_identifier = LanguageModelAuthorIdentifier()
  
  def generate_simhash(self, tokens):
    #Generate a Simhash from Spacy tokens.
    sh = Simhash(u'', f=self.hash_size) #silly interface...
    sh.build_by_features(tokens)
    return sh
    
  def add(self, doc, title, author):
    add_to_index = self.simhash_index.add
    doc = preprocess(doc)
    author_identifier = self.author_identifier
    
    #Index each paragraph in the document into the simhash index
    paras = extract_paragraphs(doc)
    
    #Update the word shape language model for this author
    para_toks = [tokenize(p) for p in paras]
    flat_tokens = [item for sublist in para_toks for item in sublist]
    author_identifier.add_doc(flat_tokens, author)
    
    for para_num, tokens in enumerate(para_toks, 1):
      if not tokens:
        continue
      sh = self.generate_simhash(tokens)
      self.simhash_index.add((tokens, title, author, para_num), sh)
        
  def get_best_match(self, snippet):
    get_near_dups = self.simhash_index.get_near_dups
    generate_simhash = self.generate_simhash
    title_author_to_count = {}
    
    paras = extract_paragraphs(snippet)
    
    #evenly distribute the corrupted paragraphs
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
        
        #See if we we're twice as sure as the one we're most sure about than all the rest combined
        vals = title_author_to_count.values()
        if len(title_author_to_count) == 1:
          #We've seen this many and have guessed the same work every time
          break
        #OK, we've seen more than one guess, but are we way more sure about one than the rest?
        vals.sort(reverse=True)
        others = sum(vals[1:])
        if vals[0] >= 2*others:
          break #yeah, we're pretty sure it's this one.
      
      tokens = tokenize(para)
      sh = generate_simhash(tokens)
      candidates = [make_tuple(match) for match in get_near_dups(sh)]
      
      #Increment the count of these works
      for candidate in candidates:
        _, title, author, para_num = candidate
        k = (title, author)
        title_author_to_count[k] = title_author_to_count.get(k, 0) + 1
    
    if title_author_to_count:
      #OK, what work was the most frequent, and what was that frequency?
      (title, author), f = max(title_author_to_count.iteritems(), key=lambda item: item[1])
    
      score = 1.*f/paras_done
      if score >= 0.3:
        return {'title': title, 'author': author, 'score': score, 'author_score': None}
    
    #This is either so corrupt that we can't tell what it is, or is a new work.
    #Guess the author
    tokens = [item for sublist in [tokenize(p) for p in paras] for item in sublist]
    author_guess, author_score = self.author_identifier.predict_author(tokens)
    
    return {'title': None, 'author': author_guess, 'score': None, 'author_score': author_score}

  def clear(self):
    self.simhash_index = SimhashIndex(objs=[], f=self.hash_size, k=self.hash_tol)