import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

import random
import numpy as np
import torch

nltk.download("punkt")
nltk.download("wordnet")
nltk.download("stopwords")


def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def process_text(text):

    text = text.lower()

    table = str.maketrans("", "", string.punctuation)
    text = text.translate(table)

    words = nltk.word_tokenize(text)

    stop_words = set(stopwords.words("english"))
    words = [word for word in words if word not in stop_words]

    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()

    words_stemmed_lemmatized = [
        lemmatizer.lemmatize(stemmer.stem(word)) for word in words
    ]

    processed_text = " ".join(words_stemmed_lemmatized)

    return processed_text
