from text_stats import *
import random as rnd
import sys
from os import path

def get_probs(word, all_successors):
    successors = all_successors[word]
    total = sum(successors.values())
    probs = {key:value/total for key,value in successors.items()}
    return(probs)
    
def generate_text(initial, max_word, all_successors):
    text = initial
    while max_word>0 and all_successors[initial]:
        probs = get_probs(initial, all_successors)
        p = rnd.random()
        cumsum = 0
        for k, v in probs.items():
            cumsum += v
            if cumsum>p:
                text = text + " " + k
                initial = k
                break
        max_word-=1
    return text

def print_file(out_fname, text):
    org_stdout = sys.stdout
    sys.stdout = open("./" + out_fname, "w")
    print(text)
    sys.stdout = org_stdout

                

def run_terminal():
    output = None
    if (len(sys.argv)==1):
        print("No arguments were given")
        sys.exit()
    if(len(sys.argv)>5):
        print("No more than three rguments should be given")
        sys.exit()
    if(not path.isfile(sys.argv[1])):
        print("The file does not exist!.")
        sys.exit()
    if(len(sys.argv)==5):
        output = sys.argv[4]  
    filename = sys.argv[1]
    init_word = sys.argv[2]
    max_word = int(sys.argv[3])
    
    with  open(filename, 'r', encoding='utf-8' ) as file:
        text = file.read()
        
        #use the function to take all the words
        all_wrds = all_words(text)
        
        #Cound the all the words of the text
        count_word = Counter(all_wrds)
        
        #all the successors for the text
        all_successors = all_success(all_wrds)
        
        rand_text = generate_text(init_word, max_word, all_successors)
        print(rand_text)

        if output:
            print_file(output, rand_text)

if __name__ == '__main__':
    run_terminal()
    