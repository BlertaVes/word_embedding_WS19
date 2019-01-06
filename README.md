# Word Embedding WS 19


Exercises for seminar "word embedding" in winter semester 2019 at Julius Maximilians University Würzburg.

### Command line scripts

#### Description

The folder "command line scripts" contains a python script for tokenizing the wiki docs created by WikiExtractor (https://github.com/attardi/wikiextractor/blob/master/WikiExtractor.py) and a python script that creates a co-occurrence matrix, 
a document_frequency_matrix (number of documents that contain a certain co-occurrence), tf-idf matrix (co-occurence matrix with tfidf values).

#### Use

To tokenize the wiki docs use tokenize_wiki_docs.py in cmd:

python tokenize_wiki_docs.py [wiki_docs_dir] [stopwords]

The wiki_docs_dir argument is the directory to the extracted wiki files and the stopwords argument needs to be your stopword list as txt file. The output will be tokenized wiki docs as well as a frequency distribution counter.


to compute the co-occurrence matrix, the tfidf matrix and the document frequency matrix in cmd:

python create_co_occurrence_matrices.py [frequency_dist_counter] [tokenized_docs_dir]

The frequency_dist_counter argument as well as tokenized_docs_dir argument are the output from tokenize_wiki_docs.py and should be used here to compute the matrices. When running this code, the user will be asked for the matrix size and the window size that is needed to compute the co-occurrence matrix. 

### Jupyter Notebooks

The jupyter notebooks contain necessary steps for tokenizing the wiki docs, creating a co-occurrence matrix, converting the co-occurrence matrix to tfidf matrix and computing the cosine similarity between word vectors in the matrix. 

#### Use

To use the jupyter notebooks the directories have to be changed to local ones.
