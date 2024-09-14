class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.orig = None
        
class Trie:
    def __init__(self):
        self.root = TrieNode()
        
    def insert(self, word, orig_word = None):
        """
        Insert the word into Trie.
        
        Keyword arguments:
        word -- String
        orig_word -- Word origin
        """
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()
                
            node = node.children[c]
            
        node.is_end_of_word = True
        node.orig = orig_word
        
    def find_prefix_node(self, prefix) -> TrieNode:
        """
        Find node where prefix ends.
        
        Keyword arguments:
        prefix -- Prefix of node
        Return: Node.
        """
        node = self.root
        
        for c in prefix:
            if c not in node.children:
                return None
            node = node.children[c]
            
        return node
    
    def collect_words(self, node: TrieNode, prefix):
        """
        Recursively collect all words from given node.
        
        Keyword arguments:
        node -- Trie node
        prefix -- Node prefix
        Return: List of words.
        """
        words = []
        if node.is_end_of_word:
            words.append(node.orig)
            
        for c, c_node in node.children.items():
            words.extend(self.collect_words(c_node, prefix+c))
            
        return words
    
    def words_with_prefix(self, prefix):
        """
        Return all words in the Trie that starts with the given prefix.
        
        Keyword arguments:
        prefix -- String prefix.
        Return: List of words with prefix.
        """
        node = self.find_prefix_node(prefix=prefix)
        
        if not node:
            return []
        
        return self.collect_words(node=node, prefix=prefix)
        