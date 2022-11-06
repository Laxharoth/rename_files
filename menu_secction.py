from tkinter import Button, Entry, Event, Frame, Label, Misc
from tkinter.constants import X
from typing import Literal

from Classes.file_tree import FileTree
from Classes.modify_text_pattern import ModifyTextPattern
from myfunctions import rename_file


def menu_section(root:Misc,position:Literal['left', 'right', 'top', 'bottom'],modify_text_pattern:ModifyTextPattern,file_tree:FileTree)->None:
    '''Insert the menu selection into a window or frame'''

    def update_search_text_pattern(event:Event):
        text_box_str = text_pattern_select_input.get()
        modify_text_pattern.search_pattern = text_box_str
    def update_modify_text_pattern(event:Event):
        text_box_str = text_pattern_apply_input.get()
        modify_text_pattern.modify_pattern = text_box_str
    def rename_files():
        for filename in file_tree.file_path:
            rename_file(filename.file_route,modify_text_pattern.modify_text(filename.file_name))
        file_tree.reload()

    menu_container = Frame(root)
    menu_container.pack(side=position,fill=X)

    Label(menu_container, text="Regex selector").pack()
    text_pattern_select_input = Entry(menu_container)
    text_pattern_select_input.pack(fill=X,padx=10)
    text_pattern_select_input.bind('<KeyRelease>',update_search_text_pattern)
    Label(menu_container, text="Regex Applier").pack()
    text_pattern_apply_input = Entry(menu_container)
    text_pattern_apply_input.pack(fill=X,padx=10)
    text_pattern_apply_input.bind('<KeyRelease>',update_modify_text_pattern)
    Button(menu_container , text="Apply", command=rename_files).pack(fill=X,padx=10,pady=5)
