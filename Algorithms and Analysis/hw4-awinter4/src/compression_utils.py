import copy
from queue import *
from dataclasses import *
from typing import *
from byte_utils import *
from typing import Optional

# [!] Important: This is the character code of the End Transmission Block (ETB)
# Character -- use this constant to signal the end of a message
ETB_CHAR = "\x17"

class HuffmanNode:
    '''
    HuffmanNode class to be used in construction of the Huffman Trie
    employed by the ReusableHuffman encoder/decoder below.
    '''
    
    # Educational Note: traditional constructor rather than dataclass because of need
    # to set default values for children parameters
    def __init__(self, char: str, freq: int, 
                 zero_child: Optional["HuffmanNode"] = None, 
                 one_child: Optional["HuffmanNode"] = None):
        '''
        HuffNodes represent nodes in the HuffmanTrie used to create a lossless
        encoding map used for compression. Their properties are given in this
        constructor's arguments:
        
        Parameters:
            char (str):
                Really, a single character, storing the character represented
                by a leaf node in the trie
            freq (int):
                The frequency with which the character / characters in a subtree
                appear in the corpus
            zero_child, one_child (Optional[HuffmanNode]):
                The children of any non-leaf, or None if a leaf; the zero_child
                will always pertain to the 0 bit part of the prefix, and vice
                versa for the one_child (which will add a 1 bit to the prefix)
        '''
        self.char = char
        self.freq = freq
        self.zero_child = zero_child
        self.one_child = one_child

    def is_leaf(self) -> bool:
        '''
        Returns:
            bool:
                Whether or not the current node is a leaf
        '''
        return self.zero_child is None and self.one_child is None

class ReusableHuffman:
    '''
    ReusableHuffman encoder / decoder that is trained on some original
    corpus of text and can then be used to compress / decompress other
    text messages that have similar distributions of characters.
    '''
    
    def __init__(self, corpus: str):
        '''
        Constructor for a new ReusableHuffman encoder / decoder that is fit to
        the given text corpus and can then be used to compress and decompress
        messages with a similar distribution of characters.
        
        Parameters:
            corpus (str):
                The text corpus on which to fit the ReusableHuffman instance,
                which will be used to construct the encoding map
        '''
        freq_map: Dict[str, int] = {}
        for ch in corpus:
            freq_map[ch] = freq_map.get(ch, 0) + 1
        freq_map[ETB_CHAR] = freq_map.get(ETB_CHAR, 0) + 1

        self._root: HuffmanNode = self._build_trie(freq_map)

        self._encoding_map: dict[str, str] = dict()

        self._generate_codes(self._root, "")
    
    def _build_trie(self, freq_map: Dict[str, int]) -> HuffmanNode:
        """
        Builds the Huffman trie (prefix tree) from a character frequency map.

        Parameters:
            freq_map (Dict[str, int]): Mapping from character to its frequency.

        Returns:
            HuffmanNode: Root node of the Huffman trie.
        """
        entries: List[tuple[int, str, HuffmanNode]] = [
            (freq, char, HuffmanNode(char, freq))
            for char, freq in freq_map.items()
        ]
        while len(entries) > 1:
            entries.sort()         
            f1, c1, n1 = entries.pop(0)
            f2, c2, n2 = entries.pop(0)
            parent_char = c1 if c1 < c2 else c2
            parent_node = HuffmanNode(parent_char, f1 + f2, n1, n2)
            entries.append((parent_node.freq, parent_node.char, parent_node))

        return entries[0][2]

    def _generate_codes(self, node: Optional[HuffmanNode], prefix: str) -> None:
        """
        Recursively traverse the Huffman trie to generate the encoding map.

        Parameters:
            node (Optional[HuffmanNode]): Current node in the trie.
            prefix (str): Accumulated bitstring prefix for the path to this node.
        """
        if node is None:
            return
        if node.is_leaf():
            self._encoding_map[node.char] = prefix or "0"
        else:
            self._generate_codes(node.zero_child, prefix + "0")
            self._generate_codes(node.one_child,  prefix + "1")
    
    def get_encoding_map(self) -> dict[str, str]:
        '''
        Simple getter for the encoding map that, after the constructor is run,
        will be a dictionary of character keys mapping to their compressed
        bitstrings in this ReusableHuffman instance's encoding
        
        Example:
            {ETB_CHAR: 10, "A": 11, "B": 0}
            (see unit tests for more examples)
        
        Returns:
            dict[str, str]:
                A copy of this ReusableHuffman instance's encoding map
        '''
        return copy.deepcopy(self._encoding_map)
    
    # Compression
    # ---------------------------------------------------------------------------
    
    def compress_message(self, message: str) -> bytes:
        '''
        Compresses the given String message / text corpus into its Huffman-coded
        bitstring, and then converted into a Python bytes type.
        
        [!] Uses the _encoding_map attribute generated during construction.
        
        Parameters:
            message (str):
                String representing the corpus to compress
        
        Returns:
            bytes:
                Bytes storing the compressed corpus with the Huffman coded
                bytecode. Formatted as (1) the compressed message bytes themselves,
                (2) terminated by the ETB_CHAR, and (3) [Optional] padding of 0
                bits to ensure the final byte is 8 bits total.
        
        Example:
            huff_coder = ReusableHuffman("ABBBCC")
            compressed_message = huff_coder.compress_message("ABBBCC")
            # [!] Only first 5 bits of byte 1 are meaningful (rest are padding)
            # byte 0: 1010 0011 (100 = ETB, 101 = 'A', 0 = 'B', 11 = 'C')
            # byte 1: 1110 0000
            solution = bitstrings_to_bytes(['10100011', '11100000'])
            self.assertEqual(solution, compressed_message)
        '''
        full_bits = "".join(self._encoding_map[ch] for ch in (message + ETB_CHAR))
        pad_len = (-len(full_bits)) % 8
        if pad_len:
            full_bits += '0' * pad_len
        chunks = [full_bits[i:i+8] for i in range(0, len(full_bits), 8)]
        return bitstrings_to_bytes(chunks)
    
    # Decompression
    # ---------------------------------------------------------------------------
    
    def decompress (self, compressed_msg: bytes) -> str:
        '''
        Decompresses the given bytes representing a compressed corpus into their
        original character format.
        
        [!] Should use the Huffman Trie generated during construction.
        
        Parameters:
            compressed_msg (bytes):
                Formatted as (1) the compressed message bytes themselves,
                (2) terminated by the ETB_CHAR, and (3) [Optional] padding of 0
                bits to ensure the final byte is 8 bits total.
        
        Returns:
            str:
                The decompressed message as a string.
        
        Example:
            huff_coder = ReusableHuffman("ABBBCC")
            # byte 0: 1010 0011 (100 = ETB, 101 = 'A', 0 = 'B', 11 = 'C')
            # byte 1: 1110 0000
            # [!] Only first 5 bits of byte 1 are meaningful (rest are padding)
            compressed_msg: bytes = bitstrings_to_bytes(['10100011', '11100000'])
            self.assertEqual("ABBBCC", huff_coder.decompress(compressed_msg))
        '''
        bits = "".join(byte_to_bitstring(b) for b in compressed_msg)
        result: List[str] = []
        node: HuffmanNode = self._root
        for bit in bits:
            next_node: Optional[HuffmanNode] = node.zero_child if bit == '0' else node.one_child
            assert next_node is not None, "Trie structure broken"
            node = next_node
            if node.is_leaf():
                if node.char == ETB_CHAR:
                    break
                result.append(node.char)
                node = self._root
        return ''.join(result)
    
        