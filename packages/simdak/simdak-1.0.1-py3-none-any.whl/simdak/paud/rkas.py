from __future__ import annotations
from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass
from typing import List, Optional, Type
from simdak.exception import DataKosongException
from . import BaseSimdakPaud, Rab


@dataclass
class Rkas(BaseSimdakPaud):
    no: str
    npsn: str
    satuan_pendidikan: str
    alamat: str
    alokasi: str
    kegiatan_pembelajaran_dan_bermain: str
    kegiatan_pendukung: str
    kegiatan_lainnya: str
    jumlah: str
    url: str
    semester_id: int = 20201
    id: str = ""

    def __post_init__(self) -> None:
        url = self.url
        if "=" in url:
            self.id = url.split("&")[1].split("=")[-1]
        else:
            urls = url.split("/")
            self.id = urls[-3]
            if urls[-1].isdigit():
                self.semester_id = int(urls[-1])
        self._logger.info(f"RKAS ({self.id}) berhasil dibuka")

    def __call__(self, semester_id: int = 20201, save_as: Type[Rab] = Rab) -> List[Rab]:
        return self.get(semester_id, save_as)

    def get(self, semester_id: int = 20201, save_as: Type[Rab] = Rab) -> List[Rab]:
        results: List[Rab] = []
        semester = semester_id or self.semester_id
        url = self._base_url + f"boppaudrkas/create/id/{self.id}/semester_id/{semester}"
        res = self._session.get(url)
        if not res.ok:
            return results
        soup = BeautifulSoup(res.text, "html.parser")
        table: List[Tag] = soup.findAll("table")
        if not table or len(table) != 2:
            raise DataKosongException(
                f"Data tidak ditemukan untuk rkas [{self.id}] semester [{semester}]"
            )
        results = save_as.from_table(table[1])
        return results

    def create(self, rkas_data: Rab, semester_id: int = 20201) -> Optional[Rab]:
        data = rkas_data.as_data()
        data.update({"yt0": "Simpan"})
        semester = semester_id or self.semester_id
        url = self._base_url + f"boppaudrkas/create/id/{self.id}/semester_id/{semester}"
        res = self._session.post(url, data=data)
        if not res.ok:
            return None
        soup = BeautifulSoup(res.text, "html.parser")
        table: List[Tag] = soup.findAll("table")
        if not table or len(table) != 2:
            raise DataKosongException(
                f"Data tidak ditemukan untuk rkas [{self.id}] semester [{semester}]"
            )
        tr: Tag = table[-1].findAll("tr")[-1]
        return Rab.from_tr(tr)
