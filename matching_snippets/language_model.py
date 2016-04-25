from nltk import FreqDist, KneserNeyProbDist, trigrams#, NgramModel
from itertools import chain

class KneserNeyModel(object):
  def __init__(self, order):
    pass
    
  def fit(self, tokenized_docs):
    trigrams = trigrams(chain(toks for toks in tokenized_docs))
    self.freqs_dist = FreqDist(trigrams)
    self.prob_dist = KneserNeyProbDist(self.freqs_dist)
  
  def get_prob(self, tokens):
    pass#return self.prob_dist.()

def generate(kn, context, num):
  a,b = context[-2:]
  generated = []
  for i in xrange(num):
  
    #Get weights for next sample
    candidates = [(k, f) for k, f in kn._trigrams.iteritems() if k[:2] == (a, b)]
    if not candidates:
      candidates = [(k, f) for k, f in kn._bigrams.iteritems() if k[:1] == (b,)]
    if not candidates:
      #We're in the dark. This is total guessing.
      candidates = [(k, f) for k, f in kn._unigrams.items()]
      
    words, weights = zip(*candidates)
    total = sum(weight)
    weights = [1.*w/total for w in weights]
    c = choice(words, 1, p=weights)
    generated.append(c)
    a = b
    b = c
  return generated

if __name__ == '__main__':
  from cPickle import load
  from code import interact
  tokens = load(open('animal_farm_toks'))
  fd = FreqDist(trigrams(tokens))
  kn = KneserNeyProbDist(fd)
  interact(local=locals())
  #http://www.gilesthomas.com/2010/05/generating-political-news-using-nltk/
  #content_model = NgramModel(3, tokenized_content)
  #starting_words = content_model.generate(100)[-2:]
  #content = content_model.generate(words_to_generate, starting_words)
  #print u' '.join(content)