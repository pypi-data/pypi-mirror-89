##
# @brief 一般的なユーティリティモジュール。
#

import hashlib
from chardet import UniversalDetector
import requests

# 4バイト unsigned int の最大値
MAX_UNSIGNED_INT = 4294967295
# 8バイト unsigned long の最大値
MAX_UNSIGNED_LONG = 18446744073709551615

##
# @brief バイトコンテントから４バイトの整数のハッシュ値を生成して返す。
#
# ハッシュはSHA256を使用。
# 引数でハッシュ値の範囲を指定できる。指定できない場合は４バイト(32ビット)。
# @param byte_content バイトデーター
# @param max_range  生成されるハッシュ値の最大値
# @return 整数のハッシュ値
def hashint(byte_content: bytes, max_range: int=MAX_UNSIGNED_INT):
    ret = 1
    sha = hashlib.sha256()
    sha.update(byte_content)
    hashval = sha.hexdigest()
    for ch in hashval:
        val = ord(ch)
        ret = ret + val
    ret = ret * 1234567
    return ret % max_range

##
# @brief バイトコンテントから8バイトの整数のハッシュ値を生成して返す。
#
# @return 8バイトのハッシュ値の整数
def hashint_64(byte_content: bytes):
    return hashint(byte_content, MAX_UNSIGNED_LONG)



##
# @brief シーケンスを引数のsize分の大きさのリストで分割して返す。
#
# ジェネレーター関数である。
# @param seq シーケンス
# @param size 分割の大きさ
# @param size分の大きさのリスト
def seq_split(seq, size):
    maxidx = size
    length = len(seq)       # シーケンスのサイズ
    for minidx in range(0, length, size):
        maxidx = minidx + size
        yield seq[minidx:maxidx]

##
# @brief バイト文字列のエンコード名を返す。
# 
# @param bytes_content バイト文字列
# @return 文字コード名の文字列
def bytes_enc(bytes_content):
    detector = UniversalDetector()
    buflen = 1000   # detectorに渡すバッファの大きさ
    for buf in seq_split(bytes_content, buflen):
        detector.feed(buf)
        if detector.done:
            break

    # UnivarsalDetectorのresultアトリビュートで
    # エンコーディング名を取り出す前にclose()関数を呼ばないと
    # きちんとエンコーディングを取得できないので注意。
    detector.close()
    encdic = detector.result
    return encdic['encoding']


# *importでimportするクラス・関数
__all__ = ['MAX_UNSIGNED_INT', 'MAX_UNSIGNED_LONG', 'hashint', 'hashint_64', 'bytes_enc']
