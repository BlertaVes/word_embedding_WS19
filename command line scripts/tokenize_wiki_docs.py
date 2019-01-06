"""
@author: Blerta Veseli
@contact: blerta.veseli@stud-mail.uni-wuerzburg.de
"""

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import collections
import glob
from nltk import FreqDist
from collections import Counter
import pickle
import pandas as pd
import optparse
from bs4 import BeautifulSoup
import os
import argparse
#import errno

help_text = """
python tokenize_wiki_docs.py [wiki_docs_dir] [stopwords]

tokenize_wiki_docs.py takes the directory to the folders of wiki documents, that are created by the 
WikiExtractor (https://github.com/attardi/wikiextractor), as input and produces tokenized wiki documents
as well as a frequency distribution of all words in the wiki documents. The output data is saved in folder pickle_output.
"""



parser = argparse.ArgumentParser(help_text)
parser.add_argument("wiki_docs_dir", help="file directory to WikiExtractor output", type=str)
parser.add_argument("stopwords", help="stopwords file needs to be txt file", type=str)



args = parser.parse_args()


if (args.wiki_docs_dir is not None) and (args.stopwords is not None): 

    custom_stops = open(args.stopwords, "r", encoding="utf-8").read().splitlines()

    stopset = set(custom_stops)
    
    counter = Counter()

    for path in glob.glob(args.wiki_docs_dir+"\*"):
        print(path)
        
        all_docs = []
        
        for wiki in glob.glob(path+"\*"):
            print(wiki)
        
    
            soup = BeautifulSoup(open(wiki, encoding="utf-8"), "html.parser")   


            for doc_tag in soup.find_all("doc"):

                doc = doc_tag.text

                words = word_tokenize(doc)

                words=[word.lower() for word in words if word.isalpha()]

                filtered_words = [word for word in words if word not in stopset]


                all_docs.append(filtered_words)


        filename="pickle_output\\tokenized_docs\\"+"tokenized_documents_"+os.path.basename(path)+".p"
        os.makedirs(os.path.dirname(filename),exist_ok=True)
        with open(filename, 'wb') as handle:
            pickle.dump(all_docs, handle)
        
    
        flat_list = [item for sublist in all_docs for item in sublist]

    
        frequency_distribution = Counter(FreqDist(flat_list))
            
        counter = counter + frequency_distribution

    filename_freq= "pickle_output\\"+"frequency_dist_counter.p"
    os.makedirs(os.path.dirname(filename_freq), exist_ok=True)
    with open(filename_freq, 'wb') as handle:
        pickle.dump(counter, handle)

        
        
else: 
    print("Two positional arguments needed for running this code: wiki docs dir and stopwords")
    