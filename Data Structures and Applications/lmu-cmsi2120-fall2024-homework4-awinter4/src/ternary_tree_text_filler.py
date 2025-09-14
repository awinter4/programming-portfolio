'''
CMSI 2120 - Homework 4
Author: Andrew Winter

Original Java assignment written by Andrew Forney @forns,
converted to Python by Natalie Lau @nklau.
'''

from ternary_tree_node import TTNode
from text_filler import TextFiller
from typing import Optional


class TernaryTreeTextFiller(TextFiller):
    '''
    A ternary-search-tree implementation of a text-autocompletion
    trie, a simplified version of some autocomplete software.
    '''
    
    # Fields
    # -----------------------------------------------------------
    root: Optional[TTNode]
    size: int

    # Constructor
    # -----------------------------------------------------------
    def __init__(self) -> None:
        self.root = None
        self.size = 0

    # Methods
    # -----------------------------------------------------------
    def __len__(self) -> int:
        """
        Returns the number of stored terms inside of the TextFiller -- synonymous 
        with asking for the number of wordEnds at TTNodes.
        """
        return self.size
    
    def is_empty(self) -> bool:
        """
        Returns True if the TextFiller has no search terms stored, False otherwise.
        """
        return self.size == 0
    
    def add(self, word: str, priority: int = -1) -> None:
        """
        Adds the given search term to the TextFiller. If the term already exists, it does nothing.
        Traverses or creates nodes for each character, marking the final node as a "word end" and updating 
        its priority if higher. The tree size increases only for new unique words.

        param:
        - word: The term to add. Must be non-empty and is normalized.
        - priority: Optional importance of the term, extra credit.
        """
        word = self.normalize_term(word)
        if len(word) == 0:
            raise ValueError("Cannot add an empty string to the TernaryTreeTextFiller.")
        
        def recursive_add(node: Optional[TTNode], index: int) -> TTNode:
            letter = word[index]
            if node is None:
                node = TTNode(letter)

            if letter < node.letter:
                node.left = recursive_add(node.left, index)
            elif letter > node.letter:
                node.right = recursive_add(node.right, index)
            else: 
                if index + 1 < len(word):
                    node.middle = recursive_add(node.middle, index + 1)
                else: 
                    if not node.word_end:
                        self.size += 1
                    node.word_end = True
                    node.word_end_priority = max(node.word_end_priority, priority)

            return node

        self.root = recursive_add(self.root, 0)

    def contains(self, query: str) -> bool:
        """
        Returns True if the given query String exists within the TextFiller, False otherwise.
        
        param: 
        - query: The term to check for in the TextFiller.
        """
        query = self.normalize_term(query)
        node = self._find_prefix_node(query)
        return node is not None and node.word_end

    def text_fill(self, query: str) -> Optional[str]:
        """
        Returns any search term contained in the TextFiller that possesses the query as a prefix 
        (e.g., "it" is a prefix of both "it" [exact match] and "item" [first two letters]). If the given query
        is a prefix for NO search term, returns None.
        
        param:
        - query: The term to check for in the TextFiller.
        """
        query = self.normalize_term(query)
        if len(query) == 0:
            return None
        
        prefix_node = self._find_prefix_node(query)
        if prefix_node is None:
            return None
        
        if prefix_node.word_end:
            return query
        
        words = self._collect_all_words(prefix_node.middle, query)
        return words[0] if words else None
    
    def get_sorted_list(self) -> list[str]:
        """
        Returns a List of Strings consisting of the alphabetically sorted search terms within this TextFiller.
        """
        if self.is_empty():
            return []
        return self._collect_all_words(self.root, "")

    # Helper Methods
    # -----------------------------------------------------------
    def normalize_term(self, string: str) -> str:
        '''
        Normalizes a term to either add or search for in the tree,
        since we do not want to allow the addition empty strings.
        Removes empty spaces at the beginning or end of the string
        (spaces in the middle are fine, as they allow our tree to
        also store multi-word phrases).

        :param string: The string to sanitize
        :returns: The sanitized version of string
        '''
        # Edge case handling: empty strings illegal
        if len(string) == 0:
            raise ValueError
        return string.strip().lower()
    
    def _find_prefix_node(self, prefix: str) -> Optional[TTNode]:
        """
        Finds the node corresponding to the last character of the given prefix.
        
        param:
        - prefix: The prefix to search for.
        """
        current_node = self.root
        index = 0

        while current_node is not None:
            letter = prefix[index]
            if letter < current_node.letter:
                current_node = current_node.left
            elif letter > current_node.letter:
                current_node = current_node.right
            else:
                if index + 1 == len(prefix):
                    return current_node
                current_node = current_node.middle
                index += 1
            
        return None

    def _collect_all_words(self, node: Optional[TTNode], prefix: str) -> list[str]:
        """
        Collects all words starting from a given node.
        
        param:
        - node: The starting node for collecting words.
        - prefix: The prefix built up to the current node.
        """
        result: list = []

        if node is None:
            return result

        result.extend(self._collect_all_words(node.left, prefix))

        if node.word_end:
            result.append(prefix + node.letter)

        result.extend(self._collect_all_words(node.middle, prefix + node.letter))

        result.extend(self._collect_all_words(node.right, prefix))

        return result

    # Extra Credit Method
    # -----------------------------------------------------------

    def text_fill_premium(self, query: str) -> Optional[str]:
        """
        Returns the highest-priority search term matching the given prefix. Finds the node associated 
        with the prefix and traverses the subtree to locate the highest-priority word. If no term 
        matches the prefix, returns None.

        param:
        - query: The prefix to search for.
        """
        raise NotImplementedError