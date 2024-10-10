from typing import TypeVar, Union, Generic, Callable, Iterable


T = TypeVar('T')
class ListObserver(Generic[T]):
    def __init__(self,init:Union[list[T], None] = None) -> None:
        self.state: list[T] = []
        self.subscriptions:set[Callable[[],None]] = set()
        if init is not None:
            self.state.extend(init)
    
    def subscribe(self, subcription:Callable[[],None]) -> Callable[[], None]:
        self.subscriptions.add(subcription)
        unsubscribe = lambda: self.subscriptions.remove(subcription)
        return unsubscribe
    
    def append(self, item:T):
        self.state.append(item)
        self._notify()
    
    def insert(self, position:int, item:T):
        self.state.insert(position, item)
        self._notify()
    
    def pop(self, position:Union[None, int] = None):
        if position is None:
            retval = self.state.pop()
        else :
            retval = self.state.pop(position)
        self._notify()
        return retval
    
    def reverse(self):
        self.state.reverse()
        self._notify()
        
    def remove(self, value:T):
        self.state.remove(value)
        self._notify()
        
    def clear(self):
        self.state.clear()
        self._notify()
        
    def extend(self, values:Iterable[T]):
        self.state.extend(values)
        self._notify()
        
    def setList(self, values:Iterable[T]):
        self.state.clear()
        self.state.extend(values)
        self._notify()
    
    def _notify(self):
        for subscription in self.subscriptions:
            subscription()        
    
    def __iter__(self):
        return self.state.__iter__()