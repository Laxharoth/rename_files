import os
from tkinter import Misc, filedialog

from Classes.file_tree import FileTree

def clear_frame(master:Misc):
    """Removes the children from a tkinter widget.

    Args:
        * master (Misc): The widget to remove children from.
    """
    for widget in master.winfo_children():
        widget.destroy()

def rename_file(original_file_path,renamed_file_name):
    """A small wrapper for the os.rename() function

    Args:
        * original_file_path ([type]): The path to the original file.
        * renamed_file_name ([type]): The name of the new file (basename).
    """
    filename  = os.path.basename(original_file_path)
    directory = os.path.dirname(original_file_path)
    if filename == renamed_file_name:
        return
    os.rename(
                src=os.path.abspath(original_file_path),
                dst=os.path.join(directory,renamed_file_name)
             ) 

def select_directory(filetree:FileTree):
    """Opens a directory select dialog and sets the FileTree root directory to the specified by the dialog.

    Args:
        * filetree (FileTree): The FileTree which will update the root directory.
    """
    directory=filedialog.askdirectory()
    if directory:
        filetree.set_root_directory(directory)