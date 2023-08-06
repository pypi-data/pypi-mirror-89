from dataclasses import dataclass
from logging import getLogger, Logger
from requests import Session, get

from simdak.config import HEADERS


class BaseSimdakPaud(object):
    _domain: str = "https://dapo.paud-dikmas.kemdikbud.go.id"
    _base_url: str = "https://dapo.paud-dikmas.kemdikbud.go.id/simdak/"
    _logger: Logger = getLogger("simdak-paud")
    _session: Session = Session()

    def __init__(
        self,
        login: bool = False,
        modul: bool = False,
        logger: Logger = getLogger("simdak-paud"),
        retry: int = 0,
    ):
        self._login: bool = login
        self._modul: bool = modul
        self._logger: Logger = logger
        self._retry: int = retry
        self._session.headers.update(HEADERS)

    @classmethod
    def is_online(cls, url: str = "site/login") -> bool:
        return get(cls._base_url + url).ok
