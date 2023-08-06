from typing import Optional, Union
from typing import Callable
from typing import Sequence, Iterable, List
from typing import Dict
from typing import TypeVar, Generic, NewType

# 元の例外となる型 BaseExceptionを継承
E = NewType('E', BaseException)

##
# @breif IMAPのエラーを表す例外クラス。
#
# @version 0.1.1
# @file AbstractException.py
# @date 2020-11-04
# @author 荒川 健太郎
class AbstractException(Exception):
    ##
    # @brief コンストラクタ
    #
    # @param message   この例外のメッセージ
    # @param nextex     この例外の元になった例外
    def __init__(self, message: str, nextex: Optional[E]=None) -> None:
        self.__message: str = message
        self.__nextex = nextex

    ##
    # @breif この例外の元になった例外
    # 
    # @return この例外の元になった例外
    @property
    def nextex(self) -> Optional[E]:
        return self.__nextex
    ##
    # @breif この例外の元になった例外を設定する。
    # 
    # @param nextex この例外の元になった例外
    @nextex.setter
    def nextex(self, nextex: Optional[E]) -> None:
        self.__nextex = nextex
    
    ##
    # @brief 例外メッセージ
    #
    # @return 例外メッセージ
    @property
    def message(self) -> str:
        return self.__message
    ##
    # @brief 例外メッセージをセットする
    #
    # @param 例外メッセージ
    @message.setter
    def message(self, message):
        self.__message = message

    ##
    # @brief このオブジェクトの文字列表現を返す。
    #
    # @return オブジェクトの文字列表現
    def __str__(self) -> str:
        ret = self.message + '\n'
        ret += str(self.nextex)
        return ret

# *でインポートする関数とクラス名
__all__ = ['AbstractException']

