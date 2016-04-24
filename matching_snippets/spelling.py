from simhash import Simhash, SimhashIndex
from editdistance import eval as levenshtein
from utils import all_min_or_max
from random import choice

class SpellingCorrector(object):
  def __init__(self, vocab_to_freq, f=64, k=32):
    self.vocab_to_freq = vocab_to_freq
    self.simhash_index = SimhashIndex([], f=f, k=k)
    self.f = f
    self.k = k
    
    simhash_index = self.simhash_index
    for w in vocab_to_freq:
      sh = Simhash(w, f=f)
      simhash_index.add(w, sh)
  
  def add_valid_word(self, word):
    if word not in self.vocab_to_freq:
      sh = Simhash(word, self.f)
      self.simhash_index.add(word, sh)
    self.vocab_to_freq[word] = self.vocab_to_freq.get(word, 0) + 1
    
  def correct_word(self, word):
    
    if word in self.vocab_to_freq:
      return word
    
    #Edit distance between
    sh = Simhash(word, f=self.f)
    candidates = self.simhash_index.get_near_dups(sh)
    
    if not candidates:
      #No near dups. Oh well. This word will go as it is.
      print 'no candidates'
      return word
    
    if len(candidates) == 1:
      #Only one candidate, so assume this is the correction
      return candidates[0]
      
    lev_dist_gen = ((other_w, levenshtein(other_w, word)) for other_w in candidates)
    closest_words, dists = zip(*all_min_or_max(lev_dist_gen, min, lambda item: item[1]))
    
    if len(closest_words) == 1:
      #One of the candidates had the best edit distance. Return that.
      return closest_words[0]
    
    #OK, there are multiple closest words. Rely on word frequency to choose the right one.
    vocab_to_freq = self.vocab_to_freq
    word_freq_gen = ((other_w, vocab_to_freq[other_w]) for other_w in closest_words)
    most_freq_words, freqs = zip(*all_min_or_max(word_freq_gen, max, lambda item: item[1]))
    
    #using choice because at this point there's no other way to narrow it down, unless we
    #track higher order ngrams.
    return choice(most_freq_words)