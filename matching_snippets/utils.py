from random import choice, random
from string import letters, digits, punctuation
chars = unicode(letters) + unicode(digits) + unicode(punctuation)

def corrupt_text(text, prob):
  """
  text : the text you want corrupted
  prob : the probability that any particular character is corrupted
  """
  new_text = []
  for c in text:
    if random() <= prob:
      #Corrupt the character
      new_text.append(choice(chars))
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