import pandas as pd
import html
import matplotlib.pyplot as plt
import re, string, unicodedata
import nltk
import contractions
import inflect
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords, words
from nltk.stem import LancasterStemmer, WordNetLemmatizer
from nltk.util import ngrams
from tqdm import tqdm
import gensim

''' From: https://gist.github.com/MrEliptik/b3f16179aa2f530781ef8ca9a16499af'''

def replace_contractions(text):
    """Replace contractions in string of text"""
    return contractions.fix(text)

def remove_non_ascii(words):
    """Remove non-ASCII characters from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8','ignore')
        new_words.append(new_word)
    return new_words

def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words

def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    new_words = []
    for word in words:
        word = re.sub(r'-',' ',word)
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            # if we replace hyphens with spaces, we should still split, e.g. '2-trillion' -> ['2','trillion']
            new_words += [i for i in new_word.split()]
    return new_words

def replace_numbers(words):
    """Replace all integer occurrences in list of tokenized words with textual representation"""
    p = inflect.engine()
    new_words = []
    for word in words:
        if word.isdigit():
            new_word = p.number_to_words(word)
            new_word = new_word.replace(',','')
            new_word = new_word.replace(' ','-')
            new_words.append(new_word)
        else:
            new_words.append(word)
    return new_words

def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    new_words = []
    for word in words:
        if word not in stopwords.words('english'):
            new_words.append(word)
    return new_words

def stem_words(words):
    """Stem words in list of tokenized words"""
    stemmer = LancasterStemmer()
    stems = []
    for word in words:
        stem = stemmer.stem(word)
        stems.append(stem)
    return stems

def lemmatize_words(words):
    """Lemmatize words in list of tokenized words"""
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    for word in words:
        if word == 'pence':
            # it likes to make "Mike Pence" "Mike Penny" :)
            lemmas.append('pence')
        else:
            lemma = lemmatizer.lemmatize(word, pos='v')
            lemma = lemmatizer.lemmatize(word, pos='n')
            # WordNetLemmatizer converts us -> u
            if lemma not in ['u']:
                lemmas.append(lemma)
    return lemmas


def normalize(words):
    ''' return a normalized sentence '''
    words = nltk.word_tokenize(replace_contractions(words))
    words = remove_non_ascii(words)
    words = to_lowercase(words)
    words = remove_punctuation(words)
    words = replace_numbers(words)
    words = remove_stopwords(words)
    words = lemmatize_words(words)
    return ' '.join(words)
    #return words

if __name__ == '__main__':
   print(normalize('2-trillion-dollar'))
   print(normalize("I can't even"))
   print(normalize('2019'))
