
import sys
from os import path
import string 
from collections import Counter
import re


def all_words(str):
    seps = '[' + string.whitespace + string.punctuation + ']+'
    split = re.split(seps, str)
    
    words  = []
    for i in split:
        if not i.isalpha():
            continue
        words.append(i.lower())
        
    return words
    
#function counds letters
def count_letter(text):
    
    #only_strings = ''.join(filter(str.isalpha, text))
    #lower_strings = only_strings.lower()
    count = Counter(text)    
    return(count)

def all_success(str):
    
    # dictionery to store the successors
    successors = {}
    
    for i in range(1,len(str)):
        
        if str[i-1] in successors.keys():
            succs = successors[str[i-1]]
            if str[i] in succs.keys():
                succs[str[i]] +=1
            else:
                succs[str[i]] = 1
        else:
            successors[str[i-1]] = {}
            succs = successors[str[i-1]] 
            if str[i] in succs.keys():
                succs[str[i]] +=1
            else:
                succs[str[i]] = 1

    return (successors)


def most_common_successors(dict,all_success):
    for key,value in dict:
        print(key,value)
        
        all_my_success = all_success[key]
        final_success = sorted(all_my_success,key= all_my_success.get, reverse = True)[:3]
       
        for k in final_success:
            print ("\t", k, all_my_success[k])
            

def print_terminal(all_letters, count_word,all_successors ):
    sorted_keys = sorted(all_letters,key = all_letters.get, reverse = True)
    # cound the unique words
    unique_words = len(count_word.keys())
        
    # use the function and take the 5 most frequent words with their frequence
    most_freq = count_word.most_common(5)
        
    for key in sorted_keys:
        print("{}:{}".format(key,all_letters[key]))
        
        
    print("total words =", sum(count_word.values()))
    print("unique words =", unique_words)
    
    most_common_successors(most_freq,all_successors)

def print_file(out_fname, all_letters, count_word,all_successors):
    org_stdout = sys.stdout
    sys.stdout = open("./" + out_fname, "w")
    print_terminal(all_letters, count_word,all_successors)
    sys.stdout = org_stdout





def run_terminal():
    output = None
    if (len(sys.argv)==1):
        print("No arguments were given")
        sys.exit()
    
    if(len(sys.argv)>3):
        print("No more than two rguments should be given")
        sys.exit()
        
    if(not path.isfile(sys.argv[1])):
         
        print("The file does not exist!.")
        sys.exit()
         
    if(len(sys.argv)==3):
        output = sys.argv[2]  
                
        
    filename = sys.argv[1]
        
        
    #Open the file 
    with  open(filename, 'r', encoding='utf-8' ) as file:
        text = file.read()
        
        #use the function to take all the words
        all_wrds = all_words(text)
    
        all_letters =  Counter("".join(all_wrds)) 
        
        
        
        #Cound the all the words of the text
        count_word = Counter(all_wrds)
            
        
        
        
        #all the successors for the text
        all_successors = all_success(all_wrds)
        # function finding the most frequent successors given some words
        
        print_terminal(all_letters, count_word,all_successors )
        
        if output:
            print_file(output, all_letters, count_word,all_successors)
        

        
    
if __name__ == '__main__':
    run_terminal()




            
        
    
    











