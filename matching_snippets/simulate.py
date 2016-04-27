from doc_collection import DocCollection
from os import listdir
from random import choice, random
from preprocess import preprocess
from code import interact
from copy import copy
from utils import corrupt_text, corrupt_book
      
def identify_with_corruption(collection, author_to_books, prob_para=0.1, prob_tok=0.5, prob_mutate=0.5):
  #Simulate identifying which work a snippet came from 
  # when the snippet came from the initial collection
  
  #This is just measuring accuracy. Do something better in reality.
  
  print 'Testing with'
  print 'prob_para=%s, prob_tok=%s, prob_mutate=%s' % (prob_para, prob_tok, prob_mutate)
  
  right, wrong = 0., 0.
  for author in author_to_books:
    for title, doc in author_to_books[author]:
    
      #Corrupt the book
      doc = corrupt_book(doc, prob_para=0.1, prob_tok=0.2, prob_mutate=0.5)
    
      print '\n'
      print 'Actual:', title, author
      pred = collection.get_best_match(doc)
      print 'Predition'
      print pred
      

      pred_title = pred['title']
      pred_author = pred['author']
    
      if pred_title == title and pred_author == author:
        right += 1
        print 'CORRECT'
      else:
        wrong += 1
        print 'INCORRECT'
      
      print '\n'
      print '-'*80
  
  print 'Got EVERYTHING right %s%% of the time. Obviously needs tuning.' % (100.*right / (right+wrong),)
    
if __name__ == '__main__':
  author_to_books = {}
  
  for author in listdir('data/in_sample'):
    author_to_books[author] = []
    for title in listdir('data/in_sample/' + author):
      filename = 'data/in_sample/%s/%s' % (author, title)
      doc = preprocess(open(filename).read())
      author_to_books[author].append((title, doc))
  
  for author in listdir('data/out_of_sample'):
    for title in listdir('data/out_of_sample/' + author):
      filename = 'data/out_of_sample/%s/%s' % (author, title)
      doc = preprocess(open(filename).read())
      author_to_books[author].append((None, doc))

  #Put all the documents into the collection
  collection = DocCollection()
  for author, title_doc in author_to_books.iteritems():
    print author
    for title, doc in title_doc:
      if title is not None: #Don't add the out of sample books
        collection.add(doc, title, author)
      else:
        print 'Not using one by', author
  
  #Corrupt books and see if we can recognize them
  identify_with_corruption(collection, author_to_books)