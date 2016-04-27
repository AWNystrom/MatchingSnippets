from numpy.random import random, choice
from tokenization import extract_paragraphs, tokenize
from string import letters, digits, punctuation
chars = unicode(letters) + unicode(digits) + unicode(punctuation)
chars_list = list(chars)

def corrupt_book(doc, prob_para, prob_tok, prob_mutate):
  """
  params:
    prob_para : the probability a paragraph will be chosen to be corrupted
    prob_tok : the probability a token within a corrupted paragraph will be chosen for
                corruption
    prob_mutate : the probability the corruption will be a mutation. 1 minus this prob
                  is the probability for deletion
  """
  paras = extract_paragraphs(doc)
  paras = [tokenize(para) for para in paras]
  num_to_corrupt = int(round(len(paras)*prob_para))
  if not num_to_corrupt:
    return doc
    
  inds_to_corrupt = choice(range(len(paras)), num_to_corrupt)
  
  for i in inds_to_corrupt:
    tokens = paras[i]
    num_toks_to_corrupt = int(round(len(tokens)*prob_tok))
    if not num_toks_to_corrupt:
      continue
    tok_inds_to_corrupt = choice(range(len(tokens)), num_toks_to_corrupt)
    for i in tok_inds_to_corrupt:      
      #Should we mutate it, or remove it?
      if random() > prob_mutate:
        #remove it
        tokens[i] = u''
      else:
        #mutate it
        tokens[i] = u''.join(choice(chars_list, len(tokens[i])))
  
  #collapse it all back down into a unicode document
  paras = [u' '.join(para) for para in paras]
  doc = u'\n\n'.join(paras)
  return doc

def corrupt_text(text, prob):
  """
  text : the text you want corrupted
  prob : the probability that any particular character is corrupted
  """
  new_text = []
  for c in text:
    if random() <= prob:
      #Corrupt the character
      new_text.append(choice(chars, 1))
    else:
      new_text.append(c)
  return u''.join(new_text)

def all_min_or_max(iterable, min_max, extractor):
  """
  params:
    iterable : the thing you want the min or max from
    funct : min or max
    key : a function that returns the thing to compare
  """
    
  iterator = iter(iterable)
  
  try:
    extrema = [next(iterator)]
  except StopIteration:
    return []
  cur_min_max_val = extractor(extrema[0])
  
  for elem in iterator:
    this_val = extractor(elem)
    if cur_min_max_val == this_val:
      #Equal, so track it
      extrema.append(elem)
      
    elif min_max(cur_min_max_val, this_val) == this_val:
      #We have a new min or max
      extrema = [elem]
      cur_min_max_val = this_val
    
    #Else this key is irrelevant as it's not a min/max
  
  return extrema