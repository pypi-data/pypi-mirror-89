from fuzzywuzzy import fuzz
from logging import getLogger
from typing import Callable, Dict, List, Optional, TypeVar
from . import JENIS_KOMPONEN

logger = getLogger(__name__)


def get_key(nama: str, data: Dict[int, str] = JENIS_KOMPONEN) -> Optional[int]:
    nama = nama.replace("\r\n", " ")
    for k, v in data.items():
        if v == nama:
            return k
    return None


def get_fuzz(f: str, data: Dict[int, str], default: int = 0, ok: int = 80) -> int:
    for k, v in data.items():
        if fuzz.ratio(v, f) > ok:
            logger.debug(f"Key dari {f} ditemukan")
            return k
    logger.debug(f"Key dari {f} tidak ditemukan")
    return default


T = TypeVar("T")


def try_find_one(datas: List[T], f: T, func: Callable[[T], str], ok: int = 90) -> T:
    for t in datas:
        if fuzz(func(t), func(f)) >= ok:
            return t
    return f
