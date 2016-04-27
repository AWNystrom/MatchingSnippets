from subprocess import Popen, PIPE
from re import compile
from tempfile import NamedTemporaryFile
import lxml

newline_re = compile('[\r\n]{2,}')
tag_re = compile(u'<[^>]+>')

def preprocess(doc):
  """
  Takes a UTF8 string, returns a unicode string. All HTML and Javascript are marked up
  and executed. All sequences of newlines are truncated to a single newline.
  """
  
  if type(doc) is not unicode:
    doc = doc.decode('utf8')
  
  #Normalize newlines as they'll define paragraphs
  return tag_re.sub(u'\n\n', doc)
  
  if type(doc) is unicode:
    doc = doc.encode('utf8')

  with NamedTemporaryFile(mode='w+b') as fd:
    fd.write(doc)
    fd.seek(0)
    p = Popen(['links', fd.name, '-dump'], stdout=PIPE)
    doc, _ = p.communicate()
    
  doc = newline_re.sub(doc, '\n\n')
  return doc.decode('utf8')