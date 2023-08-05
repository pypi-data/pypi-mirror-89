from __future__ import annotations
from requests import Session
from logging import getLogger
from . import BaseSimdakPaud, SimdakRkasPaud
from simdak.config import HEADERS


class SimdakPaud(BaseSimdakPaud):
    def __init__(self, email: str, password: str):
        self._logger = getLogger(self.__class__.__name__)
        self._email = email
        self._password = password
        self._session.headers.update(HEADERS)
        self._login = self.login()
        self._modul = self.modul()
        self.rkas = SimdakRkasPaud()

    def login(self) -> bool:
        if self._login:
            raise PermissionError("Anda sudah login.")
        url = self._base_url + "site/login"
        res = self._session.get(url)
        if not res.status_code == 200:
            raise Exception("Error! tidak dapat menghubungi website simdak")
        data = {
            "LoginForm[username]": self._email,
            "LoginForm[password]": self._password,
            "LoginForm[rememberMe]": ["0", "1"],
            "yt0": "Masuk",
        }
        res = self._session.post(url, data)
        if res.ok and "DAK NON FISIK" in res.text:
            self._logger.debug(f"Berhasil login dengan {self._email}.")
            return True
        self._logger.error(f"Gagal login dengan {self._email}.")
        return False

    def logout(self) -> bool:
        res = self._session.get(self._base_url + "site/logout")
        self._logger.debug(f"Berhasil keluar dari akun {self._email}")
        return res.ok

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
