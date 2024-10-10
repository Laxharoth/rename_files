from dataclasses import dataclass

@dataclass()
class RenameFileStruct:
    path:str
    original:str
    renamed:str