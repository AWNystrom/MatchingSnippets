#from online_gaussian_naive_bayes import OnlineGaussianNaiveBayes
from numpy import array, log
from nltk import trigrams, FreqDist, KneserNeyProbDist
from code import interact

stopword_set =  set([u'a',
                     u'about',
                     u'above',
                     u'across',
                     u'after',
                     u'afterwards',
                     u'again',
                     u'against',
                     u'all',
                     u'almost',
                     u'alone',
                     u'along',
                     u'already',
                     u'also',
                     u'although',
                     u'always',
                     u'am',
                     u'among',
                     u'amongst',
                     u'amoungst',
                     u'amount',
                     u'an',
                     u'and',
                     u'another',
                     u'any',
                     u'anyhow',
                     u'anyone',
                     u'anything',
                     u'anyway',
                     u'anywhere',
                     u'are',
                     u'around',
                     u'as',
                     u'at',
                     u'back',
                     u'be',
                     u'became',
                     u'because',
                     u'become',
                     u'becomes',
                     u'becoming',
                     u'been',
                     u'before',
                     u'beforehand',
                     u'behind',
                     u'being',
                     u'below',
                     u'beside',
                     u'besides',
                     u'between',
                     u'beyond',
                     u'bill',
                     u'both',
                     u'bottom',
                     u'but',
                     u'by',
                     u'call',
                     u'can',
                     u'cannot',
                     u'cant',
                     u'co',
                     u'computer',
                     u'con',
                     u'could',
                     u'couldnt',
                     u'cry',
                     u'de',
                     u'describe',
                     u'detail',
                     u'did',
                     u'didn',
                     u'do',
                     u'does',
                     u'doesn',
                     u'doing',
                     u'don',
                     u'done',
                     u'down',
                     u'due',
                     u'during',
                     u'each',
                     u'eg',
                     u'eight',
                     u'either',
                     u'eleven',
                     u'else',
                     u'elsewhere',
                     u'empty',
                     u'enough',
                     u'etc',
                     u'even',
                     u'ever',
                     u'every',
                     u'everyone',
                     u'everything',
                     u'everywhere',
                     u'except',
                     u'few',
                     u'fifteen',
                     u'fify',
                     u'fill',
                     u'find',
                     u'fire',
                     u'first',
                     u'five',
                     u'for',
                     u'former',
                     u'formerly',
                     u'forty',
                     u'found',
                     u'four',
                     u'from',
                     u'front',
                     u'full',
                     u'further',
                     u'get',
                     u'give',
                     u'go',
                     u'had',
                     u'has',
                     u'hasnt',
                     u'have',
                     u'he',
                     u'hence',
                     u'her',
                     u'here',
                     u'hereafter',
                     u'hereby',
                     u'herein',
                     u'hereupon',
                     u'hers',
                     u'herself',
                     u'him',
                     u'himself',
                     u'his',
                     u'how',
                     u'however',
                     u'hundred',
                     u'i',
                     u'ie',
                     u'if',
                     u'in',
                     u'inc',
                     u'indeed',
                     u'interest',
                     u'into',
                     u'is',
                     u'it',
                     u'its',
                     u'itself',
                     u'just',
                     u'keep',
                     u'kg',
                     u'km',
                     u'last',
                     u'latter',
                     u'latterly',
                     u'least',
                     u'less',
                     u'ltd',
                     u'made',
                     u'make',
                     u'many',
                     u'may',
                     u'me',
                     u'meanwhile',
                     u'might',
                     u'mill',
                     u'mine',
                     u'more',
                     u'moreover',
                     u'most',
                     u'mostly',
                     u'move',
                     u'much',
                     u'must',
                     u'my',
                     u'myself',
                     u'name',
                     u'namely',
                     u'neither',
                     u'never',
                     u'nevertheless',
                     u'next',
                     u'nine',
                     u'no',
                     u'nobody',
                     u'none',
                     u'noone',
                     u'nor',
                     u'not',
                     u'nothing',
                     u'now',
                     u'nowhere',
                     u'of',
                     u'off',
                     u'often',
                     u'on',
                     u'once',
                     u'one',
                     u'only',
                     u'onto',
                     u'or',
                     u'other',
                     u'others',
                     u'otherwise',
                     u'our',
                     u'ours',
                     u'ourselves',
                     u'out',
                     u'over',
                     u'own',
                     u'part',
                     u'per',
                     u'perhaps',
                     u'please',
                     u'put',
                     u'quite',
                     u'rather',
                     u're',
                     u'really',
                     u'regarding',
                     u'same',
                     u'say',
                     u'see',
                     u'seem',
                     u'seemed',
                     u'seeming',
                     u'seems',
                     u'serious',
                     u'several',
                     u'she',
                     u'should',
                     u'show',
                     u'side',
                     u'since',
                     u'sincere',
                     u'six',
                     u'sixty',
                     u'so',
                     u'some',
                     u'somehow',
                     u'someone',
                     u'something',
                     u'sometime',
                     u'sometimes',
                     u'somewhere',
                     u'still',
                     u'such',
                     u'system',
                     u'take',
                     u'ten',
                     u'than',
                     u'that',
                     u'the',
                     u'their',
                     u'them',
                     u'themselves',
                     u'then',
                     u'thence',
                     u'there',
                     u'thereafter',
                     u'thereby',
                     u'therefore',
                     u'therein',
                     u'thereupon',
                     u'these',
                     u'they',
                     u'thick',
                     u'thin',
                     u'third',
                     u'this',
                     u'those',
                     u'though',
                     u'three',
                     u'through',
                     u'throughout',
                     u'thru',
                     u'thus',
                     u'to',
                     u'together',
                     u'too',
                     u'top',
                     u'toward',
                     u'towards',
                     u'twelve',
                     u'twenty',
                     u'two',
                     u'un',
                     u'under',
                     u'unless',
                     u'until',
                     u'up',
                     u'upon',
                     u'us',
                     u'used',
                     u'using',
                     u'various',
                     u'very',
                     u'via',
                     u'was',
                     u'we',
                     u'well',
                     u'were',
                     u'what',
                     u'whatever',
                     u'when',
                     u'whence',
                     u'whenever',
                     u'where',
                     u'whereafter',
                     u'whereas',
                     u'whereby',
                     u'wherein',
                     u'whereupon',
                     u'wherever',
                     u'whether',
                     u'which',
                     u'while',
                     u'whither',
                     u'who',
                     u'whoever',
                     u'whole',
                     u'whom',
                     u'whose',
                     u'why',
                     u'will',
                     u'with',
                     u'within',
                     u'without',
                     u'would',
                     u'yet',
                     u'you',
                     u'your',
                     u'yours',
                     u'yourself',
                     u'yourselves'])

