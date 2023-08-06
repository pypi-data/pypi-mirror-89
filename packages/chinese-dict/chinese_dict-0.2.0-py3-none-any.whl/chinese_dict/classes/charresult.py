from ..errors.NotFound import WordNotFoundException
from treelib import Tree
from ..helpers.converter import converter


class CharResult:
    def __init__(self, character, han_dict):
        self._character = character
        self._han_dict = han_dict
    
    @property
    def character(self):
        return self._character

    @property
    def simplified(self):
        try:
            return self._han_dict._lookup_word(self.character).simplified
        except WordNotFoundException:
            return None 
        
    
    @property
    def traditional(self):
        try:
            return self._han_dict._lookup_word(self.character).traditional
        except WordNotFoundException:
            return None 
        
    def _pinyin(self, style):
        try:
            res = self._han_dict._lookup_word(self.character).pinyin(style)
            if style == 'accented':
                return [converter(pin) for pin in res]
            return res
        except WordNotFoundException:
            return None 
    
    @property
    def pinyin(self):
        return self._pinyin(self._han_dict.pinyin_style)
    
    @property
    def meaning(self):
        try:
            return self._han_dict._lookup_word(self.character).meaning
        except WordNotFoundException:
            return None
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.character})'
    

    def tree(self):
        tree = Tree()
        tree.create_node(self.character, self)
        
        
        def recursive(parent, tree):
            for child in parent.components:
                tree.create_node(child.character, child, 
                                 parent=parent)
                if hasattr(child, 'components'):
                    recursive(child, tree)
                    
        if hasattr(self, 'components'):
            recursive(self, tree)
            
        tree.show()


class Radical(CharResult):
    @property
    def num_strokes(self):
        try: 
            return self._han_dict._lookup_char(self.character).num_strokes
        except WordNotFoundException:
            return None


class BaseChar(CharResult):
    def __init__(self, character, num_strokes, radical, han_dict):
        super().__init__(character, han_dict)
        self._num_strokes = num_strokes
        self._radical = Radical(radical, han_dict) if radical != '*' else Radical(character, han_dict)

    @property
    def num_strokes(self):
        return self._num_strokes
    
    @property
    def radical(self):
        return self._radical


class Char(BaseChar):
    def __init__(self, character, num_strokes, first, 
                 second, radical, han_dict):
        super().__init__(character, num_strokes, radical, han_dict)
        self._first = first
        self._second = second

    @property
    def components(self):
        return [self._han_dict._lookup_char(self._first), 
                self._han_dict._lookup_char(self._second)]


class MultipleChar(CharResult):
    @property
    def components(self):
        return [self._han_dict._lookup_char(char) for char in self.character]


class WordResult:
    def __init__(self, character, simplified, traditional, pinyin, meaning, 
                 han_dict):
        self._character = character
        self._simplified = simplified
        self._traditional = traditional
        self._pinyin = pinyin
        self._meaning = meaning
        
    @property
    def character(self):
        return self._character

    @property
    def simplified(self):
        return self._simplified
    
    @property
    def traditional(self):
        return self._traditional

    def pinyin(self, style='numerical'):
        if style == 'accented':
            return [converter(pin) for pin in self._pinyin]
        return self._pinyin 

    @property
    def meaning(self):
        return self._meaning
