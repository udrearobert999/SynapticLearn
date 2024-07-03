import spacy

from queries_config import USER_QUERY

nlp = spacy.load("en_core_web_sm")


def sentence_chunk_text(text):
    document = nlp(text)
    sentences = [sent.text for sent in document.sents]

    return sentences


def chunk_text(llm, text, max_tokens_per_chunk=512, padding=0):
    document = nlp(text)
    sentences = [sent.text for sent in document.sents]

    chunks = []
    current_chunk = []
    current_count = 0

    for sentence in sentences:
        # Use llm's tokenize method
        sentence_tokens = llm.tokenize(sentence)

        sentence_count = len(sentence_tokens)

        if sentence_count > max_tokens_per_chunk - padding:
            continue

        if current_count + sentence_count > max_tokens_per_chunk - padding:
            if current_chunk:
                # Use llm's detokenize method or equivalent
                chunk_text = llm.detokenize(current_chunk)
                chunks.append(chunk_text)
                current_chunk = []
                current_count = 0

        current_chunk.extend(sentence_tokens)
        current_count += sentence_count

    if current_chunk:
        # Use llm's detokenize method or equivalent
        chunk_text = llm.detokenize(current_chunk)
        chunks.append(chunk_text)

    return chunks


def generate_dialog_from_chunks(chunks, modify_user_message=lambda message: message):
    if not chunks:
        return None

    dialog = []
    for chunk in chunks:  # Dialogs must have alternating system and user messages
        # Apply the modification using the lambda function
        user_message = modify_user_message(USER_QUERY + chunk)
        dialog.append(user_message)

    return dialog


def generate_dialogs(llm, articles, chunking_method, max_tokens=512):
    dialogs = []

    # Use llm's tokenize method
    queries_padding = len(llm.tokenize(USER_QUERY))
    additional_safety_padding = 10  # determined experimentally
    for article in articles:
        chunks = []
        if chunking_method == "sentence":
            chunks = sentence_chunk_text(article)
        elif chunking_method == "paragraphs":
            chunks = chunk_text(
                llm=llm,
                text=article,
                max_tokens_per_chunk=max_tokens,
                padding=queries_padding + additional_safety_padding,
            )

        dialog = generate_dialog_from_chunks(chunks)
        if dialog:
            dialogs.append(dialog)

    return dialogs


def rebuild_articles_from_responses(responses, chunks_per_dialog):
    rebuilt_articles = []
    response_index = 0

    for chunk_count in chunks_per_dialog:
        current_article = ""

        for _ in range(chunk_count):
            current_article += responses[response_index]["generation"]["content"] + " "
            response_index += 1

        rebuilt_articles.append(current_article.strip())

    return rebuilt_articles
