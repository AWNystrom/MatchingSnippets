from simhash import SimhashIndex, Simhash, logging
from ast import literal_eval as make_tuple
from random import choice, shuffle
from code import interact
from pprint import pprint

from author_identifier import LanguageModelAuthorIdentifier
from tokenization import extract_paragraphs, tokenize
from language_model import SemanticLanguageModels

logging.disable(logging.warning)

class DocCollection(object):
  def __init__(self, hash_size=64, hash_tol=3, num_words_to_complete=10):
    """
    Params:
      hash_size : The number of output bits of the hash function used in SimHash.
                  Higher values -> able to handle more noise.
      hash_tol  : The number of bits that can differ for a candidate near-match in Simhash
      
      num_words_to_complete : The number of words to complete given a context when a new
                              document is encountered in get_best_match
    """
    
    self.num_words_to_complete = num_words_to_complete
    self.hash_size = hash_size
    self.hash_tol = hash_tol
    
    #This implementation of simhash stores the index in RAM, but it could easily be
    # put on disk.
    self.simhash_index = SimhashIndex(objs=[], f=self.hash_size, k=self.hash_tol)
    self.author_identifier = LanguageModelAuthorIdentifier()
    self.author_semantic_models = SemanticLanguageModels()
  
  def generate_simhash(self, tokens):
    #Generate a Simhash from Spacy tokens.
    sh = Simhash(u'', f=self.hash_size) #silly interface...
    sh.build_by_features(tokens)
    return sh
    
  def add(self, doc, title, author):
    add_to_index = self.simhash_index.add
    
    #Index each paragraph in the document into the simhash index
    paras = extract_paragraphs(doc)
    
    #Update the word shape language model for this author
    para_toks = [tokenize(p) for p in paras]
    flat_tokens = [item for sublist in para_toks for item in sublist]
    self.author_semantic_models.add_doc(flat_tokens, author)
    
    #Update the semantic model for this author
    self.author_identifier.add_doc(flat_tokens, author)
    
    #Add each paragraph to the simhash index
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
    #shuffle(paras)
    
    #For each paragraph, get the closest matching previously encountered paragraphs.
    #If multiple matches, prune via edit distance.
    #The work of art that matches the most paragraphs is the winner (if it matches enough)
    paras_done = 0
    for para in paras:
      tokens = tokenize(para)
      if not tokens:
        continue
      paras_done += 1
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
      if score >= 0.1:
        return {'title': title, 'author': author, 
                'score': score, 'author_score': None, 
                'completion': None}
    
    #This is either so corrupt that we can't tell what it is, or is a new work.
    #Guess the author
    tokens = [item for sublist in [tokenize(p) for p in paras] for item in sublist]
    author_guess, author_score = self.author_identifier.predict_author(tokens)
    completion = self.author_semantic_models.complete(author_guess, tokens, self.num_words_to_complete, 1)
    
    return {'title': None, 'author': author_guess, 
            'score': None, 'author_score': author_score, 
            'completion': completion}

  def clear(self):
    self.simhash_index = SimhashIndex(objs=[], f=self.hash_size, k=self.hash_tol)