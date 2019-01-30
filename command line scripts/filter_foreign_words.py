# -*- coding: utf-8 -*-
"""
@author: Blerta Veseli
@contact: blerta.veseli@stud-mail.uni-wuerzburg.de
"""



import pandas as pd
import regex
import optparse


"""python filter_foreign_words.py

this python script takes a csv with the columns category, description, text and length, that contains wikipedia articles 
and filters non-latin writing systems as well as other foreign words. 
"""

wiki_csv = input("Wikipedia CSV (directory to your csv, \t-seperated): ")
char_list = input("Character list with the letters of your language (comma seperated): ")
punctuations = input("Punctuations list (whitespace seperated): ")

wiki_data = pd.read_csv(wiki_csv, sep="\t")


def filter_foreign_words(tokens_list, char_list):
    
    filtered_tokens_list = []
    
    for i, word in enumerate(tokens_list): 
        foreign = False
        for character in word: 
            if character not in char_list:
                #print("foreign",word,i)
                foreign = True

        if not foreign:
            #print("not foreign", word, i)
            filtered_tokens_list.append(word)
            
    return filtered_tokens_list
    
	

char_list = char_list.split(",")
punctuations = punctuations.split(" ")
char_list = char_list + punctuations
re_pattern = "[\p{Latin}0-9„“.!'?()-,]+"


for index, row in wiki_data.iterrows():
    #print(index)
    
    description = row[1]
    text = row[2]   
    
    #get only latin writing system and filter other
    text_tokens_list = regex.findall(re_pattern, text )
    desc_tokens_list = regex.findall(re_pattern, description )

    #heuristic to remove words that are not german
    filtered_text_tokens = filter_foreign_words(text_tokens_list, char_list)
    filtered_desc_tokens = filter_foreign_words(desc_tokens_list, char_list)
         
    wiki_data.loc[index, "text"] = ' '.join(filtered_text_tokens)
    wiki_data.loc[index, "description"] = ' '.join(filtered_desc_tokens)
    wiki_data.loc[index, "length"] = len(filtered_text_tokens)


        
wiki_data.to_csv("filtered_wiki_data.csv", sep",", index=False)
