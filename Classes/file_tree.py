from __future__ import annotations
import os
from dataclasses import dataclass
from typing import List, Literal

from Event.event_manager import Event, EventEmitter

@dataclass
class FileDirectory:
    """Stores the filename and the abspath path"""
    file_name:str
    file_route:str

    def __contains__(self,key:str)->bool:
        """Checks if the key is either the file_name or file_path"""
        return key == self.file_name or \
            False if not os.path.exists(key) else \
                os.path.abspath(key)==os.path.abspath(self.file_route)

class FileTree(EventEmitter):
    """Stores the Root Directory the subdirectories and Files in the selected directory."""
    def __init__(self):
        super().__init__()
        self.__root_directory:FileDirectory = None
        self.__current_directory:FileDirectory = None
        self.__directory_list:List[FileDirectory] = list()
        self.__file_path:List[FileDirectory] = list()
        
    def __fill_file_directory(self,update_directory_list:bool=True):
        """Replace the file path list with the files in the current_directory.
        If update_directory_list is True also replaces the directory list

        Args:
            update_directory_list (bool, optional): [description]. Defaults to True.
        """
        self.__file_path.clear()
        if update_directory_list:
            self.__directory_list.clear()
        for subdir, dirs, files in os.walk(self.__current_directory.file_route):
            if update_directory_list:
                self.__directory_list.append(FileDirectory(os.path.basename(subdir),os.path.abspath(subdir)))
            for file in files:
                self.__file_path.append(FileDirectory(file,os.path.join(subdir, file)))

    def set_root_directory(self,root_directory:str):
        """Changes the root_directory

        Args:
            root_directory (str): The path of the root_directory
        """
        if self.__root_directory and root_directory in self.__root_directory:
            return
        self.__root_directory = self.__current_directory = FileDirectory(root_directory,os.path.abspath(root_directory))
        self.__fill_file_directory()
        self.trigger('directory-change')
        self.trigger('files-change')

    def set_current_directory(self,current_directory:FileDirectory):
        """Sets the current_directory and updates the file list.
            Only changes the current directory if current_directory is in directory_list

        Args:
            current_directory (FileDirectory): The directory to change.
        """
        if current_directory not in self.__directory_list and \
           current_directory is not self.__current_directory:
            return
        self.__current_directory = current_directory
        self.reload()

    def reload(self):
        """Reload the files in the current directory"""
        self.__fill_file_directory(False)
        self.trigger('files-change')

    @property
    def root_directory(self)->FileDirectory:
        """The root directory"""
        return self.__root_directory
    @property
    def directory_list(self)->List[FileDirectory]:
        """The directories contained in the root_directory"""
        return self.__directory_list
    @property
    def file_path(self)->List[FileDirectory]:
        """The files contained in the current directory"""
        return self.__file_path
    
    def find_directory(self, path:str)->FileDirectory:
        """Returns the first directory that matches the given path

        Args:
            path (str): The path of the directory.

        Returns:
            FileDirectory: The FileDirectory That has the path specified. None if the path is not found.
        """
        for directory in self.directory_list:
            if path in directory:
                return directory
        return None

    def trigger(self,event_name:Literal['directory-change','files-change']):
        if(event_name == 'directory-change'):
            return self.__event_manager__.trigger('directory-change',event={ "target":self,'directory':self.__root_directory})
        if(event_name == 'files-change'):
            return self.__event_manager__.trigger('files-change',event={ "target":self,'files':self.__file_path})

class DirectoryChangeEvent(Event):
    """An event fired when the root directory in a FileTree is changed"""
    target:FileTree
    directory:FileDirectory

class FilesChangedEvent(Event):
    """An event fired when the files in a FileTree are changed"""
    target:FileTree
    files:List[FileDirectory]
