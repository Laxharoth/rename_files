from enum import StrEnum

class EventEnum(StrEnum):
    FILES_CHANGED = "files_changed"
    DIRECTORY_CHANGED = "directory_changed"
    RENAME_UPDATED = "rename_updated"
