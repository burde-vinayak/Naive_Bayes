import os,sys
import pickle
from math import log10

class nblearn():
    spam_words = {}
    ham_words = {}
    totalspamfiles = 0
    totalhamfiles = 0
    vocabulary=set([])
    ham_words_probabi= {}
    spam_words_probabi= {}
    ham_probab=0
    spam_probab=0
    def tokenize(self,word):
        return word
    def get_details(self,path):

        for dirName, subdirList, fileList in os.walk(path, topdown=True):
            #print('Found directory: %s' % dirName)

            for fname in fileList:
                if "spam" in dirName:
                    #print('\t%s' % fname)
                    self.totalspamfiles = self.totalspamfiles + 1
                    fopen=open(os.path.join(dirName,fname), "r", encoding="latin1")
                    for line in fopen:
                        for word in line.split():
                            final_word=self.tokenize(word)
                            self.vocabulary.add(final_word)
                            if self.spam_words.get(final_word):
                                self.spam_words[final_word]+=1
                            else:
                                self.spam_words[final_word]=1

                elif "ham" in dirName:
                    self.totalhamfiles = self.totalhamfiles + 1
                    fopen = open(os.path.join(dirName,fname), "r", encoding="latin1")
                    for line in fopen:
                        for word in line.split():
                            final_word = self.tokenize(word)
                            self.vocabulary.add(final_word)
                            if self.ham_words.get(final_word):
                                self.ham_words[final_word] += 1
                            else:
                                self.ham_words[final_word] = 1
        #print(totalspamfiles, totalhamfiles, self.spam_words, self.ham_words)
    def ham_spam_probab(self):
        self.ham_probab=self.totalhamfiles/(self.totalhamfiles+self.totalspamfiles)
        self.spam_probab=self.totalspamfiles/(self.totalhamfiles+self.totalspamfiles)

    def ham_words_probab(self):
        total=sum(self.ham_words.values())+(len(self.vocabulary))
        for word in self.vocabulary:
            if word in self.ham_words.keys():
                self.ham_words_probabi[word]=log10(self.ham_words.get(word)+1)-log10(total)
            else:
                self.ham_words_probabi[word]=log10(1)-log10(total)
    def spam_words_probab(self):
        total=sum(self.spam_words.values())+(len(self.vocabulary))
        for word in self.vocabulary:
            if word in self.spam_words.keys():
                self.spam_words_probabi[word]=log10((self.spam_words.get(word))+1)-log10(total)
            else:
                self.spam_words_probabi[word] = log10(1) - log10(total)
path =sys.argv[1]
obj=nblearn()
obj.get_details(path)
obj.ham_spam_probab()
obj.ham_words_probab()
obj.spam_words_probab()
fopen=open('nbmodel.txt','wb')
#fopen.write(str(obj.totalspamfiles)+'   '+str(obj.totalhamfiles)+'\n'+ str(obj.ham_words_probab) + '\n' + str(obj.spam_words_probab))
data={'ham_probability':obj.ham_probab,
      'spam_probability':obj.spam_probab,
      'ham_words_probability':obj.ham_words_probabi,
      'spam_words_probability':obj.spam_words_probabi,
      'ham_file':obj.totalhamfiles,
      'vocab':obj.vocabulary
      }

pickle.dump(data,fopen)
#print(len(obj.vocabulary))
fopen.close()