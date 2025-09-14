'''
CMSI 2120 - Homework 1
Author: Andrew Winter

Original Java assignment written by Andrew Forney @forns,
converted to Python by Natalie Lau @nklau.
'''

def has_sequence(corpus: str, query: str) -> bool:
    # Empty query returns true regardless of what's in the corpus (even if the corpus is empty too)
    if query == "":
        return True
    
    query_i: int = 0 # Query index initialized at 0 
    query_length: int = len(query)

    # Iterate through every letter in corpus
    for i in corpus:
        # If current character in corpus matches current query character, move to next character
        if i == query[query_i]:
            query_i += 1
        # Return true when all query characters found in sequence
        if query_i == query_length:
            return True
    
    # Return false if loop finishes without finding all query characters in sequence
    return False

def capitalize_sentence(sentences: str) -> str:
    # Split sentences by '.'
    sentences_split: list[str] = sentences.split('.')
    # Initialize list as empty to keep track of sentences to be capitalized
    capitalized_sentences: list = []
    # Iterate through each split sentence
    for sentence in sentences_split:
        # Strip leading/tailing spaces from each sentence segment 
        stripped_sentence: str = sentence.strip()
        # Capitalize first letter if sentence segment is not empty
        if stripped_sentence: 
            capitalized_sentences.append(stripped_sentence[0].upper() + stripped_sentence[1:])
        else:
            capitalized_sentences.append('')
    # Join sentences with '. '
    joined_sentence: str = '. '.join(capitalized_sentences).strip()
    # Return joined sentence with period if original sentence ended with period 
    if sentences.endswith('.') and not joined_sentence.endswith('.'):
        joined_sentence += '.'

    return joined_sentence

def get_nth_match(sentence: str, query: str, n: int) -> str:
    # Input validation: raise ValueError if query is empty or if n is negative
    if query == '' or n < 0: 
        raise ValueError('Query string cannot be empty nor can n be a negative integer')
    # Convert sentence and query to lowercase for case sensitivity
    sentence_lower: str = sentence.lower()
    query_lower: str = query.lower()
    # Split sentence into words
    words: list[str] = sentence.split()
    count: int = 0
    # Iterate through words to find the nth match
    for word in words:
        if word.lower() == query_lower:
            if count == n:
                return word
            count += 1
    # If nth match is not found, return empty str
    return ''