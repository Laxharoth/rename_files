from tkinter import Frame, Tk
from tkinter.constants import BOTH, BOTTOM, LEFT, RIGHT, TOP, Y
from Classes.file_tree import FileTree
from Classes.modify_text_pattern import ModifyTextPattern
from directory_display_menu import directory_display_menu
from list_section import list_section
from menu_secction import menu_section
from myfunctions import select_directory


class RenameFilesGUI:
    def __init__(self, master:Tk):
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
        self.pattern = ModifyTextPattern('','')

        left_section = Frame(master)
        left_section.pack(side=LEFT,fill=Y)
        left_section.config(bg="blue")
        directory_display_menu(left_section,self.file_tree,LEFT)
        right_section = Frame(master)
        right_section.config(bg="red")
        right_section.pack(side=RIGHT,fill=BOTH,expand=1)
        menu_section(right_section,TOP,self.pattern,self.file_tree)
        list_section(right_section,BOTTOM,self.pattern)

        select_directory(self.file_tree)

def main():
    root = Tk()
    root.update_idletasks() 
    gui = RenameFilesGUI(root)
    root.event_generate("<Configure>")
    root.mainloop()

if __name__ == "__main__":
    main()
