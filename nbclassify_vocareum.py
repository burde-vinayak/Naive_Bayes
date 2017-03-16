import pickle
import os
from math import log10
import sys
fopen=open('nbmodel.txt','rb')

data=pickle.load(fopen)
#print(data['ham_probability'])
path=sys.argv[1]
file_spam={}
file_ham={}
file_actual={}
file_result={}
#print(len(data['spam_words_probability'].keys()))
#print(len(data['ham_words_probability'].keys()))
for root,dirs,files in os.walk(path):
    for file in files:
        if 'ham' in file:
            file_actual[os.path.join(root,file)]='ham'
        elif 'spam' in file:
            file_actual[os.path.join(root,file)]='spam'
        if file.endswith('.txt'):
            fileobj=open(os.path.join(root,file), "r", encoding="latin1")
            #fileword={}
            file_spam[os.path.join(root,file)]=log10(data['spam_probability'])
            file_ham[os.path.join(root,file)]=log10(data['ham_probability'])
            for line in fileobj:
                for word in line.split():
                    if data['spam_words_probability'].get(word):
                        file_spam[os.path.join(root,file)]=file_spam[os.path.join(root,file)]+(data['spam_words_probability'].get(word))
                    # else:
                    #     probab_word=1/(len(data['vocab'])+len(data['spam_words_probability']))
                    #     file_spam[file]=file_spam[file]*probab_word
                    if data['ham_words_probability'].get(word):
                        file_ham[os.path.join(root,file)]=file_ham[os.path.join(root,file)]+(data['ham_words_probability'].get(word))
                    # else:
                    #     probab_word = 1 / (len(data['vocab']) + len(data['ham_words_probability']))
                    #     file_ham[file] = file_ham[file] * probab_word
            if(file_ham[os.path.join(root,file)]>file_spam[os.path.join(root,file)]):
                file_result[os.path.join(root,file)]='ham'

            elif(file_spam[os.path.join(root,file)]>file_ham[os.path.join(root,file)]):
                file_result[os.path.join(root,file)]='spam'
fopen= open('nboutput.txt','w')
for k,v in file_result.items():
    fopen.write(v+' '+k+'\n')

document_count=len(file_actual)
correctly_classified_ham=0
correctly_classified_spam=0
ham_prediction=0
spam_prediction=0
ham_actual=0
spam_actual=0

for file in file_actual.keys():
    if file_actual[file]=='ham':
        ham_actual+=1
    elif file_actual[file]=='spam':
        spam_actual+=1
    if file_actual[file]==file_result[file]:
        if file_actual[file]=='spam':
            correctly_classified_spam+=1
        elif file_actual[file]=='ham':
            correctly_classified_ham+=1
for file in file_result.keys():
    if file_result[file]=='ham':
        ham_prediction+=1
    elif file_result[file]=='spam':
        spam_prediction+=1
accuracy=(correctly_classified_spam+correctly_classified_ham)/document_count


precision_spam=correctly_classified_spam/spam_prediction
precision_ham=correctly_classified_ham/ham_prediction

recall_spam=correctly_classified_spam/spam_actual
recall_ham=correctly_classified_ham/ham_actual

f1_spam=(2*(precision_spam*recall_spam))/(precision_spam+recall_spam)
f1_ham=(2*recall_ham*precision_ham)/(precision_ham+recall_ham)

print(str(accuracy)+' '+' '+str(precision_ham)+' '+str(precision_spam)+' '+str(recall_ham)+' '+str(recall_spam)+' '+str(f1_ham)+' '+str(f1_spam))




            # else:
            #     file_result[file]='draw'
# count=0
# for k,v in file_actual.items():
#     if file_result[k]==file_actual[k]:
#         count+=1
#
# accuracy=count/len(file_actual)
# print(str(accuracy)+' '+str(count)+' '+str(len(file_actual)))



