import re,os,sys,string
import collections

from time import time

if __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from langutil.tokenizer import tokenize

else:
    from langutil.tokenizer import tokenize

pattern = ['(?<!\w\.\w.)(?<![A-Z][a-z\.])(?<=\.|\?)\s',
           '(?<=[^A-Z].[.?]) #(?=[A-Z])',
           '\s\s+',
	   '\n\n+',
	   '\b([a-zA-Z]+)-[a-z]+']

class Loader:
    languageDBFolder =  ''#os.getcwd()#'/libraries/languagedb/'

    def __init__(self, langFolder):
        self.languageDBFolder = self.languageDBFolder + langFolder
   
    def processRaw(self, f, clear_newline = True, clear_dblspace = True):
        t0 = time()
        print("Processing raw text...")
        words = ''.join(f)
        words = re.sub(r'[^\x00-\x7F]+','',words).strip()
        if clear_newline: words = re.sub(r'\r\n',' ',words).strip()
        if clear_dblspace: words = re.sub(r'\s\s+',' ',words).strip()
        print("Processing raw text done in %fs" % (time() - t0))
        print("\n")
        
        return words # print first 5000 word       
        
    def readInChunks(self, file_object, chunk_size=1024):
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data
            
    def lazyRead(self, file_object):
        return file_object.readlines()
        
    def loadLarge(self, corpusname, lazy_load=False):
        print("Loading training corpus...")
        t0 = time()
        f = open(self.languageDBFolder + corpusname)
        print("Loading Corpus done in %fs" % (time() - t0))
        print("\n")
        if lazy_load:
            return self.lazyRead(f)
        else:
            return self.readInChunks(f)

    def rawForLangmodel(self,f,punct_remove=False):
        tok = tokenize()
        table = string.maketrans("","")

        # Splitting sentence based on new line then Regex pattern[0]
        words = re.split(r'\n',f)
        words = re.split(r''+pattern[0]+'',f)
        
        if punct_remove: words = [z.translate(table, string.punctuation) for z in words]
        
        words = [tok.WordTokenize(z) for z in words]
        return words
