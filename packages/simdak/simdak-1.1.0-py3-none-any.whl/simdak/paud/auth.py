from . import BaseSimdakPaud


class SimdakPaudAuth(BaseSimdakPaud):
    def login(
        self,
        email: str = None,
        password: str = None,
        remember: bool = False,
    ) -> bool:
        if self._login:
            raise PermissionError("Anda sudah login.")
        url = self._base_url + "site/login"
        res = self._session.get(url)
        if res.status_code != 200:
            raise Exception("Error! tidak dapat menghubungi website simdak")
        data = {
            "LoginForm[username]": email or self._email,
            "LoginForm[password]": password or self._password,
            "LoginForm[rememberMe]": "1" if remember else "0",
            "yt0": "Masuk",
        }
        headers = {"Referer": url}
        res = self._session.post(url, data, headers=headers)
        if res.url == self._base_url + 'site/modul':
            self._logger.debug(f"Berhasil login dengan {self._email}.")
            return True
        self._logger.error(f"Gagal login dengan {self._email}.")
        return False

    def logout(self) -> bool:
        res = self._session.get(self._base_url + "site/logout")
        self._logger.debug(f"Berhasil keluar dari akun {self._email}")
        return res.ok
