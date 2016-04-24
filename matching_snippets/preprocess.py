from subprocess import Popen, PIPE
from re import compile
from tempfile import NamedTemporaryFile

newline_re = compile('[\r\n]+')

def preprocess(doc):
  """
  Takes a UTF8 string, returns a unicode string. All HTML and Javascript are marked up
  and executed. All sequences of newlines are truncated to a single newline.
  """
  
  if type(doc) is unicode:
    doc = doc.encode('utf8')

  with NamedTemporaryFile(mode='w+b') as fd:
    fd.write(doc)
    fd.seek(0)
    p = Popen(['links', fd.name, '-dump'], stdout=PIPE)
    doc, _ = p.communicate()
    
  doc = newline_re.sub(doc, '\n')
  return doc.decode('utf8')