from nltk import FreqDist, KneserNeyProbDist, trigrams, SimpleGoodTuringProbDist#, NgramModel
from itertools import chain
from numpy.random import choice
from numpy import array, argmax
from code import interact

class SemanticLanguageModels(object):
  def __init__(self, smoothing=10**-10):
    self.smoothing = smoothing #used when a probability is zero 
                               #(happens when an ngram has no parts that have been seen)
    self.freqdists = {}
    self.prob_dists = {}
    self.needs_probs_recounted = {} #True if the underlying freq dist has been changed
                                    #but the kneser ney counts haven't been updated
  
  def add_doc(self, tokens, author):
    if author not in self.freqdists:
      self.freqdists[author] = FreqDist()
      self.prob_dists[author] = KneserNeyProbDist(self.freqdists[author])
      self.needs_probs_recounted[author] = True
    fd = FreqDist(trigrams(tokens))
    self.freqdists[author].update(fd)
    
  def complete(self, author, tokens, num_words, iters=100):
    if self.needs_probs_recounted[author]:
      self.prob_dists[author] = KneserNeyProbDist(self.freqdists[author])
      add_unigrams(self.prob_dists[author])
    
    context_tokens = list(tokens)
    #Chop off the end of tokens until we see a bigram we know.
    while context_tokens:
      if tuple(context_tokens[-2:]) in self.prob_dists[author]._bigrams:
        break
      context_tokens.pop(-1)
    
    context = tuple(context_tokens[-2:]) if context_tokens else (None, None)
    probdist = self.prob_dists[author]
    completion = generate(probdist, context, num_words, iters)
    return completion

def generate(kn, context, num, iters, maxprob=False):
  #Sample the next word, word by word.
  print 'Given as context', context
  """
  params:
    kn : A Kneser Ney distribution of trigrams
    context : the first two words to seed with
    num : the number of words to generate
    iters : the number of iterations to try
    maxprob : whether to just choose the most likely each time. Often gets stuck in a rut.
  """
  
  best_generated = []
  best_score = None
  
  if maxprob:
    iters = 1
  
  #Try generating it a bunch of times and keep the one with the highest probability
  #according to kneser ney
  for iteration in xrange(iters):
    trigram_frequency = {} #Track it so we can avoid loops
    a, b = context[-2], context[-1]
    generated = [a, b]
    for i in xrange(num):
      #Get weights for next sample
      candidates = [(k[-1], f) for k, f in kn._trigrams.iteritems() if k[:2] == (a, b) and \
                                                trigram_frequency.get((a,b,k[-1]), 0) < 1]
      if not candidates:
        candidates = [(k[-1], f) for k, f in kn._bigrams.iteritems() if k[:1] == (b,) and \
                                                trigram_frequency.get((a,b,k[-1]), 0) < 1]
      if not candidates:
        #We're in the dark. This is total guessing.
        candidates = [(k, f) for k, f in kn._unigrams.items()]
      
      words, weights = zip(*candidates)
      weights = array([kn.prob((a,b,w)) for w in words])
      
      if maxprob:
        word_index = argmax(weights)
        next_word = words[word_index]
      else:
        weights = array(weights, dtype='float')
        weights /= weights.sum()
        next_word = choice(words, 1, p=weights)[0]
        
      generated.append(next_word)
      a = b
      b = next_word
      
      trigram_frequency[(a,b,next_word)] = trigram_frequency.get((a,b,next_word), 0) + 1

    prob = reduce(lambda p1, p2: p1*p2, (kn.prob(trigram) for trigram in trigrams(generated[2:])), 1.)
    
    if prob > best_score:
      best_generated = list(generated)
      best_score = prob
  return best_generated, best_score**(1./num) #geometric mean

def add_unigrams(kn):
  unigrams = {}
  for k, v in kn._bigrams.iteritems():
    for w in k:
      unigrams[w] = unigrams.get(w, 0) + 1.
  kn._unigrams = unigrams

if __name__ == '__main__':
  from cPickle import load
  from code import interact
  animal_farm_toks = load(open('animal_farm_toks'))
  niniteen_eightyfour_farm_toks = load(open('1984_toks'))
  
  fd = FreqDist(trigrams(animal_farm_toks))
#  fd.update(FreqDist(trigrams(niniteen_eightyfour_farm_toks)))
  
  kn = KneserNeyProbDist(fd)
  add_unigrams(kn)
  #print generate(kn, ('the', 'day'), 10, 100)
  interact(local=locals())
  #http://www.gilesthomas.com/2010/05/generating-political-news-using-nltk/
  #content_model = NgramModel(3, tokenized_content)
  #starting_words = content_model.generate(100)[-2:]
  #content = content_model.generate(words_to_generate, starting_words)
  #print u' '.join(content)