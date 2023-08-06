from typing import TypeVar, Mapping, Type, Callable, Any

TLeft = TypeVar('TLeft')
TRight = TypeVar('TRight')


class Either(Mapping[TLeft, TRight]):

    _left: Type[TLeft]
    _right: Type[TRight]
    _isLeft: bool

    def __getitem__(self, k):
        pass

    def __len__(self):
        pass

    def __iter__(self):
        pass

    @classmethod
    def left(cls, val: Type[TLeft]):
        either = Either[TLeft, TRight]()
        either._left = val
        either._isLeft = True
        return either

    @classmethod
    def right(cls, val: Type[TRight]):
        either = Either[TLeft, TRight]()
        either._right = val
        either._isLeft = False
        return either

    def match(self, left_func: Callable[[TLeft], Any], right_func: Callable[[TRight], Any]):
        return left_func(self._left) if self._isLeft else right_func(self._right)
