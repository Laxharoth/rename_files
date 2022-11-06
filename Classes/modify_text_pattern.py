from typing import List, Literal, Tuple

from Event.event_manager import EventEmitter, Event

class ModifyTextPattern(EventEmitter):
    """Defines the pattern to modify text.
        * \* represents a wildcard
        * any othe string represents a static string
        * Wildcards are applied in order of appearance.
        * Example:
        *     -ModifyTextPattern('*abc*def*','*123*456*')
        *     -input = 'lorem abc ipsum def foo'
        *     -output = 'lorem 123 ipsum 456 foo'
    """
    def __init__(self,search_pattern:str='*',modify_pattern:str='*'):
        super().__init__()
        self._search_pattern = search_pattern
        self._modify_pattern = modify_pattern
    
    @property
    def search_pattern(self)->str:
        """The text search pattern"""
        return self._search_pattern
    @property
    def modify_pattern(self)->str:
        """The text modify pattern"""
        return self._modify_pattern
    @search_pattern.setter
    def search_pattern(self,pattern:str):
        """Sets the search pattern only if it's a string"""
        if type(pattern) != type(''):
            print("Search pattern must be str")
            return
        self._search_pattern = pattern
        self.trigger('modified-text-pattern')
        self.trigger('modified-text-search-pattern')
    @modify_pattern.setter
    def modify_pattern(self,pattern:str):
        """Set the modify pattern only if it's a string."""
        if type(pattern) != type(''):
            print("Modify pattern must be str")
            return
        self._modify_pattern = pattern
        self.trigger('modified-text-pattern',)
        self.trigger('modified-text-replace-pattern',)
    @property
    def fixed_text_pattern(self)->Tuple[List[str],List[str]]:
        """Gets the fixed text pattern for search in original str and to replace

        Returns:
            [tuple]: the search pattern and then the replacement pattern
        """        
        fixed_text_original_text_list = self._search_pattern.split('*')
        fixed_text_modify_text_pattern = self._modify_pattern.split('*')
        return fixed_text_original_text_list,fixed_text_modify_text_pattern

    def modify_text(self,original_text:str)->str:
        """Applies the text modify pattern only if the original text matches the search pattern.

        Args:
            original_text (str): The text to modify.

        Returns:
            str: The modified text if it matches the search pattern. The same text otherwise.
        """
        #Separete constants
        fixed_text_search_text_list,\
        fixed_text_replace_text_pattern = self.fixed_text_pattern
        modified_string:str = ''
        if len(fixed_text_search_text_list) < len(fixed_text_replace_text_pattern) or \
           not self.search_text_pattern_in_original_text(original_text) or \
           not original_text.startswith(fixed_text_search_text_list[0]) or \
           not original_text.endswith(fixed_text_search_text_list[-1]):
            return original_text
        
        #Find wildcards
        wildcard_text_list = self._get_wildcard_text(original_text, fixed_text_search_text_list)
        #Fix size of wildcards
        wildcard_text_list = wildcard_text_list[:len(fixed_text_replace_text_pattern)]
        if wildcard_text_list[0] == '':
            wildcard_text_list = wildcard_text_list[1:]+wildcard_text_list[:1]
        
        for replace_substring,wildcard_substring in zip(fixed_text_replace_text_pattern,wildcard_text_list):
            modified_string += replace_substring + wildcard_substring
        return modified_string

    def _get_wildcard_text(self, original_text:str, fixed_text_search_text_list:List[str])->List[str]:
        """Generates the list with the wildcard from the search pattern. The

        Args:
            original_text (str): The text to search for the wildcards.
            fixed_text_search_text_list (List[str]): The static text to search.

        Returns:
            List[str]: The list of the wildcards.
        """
        start_widcard_index = len(fixed_text_search_text_list[0])
        wildcard_text_list = list()
        for substring in fixed_text_search_text_list[1:]:
            end_widcard_index = original_text[start_widcard_index:].find(substring)
            wildcard_text_list.append(original_text[start_widcard_index:start_widcard_index+end_widcard_index])
            start_widcard_index += end_widcard_index + len(substring)
        wildcard_text_list.append(original_text[start_widcard_index:])
        return wildcard_text_list

    def search_text_pattern_in_original_text(self,original_text:str)->bool:
        """Checks that the original text matches the search pattern.

        Args:
            original_text (str): The original text.

        Returns:
            bool: True if the original text matches the search pattern.
        """
        starting_index = 0
        fixed_text_search_text_list,_ = self.fixed_text_pattern
        for substring in fixed_text_search_text_list:
            increase_index_quality = original_text[starting_index:].find(substring)
            if increase_index_quality<0:
                return False
            starting_index += increase_index_quality + len(substring)
        return True

    def trigger(self,
            event_name: Literal['modified-text-pattern', 
                'modified-text-search-pattern', 
                'modified-text-replace-pattern', ]
               )->None:
        if event_name == 'modified-text-pattern':
            self.__event_manager__.trigger('modified-text-pattern',event={'target':self})
        if event_name == 'modified-text-search-pattern':
            self.__event_manager__.trigger('modified-text-search-pattern',event={'target':self,'pattern':self._search_pattern})
        if event_name == 'modified-text-replace-pattern':
            self.__event_manager__.trigger('modified-text-replace-pattern',event={'target':self,'pattern':self._modify_pattern})
        
class ModifiedTextPattern(Event):
    """An event fired when either text pattern in a ModifyTextPattern is changed
        @key target[ModifyTextPattern]
    """
    target:ModifyTextPattern
class ModifiedTextSearchPattern(Event):
    """An event fired when either text pattern in a ModifyTextPattern is changed
        @key target[ModifyTextPattern]
        @key pattern[str] The search pattern.
    """
    target:ModifyTextPattern
    pattern:str
class ModifiedTextReplacePattern(Event):
    """An event fired when either text pattern in a ModifyTextPattern is changed
        @key target[ModifyTextPattern]
        @key pattern[str] The replace pattern.
    """
    target:ModifyTextPattern
    pattern:str
