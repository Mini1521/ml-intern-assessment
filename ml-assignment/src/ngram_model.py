import random
import re
from collections import defaultdict, Counter

class TrigramModel:
    def __init__(self):
        """
        Initializes the TrigramModel.
        """
        #stores trigram counts as a dictionary where keys are tuples and  values are counters of possible next words.
        self.trigram_counts = defaultdict(Counter)
        self.vocabulary = set()                             #set to store all unique words seen during training 
    
    def fit(self, text):
        """
        Trains the trigram model on the given text.

        Args:
            text (str): The text to train the model on.
        """

        text = text.lower()                                 #convert text to lowercase
        text = re.sub(r"[^a-z0-9\s\.\?\!]", " ", text)      #remove unwanted characters, keep letter, numbers and punctuation
        text = re.sub(r"\s+", " ", text).strip()            #replace multiple spaces with single space
        text= re.sub(r"([.?!])", r"\1", text)               #seperate punctuatuon from words    
        tokens = text.split()                               #split text into tokens

        padded= []                                          #stores final padded tokens 
        sentences = []                                      #temp. list for building sentences

        for t in tokens:
            if t in [".", "?", "!"]:
                if sentences:
                    padded.extend(["<s>", "<s>"])           #sentence start token added
                    padded.extend(sentences)                
                    padded.append("</s>")
                sentences = []                              #sentence reset
            else:
                sentences.append(t)                         #token added to current sentence
        
        if sentences:                                       #last sentence if it does not end with punctuation 
            padded.extend(["<s>", "<s>"]) 
            padded.extend(sentences)
            padded.append("</s>")
        
        self.vocabulary.update(padded)                      #vocabulary updated with all words in padded list

        for i in range(len(padded) - 2):
            w1, w2, w3 = padded[i], padded[i+1], padded[i+2]
            self.trigram_counts[(w1, w2)][w3] += 1          #increment count for trigram 


    def generate(self, max_length=50):
        """
        Generates new text using the trained trigram model.

        Args:
            max_length (int): The maximum length of the generated text.

        Returns:
            str: The generated text.
        """

        if not self.vocabulary:                                 #if model is empty return empty string
            return ""
        
        w1, w2= "<s>", "<s>"                                    #start with two sentence start tokens
        result=[]

        for _ in range(max_length):
            options= self.trigram_counts.get((w1, w2), None)    #if no option found, randomly chose a word from vocabulary
            if not options:
                w3 = random.choice(list(self.vocabulary))       
            else:
                words = list(options.keys())                    #sample next word based on trigram probabilities
                counts = list(options.values())
                w3 = random.choices(words, weights=counts, k=1)[0]
            if w3 == "</s>":                                    #break if end of sentence token is generated
                break
            result.append(w3)                                   #word result appended
            w1, w2 = w2, w3                                             
        return " ".join(result)                                 #generated text returned as a single string