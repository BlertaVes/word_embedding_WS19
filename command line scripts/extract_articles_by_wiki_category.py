"""
Extracts a certain number of articles per category from german Wikipedia.
Articles are skipped if they contain less than 100 words and are shortend to 2000 words if they are longer.
Footnotes, sources etc. are omitted.
Saves a tab-seperated csv-file to disk.

This script takes your chosen wiki categories as input as well as the number of texts per categorie you want to extract.
"""

import wikipediaapi
import pandas as pd
import regex as re

input_categories = input("Wikipedia Categories (comma seperated, without whitespaces): ")
input_num_of_texts = input("How many texts per category: ")
input_categories = input_categories.split(",")
#print("TYPE",input_categories, type(input_categories))


def print_categorymembers(df, l, num_of_texts_per_category, categorymembers, kat, level=0, max_level=2):
	
    wiki_wiki = wikipediaapi.Wikipedia('de')
    p = re.compile(r'^Literatur\n.+|^Weblinks\n.*|^== Einzelnachweise ==\n.*|^Quellen\n.*|^Fußnoten\n.*', flags=re.DOTALL|re.MULTILINE)
   
    for c in categorymembers.values():   
        laenge = len(l)
        if c.ns == 0:
                 
            titel = c.title
            #print(titel)
            p_wiki = wiki_wiki.page(titel)
         
            summary = p_wiki.summary
            fulltext = p_wiki.text
            text = re.sub(p, '', fulltext)
            a = re.compile('\p{Letter}+\p{Connector_Punctuation}?\p{Letter}+|\p{Number}+')
            tokens = re.findall(a, text)
                
            if (text == summary) or (len(tokens)<100):
            
                pass
            elif len(tokens) > 2000:    
                text = ' '.join(tokens[:2000])
                df = df.append({'Kategorie' : kat , 'Titel' : titel, 'Zusammenfassung' : summary, 'Volltext' : text} , ignore_index=True)
          
                l.append(titel)
            else:
                df = df.append({'Kategorie' : kat , 'Titel' : titel, 'Zusammenfassung' : summary, 'Volltext' : text} , ignore_index=True)
            
                l.append(titel)
          
        if len(l) == num_of_texts_per_category:
          
            break           
        elif c.ns == wikipediaapi.Namespace.CATEGORY and level <= max_level and laenge<num_of_texts_per_category:
           
            df = print_categorymembers(df, l, num_of_texts_per_category, c.categorymembers, kat, level + 1)
    return df


def extract(categories, num_of_texts_per_category):
    wiki_wiki = wikipediaapi.Wikipedia('de')
    newdf = pd.DataFrame(columns=['Kategorie','Titel', 'Zusammenfassung', 'Volltext'])
    for kat in categories:
        l = []
        cat = wiki_wiki.page("Kategorie:"+kat)
        newdf = print_categorymembers(newdf, l,  num_of_texts_per_category,  cat.categorymembers, kat= kat)
    return newdf

if __name__ == '__main__':	
	
	
    newdf = extract(input_categories, input_num_of_texts)
    newdf.to_csv('wiki_articles.csv', index=False)