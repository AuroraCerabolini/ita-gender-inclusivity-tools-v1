import spacy

nlp = spacy.load("it_core_news_lg") #first you need to install "it_core_news_lg" with the following command: python3 -m spacy download it_core_news_lg

def spacify(text: str) -> spacy.tokens.doc.Doc:
    """
    Process the given text using the spaCy model and return the processed Doc object.

    Parameters:
    text (str): The text to be processed.

    Returns:
    spacy.tokens.doc.Doc: The processed Doc object containing linguistic annotations.
    """
    return nlp(text)

