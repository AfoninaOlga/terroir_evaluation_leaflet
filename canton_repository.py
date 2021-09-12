from typing import TypedDict, List

from db import query_db, write_db, get_db


class Variety(TypedDict):
    grape_id: int
    name: str
    avg_gst: float
    comment: str
    use_direction: str
    growth_power: str
    maturation_power: str
    berry_color: str
    frost_resistance: str
    disease_resistance: str
    origin: str


class Canton(TypedDict):
    name: str
    code: int
    density: float
    latitude: float
    clay: float
    silt: float
    sand: float
    organic_matter: float
    pH: float
    phosphorus: float
    potassium: float
    sodium: float
    calcium_exch: float
    total_carbonates: float
    p: float
    terroir_index: float
    station_id: int
    soil_texture: str


class WeatherData(TypedDict):
    station_id: int
    name: str
    annual_precipitation: float
    gst: float
    t_sum: float
    t_min: float
    t_max: float
    moisture_fact: float


def get_cantons(n: int = 211) -> List[Canton]:
    return query_db('SELECT * FROM Canton LIMIT ?', [n])


def get_canton_data(code: int) -> Canton:
    return query_db('SELECT name, terroir_index FROM Canton WHERE code = ?', [code])[0]


def get_weather_data(code: int) -> WeatherData:
    station_id = query_db('SELECT station_id FROM Canton WHERE code = ?', [code], one=True)['station_id']
    print(code, station_id)
    return query_db('SELECT * FROM MeteoStation WHERE station_id = ?', [station_id], one=True)


def get_grapes(n: int = 120) -> List[Variety]:
    return query_db('SELECT * FROM GrapeVariety LIMIT ?', [n])


def get_grape(code: int) -> List[Variety]:
    grapes = query_db('SELECT grape_id FROM CantonGrape WHERE canton_id = ?', [code])
    res = []
    for g in grapes:
        grape_id = g['grape_id']
        res.append(query_db('SELECT name, berry_color, disease_resistance, origin FROM GrapeVariety WHERE grape_id = ?', [grape_id])[0])
    return res


def get_filtered_cantons(filter: str, val: str):
    filters = ['berry_color', 'use-direction', 'disease_resistance']
    cantons = []
    if filter in filters:
        cantons = query_db(f'SELECT cg.canton_id, gv.name FROM CantonGrape as cg Join GrapeVariety as gv on cg.grape_id = gv.grape_id WHERE {filter} = ?', [val])
    return cantons

def get_cantons_by_grape(grape_id: int):
    return query_db('SELECT distinct canton_id FROM CantonGrape where grape_id = ?', [grape_id])