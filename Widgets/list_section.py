
from tkinter import Misc
from tkinter.constants import BOTH, X
from typing import List, Literal

from Event.event_manager import EventManager
from Classes.file_tree import FilesChangedEvent
from Classes.RenameFilesStruct import RenameFileStruct
from Classes.ListObserver import ListObserver

from Widgets.modify_text_label import ModifyTextLabel
from myfunctions import clear_frame
from vertical_scrolled_frame import VerticalScrolledFrame
from Event.EventValues import EventEnum


def list_section(root:Misc,position:Literal['left', 'right', 'top', 'bottom'],rename_filenames:ListObserver[RenameFileStruct]):
    """Appends a frame with the names of the files.

    Args:
        root (Misc): The element where it will be attached.
        position (Literal['left', 'right', 'top', 'bottom']): The position will be attached.
        pattern (ModifyTextPattern): [description] The pattern to modify the files names.
    """
    event_manager = EventManager()
    
    display_list = VerticalScrolledFrame(root)
    display_list.pack(side=position,fill=BOTH, expand=1)
    display_list.config(bg='green')

    modify_text_label_list:List[ModifyTextLabel] = list()
    
    def fill_display_list(_event:FilesChangedEvent):
        modify_text_label_list.clear()
        clear_frame(display_list.interior)
        for file in rename_filenames:
            modify_text_label_list.append(ModifyTextLabel(display_list.interior,file))
            modify_text_label_list[-1].pack(fill=X)
        
    event_manager.attach(EventEnum.RENAME_UPDATED,fill_display_list)
