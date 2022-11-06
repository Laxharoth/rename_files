import os
from pathlib import Path
from tkinter import Button, Event, Misc
from tkinter.constants import END, X, Y
from tkinter.ttk import Treeview
from typing import List, Literal

from Event.event_manager import EventManager
from Classes.file_tree import DirectoryChangeEvent, FileDirectory, FileTree

from myfunctions import select_directory
from vertical_scrolled_frame import VerticalScrolledFrame

def directory_display_menu(root:Misc,filetree:FileTree,
        position:Literal['left', 'right', 'top', 'bottom']):
    """Appends a frame that shows the directories

    Args:
        root (Misc): The element where the frame will be attached.
        click_element_callback (Callable[[Event],None]): Callback that 
        position (Literal['left', 'right', 'top', 'bottom']): The position to pack the element.
    """

    event_manager = EventManager()
    
    display_menu = VerticalScrolledFrame(root , width = 150)
    display_menu.pack(side=position,fill=Y)
    select_directory_button = Button(display_menu.interior,
                                        text="Select Directory",
                                        command=lambda:select_directory(filetree))
    select_directory_button.pack(fill=X,padx=5,pady=5)
    treeview =  Treeview(display_menu.interior, selectmode='browse')
    treeview.pack(fill=Y)

    root_item = {"root":None}
    
    def fill_directory_display_menu(event:DirectoryChangeEvent):
        file_tree = event["target"]
        def fill_directory_display_menu_recursive(parent,path:Path):
            item = treeview.insert(parent,END,text=path.name)
            if parent == '':
                root_item['root']=item
            for sub_item in path.iterdir():
                if sub_item.is_dir():
                    fill_directory_display_menu_recursive(item,sub_item)
        if root_item['root']:
            treeview.delete(root_item['root'])
        fill_directory_display_menu_recursive('',Path(file_tree.root_directory.file_route))
    def create_change_directory_callback():
        current_directory:List[FileDirectory]=[None]
        def get_tree_view_route(tree_view,item):
            route =  tree_view.item(item,'text')
            parent = tree_view.parent(item)
            if not parent:
                return filetree.root_directory.file_route
            return os.path.join(get_tree_view_route(tree_view,parent),route)

        def change_current_directory(event:Event):
            item_text:str = None
            treeview = event.widget
            for item in treeview.selection():
                item_text = get_tree_view_route(treeview,item)
            new_directory = filetree.find_directory(item_text)
            if current_directory[0] is new_directory or new_directory is None:
                return
            current_directory[0] = new_directory
            filetree.set_current_directory(new_directory)
        return change_current_directory
    
    treeview.bind('<<TreeviewSelect>>', create_change_directory_callback())
    event_manager.attach('directory-change',fill_directory_display_menu)
    