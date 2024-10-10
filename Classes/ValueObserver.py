from typing import TypeVar, Union, Generic, Callable, Iterable

T = TypeVar('T')

class ValueObserver(Generic[T]):
    def __init__(self,init:T) -> None:
        self._state: T = init
        self.subscriptions:set[Callable[[],None]] = set()
        
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self,state:T):
        self._state = state
        self._notify()
        
    
    def subscribe(self, subcription:Callable[[],None]) -> Callable[[], None]:
        self.subscriptions.add(subcription)
        unsubscribe = lambda: self.subscriptions.remove(subcription)
        return unsubscribe
    
    def _notify(self):
        for subscription in self.subscriptions:
            subscription()