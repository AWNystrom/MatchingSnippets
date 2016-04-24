from doc_collection import DocCollection
from os import listdir
from random import choice, random
from preprocess import preprocess
from code import interact

from utils import corrupt_text

def identify_from_sample(collection, author_to_books, iters, corruption_prob, snippet_size):
  #Simulate identifying which work a snippet came from 
  # when the snippet came from the initial collection

  right, wrong = 0., 0.
  for iter in xrange(iters):
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
    
  return right / (right+wrong)
    
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

  collection = DocCollection()
  for author, title_doc in author_to_books.iteritems():
    print author
    for title, doc in title_doc:
      collection.add(doc, title, author)
      
  interact(local=locals())