dep_tags =  [u'',
             u'ROOT',
             u'acl',
             u'acomp',
             u'advcl',
             u'advmod',
             u'agent',
             u'amod',
             u'appos',
             u'attr',
             u'aux',
             u'auxpass',
             u'case',
             u'cc',
             u'ccomp',
             u'compound',
             u'conj',
             u'csubj',
             u'csubjpass',
             u'dative',
             u'dep',
             u'det',
             u'dobj',
             u'expl',
             u'intj',
             u'mark',
             u'meta',
             u'neg',
             u'nmod',
             u'npadvmod',
             u'nsubj',
             u'nsubjpass',
             u'nummod',
             u'oprd',
             u'parataxis',
             u'pcomp',
             u'pobj',
             u'poss',
             u'preconj',
             u'predet',
             u'prep',
             u'prt',
             u'punct',
             u'quantmod',
             u'relcl',
             u'xcomp']

dep_tag_set = set(dep_tags)

punct = u'.-!,;:'

from scipy.spatial.distance import euclidean

def closest_from_mean_vec(vec, model):
  return min((euclidean(vec, mean_vec), author) for author, mean_vec in model.mean_.items())[1]

def get_token_shapes(tokens):
  new_tokens = []
  for t in tokens:
    t = t.lower()
    if t in stopword_set:
      new_tokens.append('STOP')
    elif t in punct:
      new_tokens.append(t)
    else:
      #Create a new token based on the word length
      tok_len = len(t)
      if tok_len < 7:
        new_tokens.append('SHORT')
      elif tok_len < 12:
        new_tokens.append('MEDIUM')
      else:
        new_tokens.append('LONG')
  return new_tokens

