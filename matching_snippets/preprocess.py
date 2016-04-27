from re import compile

tag_re = compile(u'<[^>]+>')

def preprocess(doc):
  """
  Takes a UTF8 string, returns a unicode string. Strips out HTML.
  """
  
  if type(doc) is not unicode:
    doc = doc.decode('utf8')
  
  #Normalize newlines as they'll define paragraphs
  return tag_re.sub(u'\n\n', doc)