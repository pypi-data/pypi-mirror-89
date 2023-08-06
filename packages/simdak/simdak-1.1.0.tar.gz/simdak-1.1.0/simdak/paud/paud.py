from __future__ import annotations
from requests import Session
from logging import getLogger
from . import BaseSimdakPaud, SimdakPaudAuth, SimdakRkasPaud


class SimdakPaud(SimdakPaudAuth):
    def __init__(self, email: str, password: str, retry: int = 3):
        self._logger = getLogger(self.__class__.__name__)
        self._email = email
        self._password = password
        self._retry = retry
        super(SimdakPaud, self).__init__(
            logger=getLogger(f"SP-{email}"),
        )
        self._login = self.login()
        self._modul = self.modul()
        self.rkas = SimdakRkasPaud()

    def modul(self, jenisdak: str = "daknfpaud") -> bool:
        res = self._session.get(self._base_url + f"site/modul/jenisdak/{jenisdak}")
        if (
            res.ok
            and "RKAS" in res.text
            and "Laporan Penggunaan  Dana (SP)" in res.text
        ):
            self._logger.debug("Berhasil mendapatkan halaman DAK")
            return True
        self._logger.error("Gagal mendapatkan halaman DAK")
        return False

    def __del__(self):
        self.logout()
