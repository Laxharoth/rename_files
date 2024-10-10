from tkinter import Tk
from Widgets.rename_files import RenameFilesGUI

from Classes.ListObserver import ListObserver
from Classes.ValueObserver import ValueObserver

from Classes.modify_text import get_text_generators, generate_text
from Classes.RenameFilesStruct import RenameFileStruct
from Classes.file_tree import FileTree, FileDirectory

from Event.event_manager import EventManager
from Event.EventValues import EventEnum

def main():
    filenames:ListObserver[RenameFileStruct] = ListObserver()
    search_pattern:ValueObserver[str] = ValueObserver("")
    replace_pattern:ValueObserver[str] = ValueObserver("")
    
    event_manager = EventManager()
    
    def modify_rename_file_structs():
        statics, generators = get_text_generators(search_pattern.state)
        for filename in filenames:
            filename.renamed = generate_text(filename.original, replace_pattern.state, statics, generators)
        event_manager.trigger(EventEnum.RENAME_UPDATED)
    filenames.subscribe(modify_rename_file_structs)
    search_pattern.subscribe(modify_rename_file_structs)
    replace_pattern.subscribe(modify_rename_file_structs)
    
    def fill_rename_filenames(event):
        filetree:FileTree = event["target"]
        rename_files = [RenameFileStruct(path=dir.file_route, original=file.file_name, renamed="") for file, dir in zip(filetree.file_path, filetree.directory_list)]
        filenames.setList(rename_files)
        event_manager.trigger(EventEnum.RENAME_UPDATED)
    
    event_manager.attach(EventEnum.FILES_CHANGED,fill_rename_filenames)
    
    
    root = Tk()
    root.update_idletasks() 
    gui = RenameFilesGUI(root, filenames, search_pattern, replace_pattern)
    root.event_generate("<Configure>")
    root.mainloop()

if __name__ == "__main__":
    main()