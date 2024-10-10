from tkinter import Frame, Tk
from tkinter.constants import BOTH, BOTTOM, LEFT, RIGHT, TOP, Y
from Classes.file_tree import FileTree
from Classes.modify_text import TextGenerator
from Widgets.directory_display_menu import directory_display_menu
from Widgets.list_section import list_section
from Widgets.menu_secction import menu_section
from myfunctions import select_directory
from typing import Tuple,List

from Classes.ListObserver import ListObserver
from Classes.ValueObserver import ValueObserver
from Classes.RenameFilesStruct import RenameFileStruct
class RenameFilesGUI:
    def __init__(self, master:Tk, rename_filenames:ListObserver[RenameFileStruct], search_pattern:ValueObserver, replace_pattern:ValueObserver):
        """Fills the Tk element with:
            * Entry elements to define the rename rules
            * A button to apply the rename rules
            * A list of the directories
            * A list of the files in the selected directory

        Args:
            * master (Tk): [description] The main component
        """        
        self.master = master
        master.title("A simple GUI")
        master.minsize(600,400)
        self.file_tree = FileTree()
        

        left_section = Frame(master)
        left_section.pack(side=LEFT,fill=Y)
        left_section.config(bg="blue")
        directory_display_menu(left_section,self.file_tree,LEFT)
        right_section = Frame(master)
        right_section.config(bg="red")
        right_section.pack(side=RIGHT,fill=BOTH,expand=1)
        menu_section(right_section,TOP,search_pattern, replace_pattern, rename_filenames,self.file_tree)
        list_section(right_section,BOTTOM,rename_filenames)

        select_directory(self.file_tree)
