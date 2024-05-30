from dataclasses import dataclass
from enum import unique, StrEnum, auto


@unique
class SiteModel(StrEnum):
    ALMATA = auto()
    ASTRAHAN = auto()
    BELGOROD = auto()
    BRYANSK = auto()
    CHELYABINSK = auto()
    CHEREPOVEC = auto()
    CHITA = auto()
    TASHKENT = auto()
    IRKUTSK = auto()
    KRASNODAR = auto()
    MAGADAN = auto()
    MOSCOW = auto()
    TBILISI = auto()
    NARIN = auto()
    MAGNITOGORSK = auto()
    VLADIMIR = auto()
    RIDDER = auto()
    AKSAI = auto()
    STEPNOGORSK = auto()
    VOLGOGRAD = auto()
    ARHANGELSK = auto()
    MURMANSK = auto()
    NOVOKUZNETSK = auto()
    BAKU = auto()
    SAMARA = auto()
    SMOLENSK = auto()
    SOROCHINSK = auto()
    STAVROPOL = auto()
    SURGUT = auto()
    TALLIN = auto()
    TUMEN = auto()
    ULANUDE = auto()
    URALSK = auto()
    EKATERINBURG = auto()
    VLADIVOSTOK = auto()
    DNEPROPETROVSK = auto()
    KALININGRAD = auto()
    KARAKOL = auto()
    KISHINEV = auto()
    MINSK = auto()
    OMSK = auto()
    SANKT_PETERBURG = auto()
    NOVOSIBIRSK = auto()
    SAMARKAND = auto()
    KRASNOYARSK = auto()
    SEVASTOPOL = auto()
    KOSTANAI = auto()
    PENZA = auto()
    KIROV = auto()
    TAGIL = auto()

    ASHHABAD = auto()
    KINESHMA = auto()
    BREST = auto()
    BARANOVICHI = auto()
    SHIMKENT = auto()
    ORENBURG = auto()

    PETROPAVLOVSK = auto()
    USTKAMENOGORSK = auto()
    KARAGANDA = auto()


@dataclass
class CitySchema:
    oid: str
    name: str
    ru: str

    def to_dict(self) -> dict:
        return {'oid': self.oid, 'name': self.name, 'ru': self.ru}