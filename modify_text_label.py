from dataclasses import dataclass
from tkinter import Entry, Frame, Label, Misc, StringVar
from tkinter.constants import X

from Classes.modify_text_pattern import ModifyTextPattern


@dataclass
class ModifyTextLabel(Frame):
    """Creates a frame which contains 2 text labels one with the original text and other with the modified text."""
    __modify_text_label:Label
    __original_text:str
    __modify_text_pattern:ModifyTextPattern

    def __init__(self,master:Misc,original_text:str,modify_text_pattern:ModifyTextPattern):
        super().__init__(master)
        self.__original_text = original_text
        self.__modify_text_pattern = modify_text_pattern
        self.__init_components()
    
    @property
    def __modified_text(self)->str:
        """The text after the modification"""
        return self.__modify_text_pattern.modify_text(self.__original_text)

    def __init_components(self):
        """Initialize components 
        * The container frame 
        * The Label that containt the original text 
        * The Label with the modified text.
        """
        data_string = StringVar()
        data_string.set(self.__original_text)
        entry = Entry(self,textvariable=data_string,state='readonly')
        self.__modify_text_label = Label(self,text=self.__modified_text,anchor='w')
        self.__original_bg = self.__modify_text_label.cget('background')
        
        entry.grid(row=0,column=0, sticky="nsew")
        self.__modify_text_label.grid(row=0,column=1, sticky="nsew")

        self.grid_columnconfigure(0, weight=1, uniform='group1')
        self.grid_columnconfigure(1, weight=1, uniform='group1')
        self.grid_rowconfigure(0, weight=1)
    
    def update_modified_text_label(self):
        """Sets the label content to the modified text."""
        modified_text = self.__modified_text
        bg = self.__original_bg if self.__original_text == modified_text else 'green'
        self.__modify_text_label.config(bg=bg)
        self.__modify_text_label.config(text=modified_text)
