import json
from pathlib import Path

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


class BarangInput(BaseModel):
    nama: str = Field(min_length=1)
    kategori: str = Field(min_length=1)
    jumlah_stok: int = Field(ge=0, strict=True)
    lokasi_gudang: str = Field(min_length=1)


class Barang(BarangInput):
    id: int


app = FastAPI(title="Inventaris Klinik Bedah Plastik Estetika", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://127.0.0.1:5174"],
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)

seed_path = Path(__file__).with_name("seed_barang.json")
barang_db = [Barang.model_validate(item) for item in json.loads(seed_path.read_text(encoding="utf-8"))]


@app.get("/barang", response_model=list[Barang])
def baca_barang():
    return barang_db


@app.post("/barang", response_model=Barang, status_code=status.HTTP_201_CREATED)
def tambah_barang(data: BarangInput):
    id_baru = max((item.id for item in barang_db), default=0) + 1
    barang = Barang(id=id_baru, **data.model_dump())
    barang_db.append(barang)
    return barang


@app.delete("/barang/{barang_id}", status_code=status.HTTP_204_NO_CONTENT)
def hapus_barang(barang_id: int):
    for index, barang in enumerate(barang_db):
        if barang.id == barang_id:
            barang_db.pop(index)
            return
    raise HTTPException(status_code=404, detail="Barang tidak ditemukan")
