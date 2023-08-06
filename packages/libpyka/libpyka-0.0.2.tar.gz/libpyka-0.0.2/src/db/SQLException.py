from typing import Optional, Union, Any
from typing import Callable, NoReturn
from typing import Sequence, Iterable, List, Tuple
from typing import Dict
from typing import TypeVar, Generic, NewType, Type

from utils import AbstractException

# Exceptionのサブクラスを表すGeneric型
E = NewType('E', BaseException)

##
# @breif DB関連の全ての例外の基底クラス
#
# @version 0.1.1
# @file     SQLException.py
# @date     2020-11-10
# @author           荒川 健太郎
class SQLException(AbstractException):
    ##
    # @brief  コンストラクタ
    #
    # @param mess エラーメッセージ
    # @param nextex 例外の元になった例外
    def __init__(self, mess: str, nextex: Optional[E]=None) -> None:
        self.message = mess
        self.nextex = nextex

# *importでimportするクラス・関数
__all__ = ['SQLException']