class LanguageModelAuthorIdentifier(object):
  def __init__(self, smoothing=10**-10):
    self.smoothing = smoothing #used when a probability is zero 
                               #(happens when an ngram has no parts that have been seen)
    self.freqdists = {}
    self.prob_dists = {}
    self.needs_probs_recounted = {} #True if the underlying freq dist has been changed
                                    #but the kneser ney counts haven't been updated
  
  def add_doc(self, tokens, author):
    shape_toks = get_token_shapes(tokens)
    
    if author not in self.freqdists:
      self.freqdists[author] = FreqDist()
      self.prob_dists[author] = KneserNeyProbDist(self.freqdists[author])
      self.needs_probs_recounted[author] = True
    fd = FreqDist(trigrams(shape_toks))
    self.freqdists[author].update(fd)
  
  def predict_author(self, tokens):
    shape_toks = get_token_shapes(tokens)
    
    needs_probs_recounted = self.needs_probs_recounted
    prob_dists = self.prob_dists
    freqdists = self.freqdists
    smoothing = self.smoothing
    
    for author in freqdists:
      #Only recount those that have since been modified (by having a doc added)
      if needs_probs_recounted[author]:
        prob_dists[author] = KneserNeyProbDist(freqdists[author])
        self.needs_probs_recounted[author] = False
    
    best_score = None
    likely_author = None
    for author, probdist in prob_dists.iteritems():
      probs = array([probdist.prob(trigram) for trigram in trigrams(shape_toks)], dtype='float')
      score = log(probs + smoothing).sum()
      
      if score > best_score:
        likely_author = author
        best_score = score
        
    return likely_author, best_score

class GaussianAuthorIdentifier(object):
  def __init__(self):
    self.author_to_model = {}
    self.D = len(self.doc_to_features([]))
    self.model = OnlineGaussianNaiveBayes(self.D, priors=False)
    
  def doc_to_features(self, sent):
    n_words = len(sent) if len(sent) else 1
    
    #Counts of puncts
    punct_dist = {p: 0 for p in punct}
    for t in sent:
      if t.text in punct:
        punct_dist[t.text] = punct_dist.get(t.text, 0) + 1
    
    dep_dist = {}
    for t in sent:
      if t.dep_ in dep_tag_set:
        dep_dist[t.dep_] = dep_dist.get(t.dep_, 0) + 1
    
    #Number of stopwords
    stopword_ratio = 1.*sum(1 for t in sent if t.text in stopword_set) / n_words
            
    #Average word length
    mean_word_len = 1.*sum(len(t) for t in sent) / n_words
    
    vec = [stopword_ratio, mean_word_len]
    vec.extend([1.*punct_dist.get(p, 0.)/n_words for p in punct])
    vec.extend([1.*dep_dist.get(d, 0.)/n_words for d in dep_tags])
    return vec
    
  def add_doc(self, spacy_sents, author):
    author_to_model = self.author_to_model
    doc_to_features = self.doc_to_features
    model = self.model
    
    for sent in spacy_sents:
      v = doc_to_features(sent)
      model.fit(v, author)
    
  def predict_author(self, spacy_sents):
    doc_to_features = self.doc_to_features
    
    author_to_score = {}
    for sent in spacy_sents:
      v = doc_to_features(sent)
      score, author = self.model.predict(v)
      author_to_score[author] = author_to_score.get(author, 0) + score
    
    #Return the author that seemed to have written the most sentences in this doc.
    return max(author_to_score.iteritems(), key=lambda item: item[1])[0]