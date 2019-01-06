import os
import argparse
import numpy as np
import pandas as pd
import pickle
import glob
#import errno

help_text = """
python create_co_occurrence_matrix.py [frequency_dist_counter][tokenized_docs_dir]

create_co_occurrence_matrix.py takes the pickled files created by tokenize_wiki_docs.py as input
and creates a cooccurrence matrix and a document frequency matrix. The output matrices will be saved in folder matrix.

"""

parser = argparse.ArgumentParser(help_text)
parser.add_argument("frequency_dist_counter", help="file directory to frequency_dist_counter", type=str)
parser.add_argument("tokenized_docs_dir", help="directory to tokenized wiki docs", type=str)

args = parser.parse_args()

input_matrix_size = input("matrix size: ")

input_window_size = input("window size: ")

################################### tf idf Formeln #############################
 
def tfLog(tf): 
    if tf > 0:
        return 1+np.log10(tf)
    else: 
        return 0

def idf(N,df_t):
    if df_t > 0:
        return np.log10(N/df_t)
    else:
        return 0

########################################################################

if (args.frequency_dist_counter is not None) and (args.tokenized_docs_dir is not None):
    
    co_occurence_matrix = np.zeros((int(input_matrix_size)+2,int(input_matrix_size)+2))

    document_frequency_matrix= np.zeros((int(input_matrix_size)+2,int(input_matrix_size)+2))

    padding_wordIDs = [int(input_matrix_size)+1,int(input_matrix_size)+1]

    N = 0
    
    
    with open(args.frequency_dist_counter, 'rb') as handle:
        frequency_dist = pickle.load(handle)
    
    mc = frequency_dist.most_common(int(input_matrix_size))
    mc = [tupel[0] for tupel in mc]
    


    for path in glob.glob(args.tokenized_docs_dir+"\*"):
        print(path)
        
        list_of_wordIDs = []

        with open(path, 'rb') as handle:
            tokenized_docs = pickle.load(handle)

        N += len(tokenized_docs)


        for doc in tokenized_docs:

            l = [mc.index(token) if token in mc else int(input_matrix_size) for token in doc]
            list_of_wordIDs.append(l)
            
        print("list_of_wordsIDs created "+ path)
        
        for doc in list_of_wordIDs: 
        
            tupel_set = set()
            doc = padding_wordIDs + doc + padding_wordIDs

            for i, center_word in enumerate(doc[int(input_window_size):-int(input_window_size) ]):
                i=i+int(input_window_size)

                window = 1
                while window <= int(input_window_size):

                    co_occurence_matrix[doc[i-window], center_word] +=1
                    co_occurence_matrix[doc[i+window], center_word] +=1

                    tupel_set.add((doc[i-window], center_word))
                    tupel_set.add((doc[i+window], center_word))



                    window +=1  

            for tupel in tupel_set:
                document_frequency_matrix[tupel] += 1
    print(N)

    filename_cooc = "matrix\\"+"co_occ_matrix.p"
    os.makedirs(os.path.dirname(filename_cooc), exist_ok=True)
    with open(filename_cooc, 'wb') as handle:
        pickle.dump(co_occurence_matrix, handle)
        
    print("cooccurrence matrix is created")

    filename_doc_freq = "matrix\\"+"document_freq_matrix.p"
    os.makedirs(os.path.dirname(filename_doc_freq), exist_ok=True)
    with open(filename_doc_freq, 'wb') as handle:
        pickle.dump(document_frequency_matrix, handle)
    
    print("document_freq_matrix is created")
    
############## tfidf matrix ##############    

    print("start creating tfidf matrix")
    
    tfidf_matrix = np.zeros((int(input_matrix_size)+2,int(input_matrix_size)+2))

    for i, row in enumerate(co_occurence_matrix):

        for j,column in enumerate(co_occurence_matrix.T):


            #print("Stelle ",i,j, "Kook-Wert ", tfLog(co_occurence_matrix[i,j]), "Zugehöriger df(kook) Wert", document_frequency_matrix[i,j])

            tfidf_matrix[i,j] = tfLog(co_occurence_matrix[i,j]) * idf(N,document_frequency_matrix[i,j])

    filename_tfidf = "matrix\\"+"tfidf_matrix.p"
    os.makedirs(os.path.dirname( filename_tfidf), exist_ok=True)
    with open(filename_tfidf, 'wb') as handle:
        pickle.dump(tfidf_matrix, handle)
    
    print("creating tfidf matrix is finished. Now start convert to pandas df")

    num = int(input_matrix_size)+2
    if len(mc) != num:
        mc.append("another_token")
        mc.append("padding_token")


        
    tfidf_df = pd.DataFrame(tfidf_matrix, index = mc, columns = mc)

    co_occurence_matrix_df = pd.DataFrame(co_occurence_matrix, index = mc, columns =mc)

    document_frequency_matrix_df = pd.DataFrame( document_frequency_matrix, index = mc, columns = mc)

    filename_tfidf_pd = "matrix\\"+"tfidf_matrix_as_pandas_df.p"
    os.makedirs(os.path.dirname(filename_tfidf_pd), exist_ok=True)
    filename_cooc_pd = "matrix\\"+"co_occ_matrix_as_pandas_df.p"
    os.makedirs(os.path.dirname( filename_cooc_pd), exist_ok=True)
    filename_doc_freq_pd = "matrix\\"+"document_freq_matrix_as_pandas_df.p"
    os.makedirs(os.path.dirname(filename_doc_freq_pd), exist_ok=True)

    with open(filename_tfidf_pd, 'wb') as handle:
        pickle.dump(tfidf_df, handle)
    with open(filename_cooc_pd, 'wb') as handle:
        pickle.dump(co_occurence_matrix_df, handle)
    with open(filename_doc_freq_pd, 'wb') as handle:
        pickle.dump(document_frequency_matrix_df, handle)
        
    print("co_occ, doc_freq and tfidf matrices saved as pandas df")


    
else:
    print("Two input positional arguments needed for running this code: the frequency_distribution and the tokenized_wiki_docs")


