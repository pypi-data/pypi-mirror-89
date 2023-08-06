from logging import getLogger
from requests import Session


class BaseSimdakPaud(object):
    _domain = "https://app.paud-dikmas.kemdikbud.go.id"
    _base_url = "https://app.paud-dikmas.kemdikbud.go.id/simdak/"
    _session = Session()
    _login = False
    _modul = False
    _logger = getLogger("SimdakPaud")

    @classmethod
    def is_online(cls) -> bool:
        res = cls._session.get(cls._base_url + "site/login")
        return res.ok
