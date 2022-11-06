from __future__ import annotations
from abc import ABC, abstractclassmethod
from typing import TypedDict, Any, Callable, Dict, List

class Event(TypedDict):
    """Event class used by the EventManager.
    @key target: The object that triggered the event.
    """
    target:Any

class EventEmitter(ABC):
    """Class for objects that emit events.
    @attribute __event_manager__[EventManager]
    """
    __event_manager__:EventManager
    def __init__(self):
        self.__event_manager__= EventManager()
    @abstractclassmethod
    def trigger(self,event_name:str):
        ...

class EventManager:
    """Singleton manages event"""
    __event_manager__:EventManager = None
    __events__:Dict[str,List[Callable[[Event],None]]]

    def __new__(cls):
        if not EventManager.__event_manager__:
            EventManager.__event_manager__ = super().__new__(EventManager)
            EventManager.__event_manager__.__events__ = dict()
        return EventManager.__event_manager__
    def attach(self,event_name:str,callback:Callable[[Event],None]):
        """Register a callback to a specific event.

        Args:
            event_name (str): The event name
            callback (Callable[[Any],None]): The callback to the event.
        """
        if not self.__events__.get(event_name):
            self.__events__[event_name] = list()
        self.__events__[event_name].append(callback)
    def detach(self,event_name:str,callback:Callable[[Event],None]):
        """Removes a callback from a specific event.

        Args:
            event_name (str): The name of the event.
            callback (Callable[[Any],None]): The callback to remove.
        """
        if not self.__events__.get(event_name):
            self.__events__[event_name] = list()
        for registered_callback in self.__events__[event_name]:
            if registered_callback == callback:
                return self.__events__[event_name].remove(callback)
        
    def trigger(self,event_name:str,event:Event={'target':None}):
        """Triggers a event with the event data.

        Args:
            event_name ([str]): The event name.
            event (dict, optional): The event data. Defaults to {}.
        """
        if not self.__events__.get(event_name):
            return
        for callback in self.__events__[event_name]:
            callback(event)
