import spacy
from pandas import DataFrame
from typing import List, Tuple, Dict

def find_initial_nouns(doc: spacy.tokens.doc.Doc, trigger_words: DataFrame) -> List[Tuple[spacy.tokens.token.Token, int]]:
    """
    Identifies and returns words in the given spaCy Doc that match the trigger words
    in the DataFrame and are either NOUN or PROPN (proper noun).

    Parameters:
    doc (spacy.tokens.doc.Doc): The spaCy Doc object containing the text to be analyzed.
    trigger_words (DataFrame): A pandas DataFrame containing columns 'maschile_singolare' 
                               and 'maschile_plurale' with words to be matched.

    Returns:
    List[Tuple[spacy.tokens.token.Token, int]]: A list of tuples, each containing a matching 
                                                word and its index in the doc.
    """
    result = []  # Initialize an empty list to store results
    index = 0  # Initialize an index to track the position of each word in the doc

    # Convert trigger words to lowercase lists for comparison
    singular_triggers = trigger_words['maschile_singolare'].str.lower().tolist()
    plural_triggers = trigger_words['maschile_plurale'].str.lower().tolist()

    # Iterate over each word in the doc
    for word in doc:
        # Check if the word (in lowercase) is in either the singular or plural trigger words
        if str(word).lower() in singular_triggers or str(word).lower() in plural_triggers:
            # Check if the word is a noun (NOUN) or a proper noun (PROPN)
            if word.pos_ == "NOUN" or word.pos_ == "PROPN":
                result.append((word, index))  # Add the word and its index to the result list
        index += 1  # Increment the index for the next word

    return result  # Return the list of matching words and their indices


def identify_nouns_to_modify(word_list: List[Tuple[spacy.tokens.token.Token, int]], trigger_words: DataFrame) -> List[Tuple[spacy.tokens.token.Token, int]]:
    """
    Determines if words need to be gendered and provides information about their gender. 

    Parameters:
    word_list (List[Tuple[spacy.tokens.token.Token, int]]): A list of tuples, each containing a word 
                                                           (spaCy Token) and its index in the document.
    trigger_words (DataFrame): A pandas DataFrame containing columns 'maschile_singolare', 'maschile_plurale', 
                               'femminile_singolare', and 'femminile_plurale' with words to be matched.

    Returns:
    List[Tuple[spacy.tokens.token.Token, int]]: A list of words that need to be made gender-inclusive.
    """
    result = []  # List to store words that have both masculine and feminine forms
    to_modify = list(word_list).copy()  # Copy of word_list to keep track of words to be modified

    for word in word_list:
        # Check conjunctions and the presence of both masculine and feminine forms
        for child in word[0].children:
            if child.dep_ == 'conj':
                if child.pos_ == "NOUN" and child.morph.get("Gender") and child.morph.get("Gender")[0] == "Fem" and \
                        child.morph.get("Number") and child.morph.get("Number")[0] == "Sing":
                    if str(word[0]).lower() in trigger_words['maschile_singolare'].str.lower().tolist():
                        index = trigger_words[trigger_words['maschile_singolare'].str.lower() == str(word[0]).lower()].index[0]
                        if trigger_words['femminile_singolare'][index].lower() == str(child):
                            result.append((word, f'Per la parola \x1B[3m{word[0]}\x1B[0m sono presenti sia la forma maschile sia la forma femminile'))
                if child.pos_ == "NOUN" and child.morph.get("Gender") and child.morph.get("Gender")[0] == "Fem" and \
                        child.morph.get("Number") and child.morph.get("Number")[0] == "Plur":
                    if str(word[0]).lower() in trigger_words['maschile_plurale'].str.lower().tolist():
                        index = trigger_words[trigger_words['maschile_plurale'].str.lower() == str(word[0]).lower()].index[0]
                        if trigger_words['femminile_plurale'][index].lower() == str(child):
                            result.append((word, f'Per la parola \x1B[3m{word[0]}\x1B[0m sono presenti sia la forma maschile sia la forma femminile'))

        # Check conjunctions and the presence of both feminine and masculine forms
        if word[0].dep_ == 'conj':
            head = word[0].head
            if head.pos_ == "NOUN" and head.morph.get("Gender") and head.morph.get("Gender")[0] == "Fem" and \
                    head.morph.get("Number") and head.morph.get("Number")[0] == "Sing":
                if str(word[0]).lower() in trigger_words['maschile_singolare'].str.lower().tolist():
                    index = trigger_words[trigger_words['maschile_singolare'].str.lower() == str(word[0]).lower()].index[0]
                    if trigger_words['femminile_singolare'][index].lower() == str(head):
                        result.append((word, f'Per la parola \x1B[3m{word[0]}\x1B[0m sono presenti sia la forma maschile sia la forma femminile'))
            if head.pos_ == "NOUN" and head.morph.get("Gender") and head.morph.get("Gender")[0] == "Fem" and \
                    head.morph.get("Number") and head.morph.get("Number")[0] == "Plur":
                if str(word[0]).lower() in trigger_words['maschile_plurale'].str.lower().tolist():
                    index = trigger_words[trigger_words['maschile_plurale'].str.lower() == str(word[0]).lower()].index[0]
                    if trigger_words['femminile_plurale'][index].lower() == str(head):
                        result.append((word, f'Per la parola \x1B[3m{word[0]}\x1B[0m sono presenti sia la forma maschile sia la forma femminile'))

        # Check for feminine and masculine forms with a comma
        for child in word[0].head.children:
            if child.pos_ == "NOUN" and child.morph.get("Gender") and child.morph.get("Gender")[0] == "Fem" and \
                    child.morph.get("Number") and child.morph.get("Number")[0] == "Sing":
                if str(word[0]).lower() in trigger_words['maschile_singolare'].str.lower().tolist():
                    index = trigger_words[trigger_words['maschile_singolare'].str.lower() == str(word[0]).lower()].index[0]
                    if trigger_words['femminile_singolare'][index].lower() == str(child):
                        result.append((word, f'Per la parola \x1B[3m{word[0]}\x1B[0m sono presenti sia la forma maschile sia la forma femminile'))
            if child.pos_ == "NOUN" and child.morph.get("Gender") and child.morph.get("Gender")[0] == "Fem" and \
                    child.morph.get("Number") and child.morph.get("Number")[0] == "Plur":
                if str(word[0]).lower() in trigger_words['maschile_plurale'].str.lower().tolist():
                    index = trigger_words[trigger_words['maschile_plurale'].str.lower() == str(word[0]).lower()].index[0]
                    if trigger_words['femminile_plurale'][index].lower() == str(child):
                        result.append((word, f'Per la parola \x1B[3m{word[0]}\x1B[0m sono presenti sia la forma maschile sia la forma femminile'))

    # Remove words from to_modify that are already in result
    for el in result:
        if el[0] in to_modify:
            to_modify.remove(el[0])

    # Print results
    for el in result:
        print(el[1])

    # Print words that need to be made gender-inclusive
    if not to_modify:
        print('There are no nouns to be made gender inclusive')
    else:
        print('The nouns to be made gender inclusive are:')
        for word in to_modify:
            print(word[0])

    return to_modify


