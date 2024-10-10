from dataclasses import dataclass
from tkinter import Entry, Frame, Label, Misc, StringVar
from tkinter.constants import X
from typing import NamedTuple
from Classes.modify_text import TextGenerator, generate_text
from Classes.RenameFilesStruct import RenameFileStruct

ModifyTextPattern = tuple[list[str], list[TextGenerator]]

@dataclass
class ModifyTextLabel(Frame):
    """Creates a frame which contains 2 text labels one with the original text and other with the modified text."""
    __modify_text_label:Label
    __original_text:str
    __modified_text:str

    def __init__(self,master:Misc, rename_file_struct:RenameFileStruct):
        super().__init__(master)
        self.__original_text = rename_file_struct.original
        self.__modified_text = rename_file_struct.renamed
        self.__init_components()
    
    @property
    def modified_text(self)->str:
        """The text after the modification"""
        return self.__modified_text

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
