
from tkinter import Misc
from tkinter.constants import BOTH, X
from typing import List, Literal

from Classes.modify_text_pattern import ModifiedTextPattern, ModifyTextPattern
from Event.event_manager import EventManager
from Classes.file_tree import FilesChangedEvent

from modify_text_label import ModifyTextLabel
from myfunctions import clear_frame
from vertical_scrolled_frame import VerticalScrolledFrame


def list_section(root:Misc,position:Literal['left', 'right', 'top', 'bottom'],pattern:ModifyTextPattern):
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

    def fill_display_list(event:FilesChangedEvent):
        files = event['files']
        modify_text_label_list.clear()
        clear_frame(display_list.interior)
        for file in files:
            modify_text_label_list.append(ModifyTextLabel(display_list.interior,file.file_name,pattern))
            modify_text_label_list[-1].pack(fill=X)
    def update_modified_text_label(event:ModifiedTextPattern):
        if pattern is not event['target']:
            return
        for label in modify_text_label_list:
            label.update_modified_text_label()
        
    event_manager.attach('files-change',fill_display_list)
    event_manager.attach('modified-text-pattern',update_modified_text_label)