def modify_sentence_based_on_rules(doc: spacy.tokens.doc.Doc, nouns_to_modify: List[Tuple[spacy.tokens.token.Token, int]], trigger_words: DataFrame, articles: Dict, adjectives: Dict):
    """
    Modifies specific words in a sentence based on given trigger words and rules.

    Parameters:
    doc (spacy.tokens.doc.Doc): The input sentence as a spaCy Doc object.
    words_to_modify (list): A list of tuples containing words and their indices in the sentence.
    trigger_words (dict): A dictionary containing trigger words categorized by masculine and feminine forms.
    articoli (dict): A dictionary mapping masculine articles to their corresponding feminine articles.
    agg (dict): A dictionary mapping masculine adjectives to their corresponding feminine adjectives.

    Returns:
    str: The modified sentence.
    """
    # Convert dictionary keys and values to lists
    articoli_key = list(articles.keys())
    articoli_val = list(articles.values())
    agg_key = list(adjectives.keys())
    agg_val = list(adjectives.values())
    result = []

    for element in nouns_to_modify:
        word = str(element[0]).lower()
        idx = element[1]
        word_mod = ''

        if idx == 0:  # No article at this position
            if word in trigger_words['maschile_singolare'].str.lower().tolist():
                i = trigger_words[trigger_words['maschile_singolare'].str.lower() == word].index[0]
                fem = trigger_words['femminile_singolare'][i].lower()
                if word != fem:
                    word_mod = fem + '/' + word
                    result.append((word, word_mod))
                else:
                    result.append((word, word))

            if word in trigger_words['maschile_plurale'].str.lower().tolist():
                i = trigger_words[trigger_words['maschile_plurale'].str.lower() == word].index[0]
                fem = trigger_words['femminile_plurale'][i].lower()
                if word != fem:
                    word_mod = fem + '/' + word
                    result.append((word, word_mod))
                else:
                    result.append((word, word))

        elif idx == 1:  # Article is present at this position
            if (
                (doc[idx - 1].pos_ == 'DET' and doc[idx - 1].tag_ in ['RD', 'RI']) or
                (doc[idx - 1].pos_ == 'ADP' and doc[idx - 1].tag_ == 'E_RD')
            ):
                # Check if the article is in the 'articoli' dictionary
                if str(doc[idx - 1]).lower() in articoli_key:
                    i_art_masc = articoli_key.index(str(doc[idx - 1]).lower())
                    art_fem = articoli_val[i_art_masc]

                    if word in trigger_words['maschile_singolare'].str.lower().tolist():
                        i = trigger_words[trigger_words['maschile_singolare'].str.lower() == word].index[0]
                        fem = trigger_words['femminile_singolare'][i].lower()
                        if word != fem:
                            word_mod = art_fem + ' ' + fem + '/' + str(doc[idx - 1:idx + 1])
                            result.append((str(doc[idx - 1:idx + 1]), word_mod))
                        else:
                            word_mod = art_fem + '/' + str(doc[idx - 1:idx + 1])
                            result.append((str(doc[idx - 1:idx + 1]), word_mod))

                    if word in trigger_words['maschile_plurale'].str.lower().tolist():
                        i = trigger_words[trigger_words['maschile_plurale'].str.lower() == word].index[0]
                        fem = trigger_words['femminile_plurale'][i].lower()
                        if word != fem:
                            word_mod = art_fem + ' ' + fem + '/' + str(doc[idx - 1:idx + 1])
                            result.append((str(doc[idx - 1:idx + 1]), word_mod))
                        else:
                            word_mod = art_fem + '/' + str(doc[idx - 1:idx + 1])
                            result.append((str(doc[idx - 1:idx + 1]), word_mod))
            else:
                # If the article is not in the dictionary or the previous conditions are not satisfied,
                # modify the word using only femminile/nome maschile
                if word in trigger_words['maschile_singolare'].str.lower().tolist():
                    i = trigger_words[trigger_words['maschile_singolare'].str.lower() == word].index[0]
                    fem = trigger_words['femminile_singolare'][i].lower()
                    if word != fem:
                        word_mod = fem + '/' + word
                        result.append((word, word_mod))
                    else:
                        result.append((word, word))

                if word in trigger_words['maschile_plurale'].str.lower().tolist():
                    i = trigger_words[trigger_words['maschile_plurale'].str.lower() == word].index[0]
                    fem = trigger_words['femminile_plurale'][i].lower()
                    if word != fem:
                        word_mod = fem + '/' + word
                        result.append((word, word_mod))
                    else:
                        result.append((word, word))

        elif idx > 1:
        # If a possessive adjective follows the article
            if (
                (doc[idx - 2].pos_ == 'DET' and doc[idx - 2].tag_ in ['RD', 'RI']) or
                (doc[idx - 2].pos_ == 'ADP' and doc[idx - 2].tag_ == 'E_RD')
                ) and (doc[idx - 1].pos_ == 'DET' and doc[idx - 1].tag_ == 'AP'):
                if str(doc[idx - 2]).lower() in articoli_key and str(doc[idx - 1]).lower() in agg_key:
                    i_art_masc = articoli_key.index(str(doc[idx - 2]).lower())
                    art_fem = articoli_val[i_art_masc]
                    i_agg_masc = agg_key.index(str(doc[idx - 1]).lower())
                    agg_fem = agg_val[i_agg_masc]
                    if word in trigger_words['maschile_singolare'].str.lower().tolist():
                        i = trigger_words[trigger_words['maschile_singolare'].str.lower() == word].index[0]
                        fem = trigger_words['femminile_singolare'][i].lower()
                        if word != fem:
                            word_mod = art_fem + ' ' + agg_fem + ' ' + fem + '/' + str(doc[idx - 2:idx + 1])
                            result.append((str(doc[idx - 2:idx + 1]), word_mod))
                        else:
                            word_mod = art_fem + ' ' + agg_fem + '/' + str(doc[idx - 2:idx + 1])
                            result.append((str(doc[idx - 2:idx + 1]), word_mod))
                    if word in trigger_words['maschile_plurale'].str.lower().tolist():
                        i = trigger_words[trigger_words['maschile_plurale'].str.lower() == word].index[0]
                        fem = trigger_words['femminile_plurale'][i].lower()
                        if word != fem:
                            word_mod = art_fem + ' ' + agg_fem + ' ' + fem + '/' + str(doc[idx - 2:idx + 1])
                            result.append((str(doc[idx - 2:idx + 1]), word_mod))
                        else:
                            word_mod = art_fem + ' ' + agg_fem + '/' + str(doc[idx - 2:idx + 1])
                            result.append((str(doc[idx - 2:idx + 1]), word_mod))

            # For example, "di suo" -> modify only the possessive adjective
            elif (doc[idx - 2].pos_ == 'ADP' and doc[idx - 2].tag_ == 'E') and (doc[idx - 1].pos_ == 'DET' and doc[idx - 1].tag_ == 'AP'):
                if str(doc[idx - 1]).lower() in agg_key:
                  i_agg_masc = agg_key.index(str(doc[idx - 1]).lower())
                  agg_fem = agg_val[i_agg_masc]
                  if word in trigger_words['maschile_singolare'].str.lower().tolist():
                    i = trigger_words[trigger_words['maschile_singolare'].str.lower() == word].index[0]
                    fem = trigger_words['femminile_singolare'][i].lower()
                    if word != fem:
                        word_mod = agg_fem + ' ' + fem + '/' + str(doc[idx - 1:idx + 1])
                        result.append((str(doc[idx - 1:idx + 1]), word_mod))
                    else:
                        word_mod = agg_fem + '/' + str(doc[idx - 1:idx + 1])
                        result.append((str(doc[idx - 1:idx + 1]), word_mod))
                  if word in trigger_words['maschile_plurale'].str.lower().tolist():
                    i = trigger_words[trigger_words['maschile_plurale'].str.lower() == word].index[0]
                    fem = trigger_words['femminile_plurale'][i].lower()
                    if word != fem:
                        word_mod = agg_fem + ' ' + fem + '/' + str(doc[idx - 1:idx + 1])
                        result.append((str(doc[idx - 1:idx + 1]), word_mod))
                    else:
                        word_mod = agg_fem + '/' + str(doc[idx - 1:idx + 1])
                        result.append((str(doc[idx - 1:idx + 1]), word_mod))

            # If the index is greater than 1 but only an article + noun is present
            elif (doc[idx - 1].pos_ == 'DET' and doc[idx - 1].tag_ in ['RD', 'RI']) or (doc[idx - 1].pos_ == 'ADP' and doc[idx - 1].tag_ == 'E_RD'):
                if str(doc[idx - 1]).lower() in articoli_key:
                    i_art_masc = articoli_key.index(str(doc[idx - 1]).lower())
                    art_fem = articoli_val[i_art_masc]
                    if word in trigger_words['maschile_singolare'].str.lower().tolist():
                        i = trigger_words[trigger_words['maschile_singolare'].str.lower() == word].index[0]
                        fem = trigger_words['femminile_singolare'][i].lower()
                        if word != fem:
                            word_mod = art_fem + ' ' + fem + '/' + str(doc[idx - 1:idx + 1])
                            result.append((str(doc[idx - 1:idx + 1]), word_mod))
                        else:
                            word_mod = art_fem + '/' + str(doc[idx - 1:idx + 1])
                            result.append((str(doc[idx - 1:idx + 1]), word_mod))
                    if word in trigger_words['maschile_plurale'].str.lower().tolist():
                        i = trigger_words[trigger_words['maschile_plurale'].str.lower() == word].index[0]
                        fem = trigger_words['femminile_plurale'][i].lower()
                        if word != fem:
                            word_mod = art_fem + ' ' + fem + '/' + str(doc[idx - 1:idx + 1])
                            result.append((str(doc[idx - 1:idx + 1]), word_mod))
                        else:
                            word_mod = art_fem + '/' + str(doc[idx - 1:idx + 1])
                            result.append((str(doc[idx - 1:idx + 1]), word_mod))

            else:
            # Modify using only feminine/masculine noun
                if word in trigger_words['maschile_singolare'].str.lower().tolist():
                    i = trigger_words[trigger_words['maschile_singolare'].str.lower() == word].index[0]
                    fem = trigger_words['femminile_singolare'][i].lower()
                    if word != fem:
                        word_mod = fem + '/' + word
                        result.append((word, word_mod))
                    else:
                        result.append((word, word))
                if word in trigger_words['maschile_plurale'].str.lower().tolist():
                    i = trigger_words[trigger_words['maschile_plurale'].str.lower() == word].index[0]
                    fem = trigger_words['femminile_plurale'][i].lower()
                    if word != fem:
                        word_mod = fem + '/' + word
                        result.append((word, word_mod))
                    else:
                        result.append((word, word))

    sentence = str(doc).lower()

    for el in result:
        if el[1] not in sentence:
          sentence = sentence.replace(el[0].lower(), el[1].lower())

    print('Suggestion:')
    print(sentence)
    return sentence

