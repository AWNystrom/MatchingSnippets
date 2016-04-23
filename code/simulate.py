from doc_collection import DocCollection
from os import listdir
from random import choice, random
from string import letters, digits, punctuation
from preprocess import preprocess
from code import interact

corruption_prob = 0.001 #Probability of a character corruption
chars = unicode(letters) + unicode(digits) + unicode(punctuation)

snippet_size = 5000 #number of characters

def corrupt_text(text, prob):
  new_text = []
  for c in text:
    if random() <= prob:
      #Corrupt the character
      new_text.append(choice(chars))
    else:
      new_text.append(c)
  return u''.join(new_text)

if __name__ == '__main__':
  authors = listdir('data')
  author_to_books = {}

  for author in authors:
    author_to_books[author] = []
    for title in listdir('data/' + author):
      filename = 'data/%s/%s' % (author, title)
      doc = open(filename).read()
      doc = preprocess(doc)
      author_to_books[author].append((title, doc))

  #Simulate identifying which work a snippet came from 
  # when the snippet came from the initial collection

  collection = DocCollection()
  for author, title_doc in author_to_books.iteritems():
    print author
    for title, doc in title_doc:
      collection.add(doc, title, author)

  right, wrong = 0., 0.
  for iter in xrange(100):
    #Randomly select an author
    author = choice(author_to_books.keys())
  
    #Randomly select a book
    title, doc = choice(author_to_books[author])
  
    #Randomly select a snippet
    start_ind = choice(range(len(doc)-snippet_size))
    snippet = doc[start_ind: start_ind + snippet_size]
    
    #Corrupt the snippet
    snippet = corrupt_text(snippet, corruption_prob)
    
    print 'Actual:', title, author
    pred = collection.get_best_match(snippet)
    print pred

    (pred_title, pred_author), count = pred
    
    if pred_title == title and pred_author == author:
      right += 1
    else:
      wrong += 1
      
    print right / (right + wrong)
    print '_'*80
    
#    interact(local=locals())