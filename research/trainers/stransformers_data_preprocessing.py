# Data loading
from datasets import Dataset
import pandas as pd

# Data preprocessing
import numpy as np
import string
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

# Utility
from tqdm import tqdm

# Download necessary NLTK data
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("stopwords")

# Load stopwords once to improve efficiency
stop_words = set(stopwords.words("english"))


def remove_punctuation(text):
    """
    Removes punctuation from the given text.

    Args:
    - text (str): The text to process.

    Returns:
    - str: The text without punctuation.
    """
    table = str.maketrans("", "", string.punctuation)
    return text.translate(table)


def stem_and_lemmatize(text):
    """
    Stems and lemmatizes the given text. Removes stopwords.

    Args:
    - text (str): The text to process.

    Returns:
    - str: The processed text.
    """
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(text)
    stemmed_and_lemmatized = [
        lemmatizer.lemmatize(stemmer.stem(word))
        for word in words
        if word not in stop_words
    ]
    return " ".join(stemmed_and_lemmatized)


def chunk_text(text, tokenizer, max_length=510, stride=510):
    """
    Splits a text into overlapping chunks using the specified tokenizer.

    Args:
    - text (str): The text to chunk.
    - tokenizer: The tokenizer instance.
    - max_length (int): The maximum length of each chunk.
    - stride (int): The stride to use for chunking.

    Returns:
    - list: A list of tokenized chunks.
    """
    tokenized_text = tokenizer.tokenize(text)
    chunks = []
    for i in range(0, len(tokenized_text), stride):
        chunk = tokenized_text[i : i + max_length]
        chunks.append(chunk)
    return chunks


def preprocess_text(text, tokenizer, max_length, stride):
    """
    Applies preprocessing steps to the text and then chunks it.

    Args:
    - text (str): The text to preprocess and chunk.
    - tokenizer: The tokenizer instance.
    - max_length (int): The maximum length for each chunk.
    - stride (int): The stride for chunking.

    Returns:
    - list: A list of preprocessed and chunked texts.
    """
    text = text.lower()
    text = remove_punctuation(text)
    # text = stem_and_lemmatize(text)
    text_chunks = chunk_text(text, tokenizer, max_length, stride)

    return text_chunks


def preprocess_dataset(
    dataset, tokenizer, max_length=510, stride=510, shuffle_seed=None
):
    """
    Applies text preprocessing and chunking to the entire dataset, then shuffles it.

    Args:
    - dataset: A dataset with 'text' and 'label' columns.
    - tokenizer: The tokenizer instance.
    - max_length (int): The maximum chunk length.
    - stride (int): The stride for chunking.
    - shuffle_seed (int, optional): Seed for shuffling the dataset.

    Returns:
    - Dataset: A new dataset with preprocessed, chunked, and shuffled texts and their labels.
    """
    processed_texts = []
    labels = []

    # Using tqdm for progress bar
    for text, label in tqdm(
        zip(dataset["text"], dataset["label"]),
        total=len(dataset["text"]),
        desc="Processing",
    ):
        text_chunks = preprocess_text(text, tokenizer, max_length, stride)
        for chunk in text_chunks:
            chunk_str = tokenizer.convert_tokens_to_string(chunk)
            processed_texts.append(chunk_str)
            labels.append(label)

    # Create a DataFrame and shuffle it with a seed
    new_df = (
        pd.DataFrame({"text": processed_texts, "label": labels})
        .sample(frac=1, random_state=shuffle_seed)
        .reset_index(drop=True)
    )

    # Convert the shuffled DataFrame to a Dataset
    new_dataset = Dataset.from_pandas(new_df)

    return new_dataset


def limit_dataset(dataset, max_samples):
    """
    Limits the dataset to a maximum number of samples while ensuring all classes are included.
    """
    samples_per_class = max_samples // len(np.unique(dataset["label"]))
    samples_per_class = max(
        1, samples_per_class
    )  # Ensure at least one sample per class

    return dataset.groupby("label", group_keys=False).apply(
        lambda x: x.sample(min(len(x), samples_per_class))
    )
