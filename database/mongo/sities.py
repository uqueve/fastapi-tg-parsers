from parsers.models.cities import SiteModel


def get_actual_cities_json() -> dict[SiteModel, dict]:
    cities = {
        SiteModel.URALSK:
            {
                'city': SiteModel.URALSK,
                'channel_tg_id': -1001995705636,
                'ru': 'Уральск',
                'oid': '1',
                'language': 'русском',
                'local': 'Уральск',
            },
        SiteModel.EKATERINBURG:
            {
                'city': SiteModel.EKATERINBURG,
                'channel_tg_id': -1002036986287,
                'ru': 'Екатеринбург',
                'oid': '2',
                'language': 'русском',
                'local': 'Екатеринбург',
            },
        SiteModel.ALMATA:
            {
                'city': SiteModel.ALMATA,
                'channel_tg_id': -1001624097228,
                'ru': 'Алматы',
                'oid': '3',
                'language': 'русском',
                'local': 'Алматы',
            },
        SiteModel.TASHKENT:
            {
                'city': SiteModel.TASHKENT,
                'channel_tg_id': -1001943543947,
                'ru': 'Ташкент',
                'oid': '4',
                'language': 'русском',
                'local': 'Ташкент',
            },
        SiteModel.BAKU:
            {
                'city': SiteModel.BAKU,
                'channel_tg_id': -1001707288834,
                'ru': 'Баку',
                'oid': '5',
                'language': 'русском',
                'local': 'Баку',
            },
        SiteModel.TALLIN:
            {
                'city': SiteModel.TALLIN,
                'channel_tg_id': -1002009471060,
                'ru': 'Таллин',
                'oid': '6',
                'language': 'русском',
                'local': 'Таллин',
            },
        SiteModel.ASTRAHAN:
            {
                'city': SiteModel.ASTRAHAN,
                'channel_tg_id': -1002072612789,
                'ru': 'Астрахань',
                'oid': '7',
                'language': 'русском',
                'local': 'Астрахань',
            },
        SiteModel.CHITA:
            {
                'city': SiteModel.CHITA,
                'channel_tg_id': -1002029411001,
                'ru': 'Чита',
                'oid': '8',
                'language': 'русском',
                'local': 'Чита',
            },
        SiteModel.NOVOKUZNETSK:
            {
                'city': SiteModel.NOVOKUZNETSK,
                'channel_tg_id': -1001695780793,
                'ru': 'Новокузнецк',
                'oid': '9',
                'language': 'русском',
                'local': 'Новокузнецк',
            },
        SiteModel.ULANUDE:
            {
                'city': SiteModel.ULANUDE,
                'channel_tg_id': -1002117826746,
                'ru': 'Улан-Удэ',
                'oid': '10',
                'language': 'русском',
                'local': 'Улан-Удэ',
            },
        SiteModel.CHEREPOVEC:
            {
                'city': SiteModel.CHEREPOVEC,
                'channel_tg_id': -1002019398891,
                'ru': 'Череповец',
                'oid': '11',
                'language': 'русском',
                'local': 'Череповец',
            },
        SiteModel.VLADIVOSTOK:
            {
                'city': SiteModel.VLADIVOSTOK,
                'channel_tg_id': -1001987581011,
                'ru': 'Владивосток',
                'oid': '12',
                'language': 'русском',
                'local': 'Владивосток',
            },
        SiteModel.BRYANSK:
            {
                'city': SiteModel.BRYANSK,
                'channel_tg_id': -1001983540338,
                'ru': 'Брянск',
                'oid': '13',
                'language': 'русском',
                'local': 'Брянск',
            },
        SiteModel.KRASNODAR:
            {
                'city': SiteModel.KRASNODAR,
                'channel_tg_id': -1002044780327,
                'ru': 'Краснодар',
                'oid': '14',
                'language': 'русском',
                'local': 'Краснодар',
            },
        SiteModel.SURGUT:
            {
                'city': SiteModel.SURGUT,
                'channel_tg_id': -1002058813596,
                'ru': 'Сургут',
                'oid': '15',
                'language': 'русском',
                'local': 'Сургут',
            },
        SiteModel.STAVROPOL:
            {
                'city': SiteModel.STAVROPOL,
                'channel_tg_id': -1002127727187,
                'ru': 'Ставрополь',
                'oid': '16',
                'language': 'русском',
                'local': 'Ставрополь',
            },
        SiteModel.CHELYABINSK:
            {
                'city': SiteModel.CHELYABINSK,
                'channel_tg_id': -1002061678932,
                'ru': 'Челябинск',
                'oid': '17',
                'language': 'русском',
                'local': 'Челябинск',
            },
        SiteModel.SOROCHINSK:
            {
                'city': SiteModel.SOROCHINSK,
                'channel_tg_id': -1002011478896,
                'ru': 'Сорочинск',
                'oid': '18',
                'language': 'русском',
                'local': 'Сорочинск',
            },
        SiteModel.SMOLENSK:
            {
                'city': SiteModel.SMOLENSK,
                'channel_tg_id': -1002058539834,
                'ru': 'Смоленск',
                'oid': '19',
                'language': 'русском',
                'local': 'Смоленск',
            },
        SiteModel.TUMEN:
            {
                'city': SiteModel.TUMEN,
                'channel_tg_id': -1002001813291,
                'ru': 'Тюмень',
                'oid': '20',
                'language': 'русском',
                'local': 'Тюмень',
            },
        SiteModel.BELGOROD:
            {
                'city': SiteModel.BELGOROD,
                'channel_tg_id': -1002132123162,
                'ru': 'Белгород',
                'oid': '21',
                'language': 'русском',
                'local': 'Белгород',
            },
        SiteModel.IRKUTSK:
            {
                'city': SiteModel.IRKUTSK,
                'channel_tg_id': -1002121446881,
                'ru': 'Иркутск',
                'oid': '22',
                'language': 'русском',
                'local': 'Иркутск',
            },
        SiteModel.MAGADAN:
            {
                'city': SiteModel.MAGADAN,
                'channel_tg_id': -1002045273161,
                'ru': 'Магадан',
                'oid': '23',
                'language': 'русском',
                'local': 'Магадан',
            },
        SiteModel.MURMANSK:
            {
                'city': SiteModel.MURMANSK,
                'channel_tg_id': -1002030948880,
                'ru': 'Мурманск',
                'oid': '24',
                'language': 'русском',
                'local': 'Мурманск',
            },
        SiteModel.SAMARA:
            {
                'city': SiteModel.SAMARA,
                'channel_tg_id': -1002064479719,
                'ru': 'Самара',
                'oid': '25',
                'language': 'русском',
                'local': 'Самара',
            },
        SiteModel.MOSCOW:
            {
                'city': SiteModel.MOSCOW,
                'channel_tg_id': -1002090035064,
                'ru': 'Москва',
                'oid': '26',
                'language': 'русском',
                'local': 'Москва',
            },
        SiteModel.TBILISI:
            {
                'city': SiteModel.TBILISI,
                'channel_tg_id': -1002078240548,
                'ru': 'Тбилиси',
                'oid': '27',
                'language': 'русском',
                'local': 'Тбилиси',
            },
        SiteModel.NARIN:
            {
                'city': SiteModel.NARIN,
                'channel_tg_id': -1002094267711,
                'ru': 'Нарын',
                'oid': '28',
                'language': 'русском',
                'local': 'Нарын',
            },
        SiteModel.MAGNITOGORSK:
            {
                'city': SiteModel.MAGNITOGORSK,
                'channel_tg_id': -1002086098916,
                'ru': 'Магнитогорск',
                'oid': '29',
                'language': 'русском',
                'local': 'Магнитогорск',
            },
        SiteModel.VLADIMIR:
            {
                'city': SiteModel.VLADIMIR,
                'channel_tg_id': -1002116767076,
                'ru': 'Владимир',
                'oid': '30',
                'language': 'русском',
                'local': 'Владимир',
            },
        SiteModel.RIDDER:
            {
                'city': SiteModel.RIDDER,
                'channel_tg_id': -1002060939041,
                'ru': 'Риддер',
                'oid': '31',
                'language': 'русском',
                'local': 'Риддер',
            },
        SiteModel.AKSAI:
            {
                'city': SiteModel.AKSAI,
                'channel_tg_id': -1002070359135,
                'ru': 'Аксай',
                'oid': '32',
                'language': 'русском',
                'local': 'Аксай',
            },
        SiteModel.STEPNOGORSK:
            {
                'city': SiteModel.STEPNOGORSK,
                'channel_tg_id': -1002025346215,
                'ru': 'Степногорск',
                'oid': '33',
                'language': 'русском',
                'local': 'Степногорск',
            },
        SiteModel.VOLGOGRAD:
            {
                'city': SiteModel.VOLGOGRAD,
                'channel_tg_id': -1002120880397,
                'ru': 'Волгоград',
                'oid': '34',
                'language': 'русском',
                'local': 'Волгоград',
            },
        SiteModel.ARHANGELSK:
            {
                'city': SiteModel.ARHANGELSK,
                'channel_tg_id': -1001912470355,
                'ru': 'Архангельск',
                'oid': '35',
                'language': 'русском',
                'local': 'Архангельск',
            },
        SiteModel.OMSK:
            {
                'city': SiteModel.OMSK,
                'channel_tg_id': -1002099463612,
                'ru': 'Омск',
                'oid': '36',
                'language': 'русском',
                'local': 'Омск',
            },
        SiteModel.DNEPROPETROVSK:
            {
                'city': SiteModel.DNEPROPETROVSK,
                'channel_tg_id': -1002071216222,
                'ru': 'Днепропетровск',
                'oid': '37',
                'language': 'русском',
                'local': 'Днепропетровск',
            },
        SiteModel.KALININGRAD:
            {
                'city': SiteModel.KALININGRAD,
                'channel_tg_id': -1002107013442,
                'ru': 'Калининград',
                'oid': '38',
                'language': 'русском',
                'local': 'Калининград',
            },
        SiteModel.KARAKOL:
            {
                'city': SiteModel.KARAKOL,
                'channel_tg_id': -1002044608563,
                'ru': 'Каракол',
                'oid': '39',
                'language': 'русском',
                'local': 'Каракол',
            },
        SiteModel.KISHINEV:
            {
                'city': SiteModel.KISHINEV,
                'channel_tg_id': -1002034870476,
                'ru': 'Кишинёв',
                'oid': '40',
                'language': 'русском',
                'local': 'Кишинёв',
            },
        SiteModel.MINSK:
            {
                'city': SiteModel.MINSK,
                'channel_tg_id': -1002060953827,
                'ru': 'Минск',
                'oid': '41',
                'language': 'русском',
                'local': 'Минск',
            },
        SiteModel.SANKT_PETERBURG:
            {
                'city': SiteModel.SANKT_PETERBURG,
                'channel_tg_id': -1002068213593,
                'ru': 'Санкт-Петербург',
                'oid': '42',
                'language': 'русском',
                'local': 'Санкт-Петербург',
            },
        SiteModel.KIROV:
            {
                'city': SiteModel.KIROV,
                'channel_tg_id': -1002051972911,
                'ru': 'Киров',
                'oid': '43',
                'language': 'русском',
                'local': 'Киров',
            },
        SiteModel.KOSTANAI:
            {
                'city': SiteModel.KOSTANAI,
                'channel_tg_id': -1002136000742,
                'ru': 'Костанай',
                'oid': '44',
                'language': 'русском',
                'local': 'Костанай',
            },
        SiteModel.KRASNOYARSK:
            {
                'city': SiteModel.KRASNOYARSK,
                'channel_tg_id': -1002007063120,
                'ru': 'Красноярск',
                'oid': '45',
                'language': 'русском',
                'local': 'Красноярск',
            },
        SiteModel.TAGIL:
            {
                'city': SiteModel.TAGIL,
                'channel_tg_id': -1002059105127,
                'ru': 'Нижний Тагил',
                'oid': '46',
                'language': 'русском',
                'local': 'Нижний Тагил',
            },
        SiteModel.NOVOSIBIRSK:
            {
                'city': SiteModel.NOVOSIBIRSK,
                'channel_tg_id': -1002057469151,
                'ru': 'Новосибирск',
                'oid': '47',
                'language': 'русском',
                'local': 'Новосибирск',
            },
        SiteModel.PENZA:
            {
                'city': SiteModel.PENZA,
                'channel_tg_id': -1002004397348,
                'ru': 'Пенза',
                'oid': '48',
                'language': 'русском',
                'local': 'Пенза',
            },
        SiteModel.SAMARKAND:
            {
                'city': SiteModel.SAMARKAND,
                'channel_tg_id': -1001989200188,
                'ru': 'Самарканд',
                'oid': '49',
                'language': 'русском',
                'local': 'Самарканд',
            },
        SiteModel.SEVASTOPOL:
            {
                'city': SiteModel.SEVASTOPOL,
                'channel_tg_id': -1002065041883,
                'ru': 'Севастополь',
                'oid': '50',
                'language': 'русском',
                'local': 'Севастополь',
            },
        SiteModel.ASHHABAD:
            {
                'city': SiteModel.ASHHABAD,
                'channel_tg_id': -1002014851524,
                'ru': 'Ашхабад',
                'oid': '51',
                'language': 'русском',
                'local': 'Ашхабад',
            },
        SiteModel.BARANOVICHI:
            {
                'city': SiteModel.BARANOVICHI,
                'channel_tg_id': -1002111398446,
                'ru': 'Барановичи',
                'oid': '52',
                'language': 'русском',
                'local': 'Барановичи',
            },
        SiteModel.BREST:
            {
                'city': SiteModel.BREST,
                'channel_tg_id': -1002022929241,
                'ru': 'Брест',
                'oid': '53',
                'language': 'русском',
                'local': 'Брест',
            },
        SiteModel.KINESHMA:
            {
                'city': SiteModel.KINESHMA,
                'channel_tg_id': -1002072172563,
                'ru': 'Кинешма',
                'oid': '54',
                'language': 'русском',
                'local': 'Кинешма',
            },
        SiteModel.SHIMKENT:
            {
                'city': SiteModel.SHIMKENT,
                'channel_tg_id': -1002069112345,
                'ru': 'Шымкент',
                'oid': '55',
                'language': 'русском',
                'local': 'Шымкент',
            },
        SiteModel.ORENBURG:
            {
                'city': SiteModel.ORENBURG,
                'channel_tg_id': -1002005081975,
                'ru': 'Оренбург',
                'oid': '56',
                'language': 'русском',
                'local': 'Оренбург',
            },
        SiteModel.PETROPAVLOVSK:
            {
                'city': SiteModel.PETROPAVLOVSK,
                'channel_tg_id': -1002129099014,
                'ru': 'Петропавловск',
                'oid': '57',
                'language': 'русском',
                'local': 'Петропавловск',
            },
        SiteModel.USTKAMENOGORSK:
            {
                'city': SiteModel.USTKAMENOGORSK,
                'channel_tg_id': -1001999350799,
                'ru': 'Усть-Каменогорск',
                'oid': '58',
                'language': 'русском',
                'local': 'Усть-Каменогорск',
            },
        SiteModel.KARAGANDA:
            {
                'city': SiteModel.KARAGANDA,
                'channel_tg_id': -1002052374403,
                'ru': 'Караганда',
                'oid': '59',
                'language': 'русском',
                'local': 'Караганда',
            },
        SiteModel.TOLIATTI:
            {
                'city': SiteModel.TOLIATTI,
                'channel_tg_id': -1002045629913,
                'ru': 'Тольятти',
                'oid': '60',
                'language': 'русском',
                'local': 'Тольятти',
            },
        SiteModel.KUTAISI:
            {
                'city': SiteModel.KUTAISI,
                'channel_tg_id': -1001526305925,
                'ru': 'Кутаиси',
                'oid': '61',
                'language': 'русском',
                'local': 'Кутаиси',
            },
        SiteModel.ZASTAPHONI:
            {
                'city': SiteModel.ZASTAPHONI,
                'channel_tg_id': -1001994173618,
                'ru': 'Зестафони',
                'oid': '62',
                'language': 'русском',
                'local': 'Зестафони',
            },
        SiteModel.HIMKI:
            {
                'city': SiteModel.HIMKI,
                'channel_tg_id': -1002121400515,
                'ru': 'Химки',
                'oid': '63',
                'language': 'русском',
                'local': 'Химки',
            },
        SiteModel.DUSHANBE:
            {
                'city': SiteModel.DUSHANBE,
                'channel_tg_id': -1002053011562,
                'ru': 'Душанбе',
                'oid': '64',
                'language': 'русском',
                'local': 'Душанбе',
            },
        SiteModel.BISHKEK:
            {
                'city': SiteModel.BISHKEK,
                'channel_tg_id': -1002093343420,
                'ru': 'Бишкек',
                'oid': '65',
                'language': 'русском',
                'local': 'Бишкек',
            },
        SiteModel.SUHUMI:
            {
                'city': SiteModel.SUHUMI,
                'channel_tg_id': -1002143147410,
                'ru': 'Сухуми',
                'oid': '66',
                'language': 'русском',
                'local': 'Сухуми',
            },
        SiteModel.PERM:
            {
                'city': SiteModel.PERM,
                'channel_tg_id': -1001990935303,
                'ru': 'Пермь',
                'oid': '67',
                'language': 'русском',
                'local': 'Пермь',
            },
        SiteModel.TULA:
            {
                'city': SiteModel.TULA,
                'channel_tg_id': -1001624232118,
                'ru': 'Тула',
                'oid': '68',
                'language': 'русском',
                'local': 'Тула',
            },
        SiteModel.KRIM:
            {
                'city': SiteModel.KRIM,
                'channel_tg_id': -1001999891572,
                'ru': 'Крым',
                'oid': '69',
                'language': 'русском',
                'local': 'Крым',
            },
        SiteModel.VORONEZH:
            {
                'city': SiteModel.VORONEZH,
                'channel_tg_id': -1002127016987,
                'ru': 'Воронеж',
                'oid': '70',
                'language': 'русском',
                'local': 'Воронеж',
            },
        SiteModel.MAHACHKALA:
            {
                'city': SiteModel.MAHACHKALA,
                'channel_tg_id': -1002030954902,
                'ru': 'Махачкала',
                'oid': '71',
                'language': 'русском',
                'local': 'Махачкала',
            },
        SiteModel.YALTA:
            {
                'city': SiteModel.YALTA,
                'channel_tg_id': -1002072851668,
                'ru': 'Ялта',
                'oid': '72',
                'language': 'русском',
                'local': 'Ялта',
            },
        SiteModel.IVANOVO:
            {
                'city': SiteModel.IVANOVO,
                'channel_tg_id': -1002122001843,
                'ru': 'Иваново',
                'oid': '73',
                'language': 'русском',
                'local': 'Иваново',
            },
        SiteModel.TVER:
            {
                'city': SiteModel.TVER,
                'channel_tg_id': -1002010141052,
                'ru': 'Тверь',
                'oid': '74',
                'language': 'русском',
                'local': 'Тверь',
            },
        SiteModel.UFA:
            {
                'city': SiteModel.UFA,
                'channel_tg_id': -1002002926426,
                'ru': 'Уфа',
                'oid': '75',
                'language': 'русском',
                'local': 'Уфа',
            },
        SiteModel.BELU:
            {
                'city': SiteModel.BELU,
                'channel_tg_id': -1002122489783,
                'ru': 'Белу-Оризонти',
                'oid': '76',
                'language': 'португальском',
                'local': 'Belo Horizonte',
            },
        SiteModel.KAMPINAS:
            {
                'city': SiteModel.KAMPINAS,
                'channel_tg_id': -1002132116187,
                'ru': 'Кампинас',
                'oid': '77',
                'language': 'португальском',
                'local': 'Campinas',
            },
        SiteModel.DUKI:
            {
                'city': SiteModel.DUKI,
                'channel_tg_id': -1002016066715,
                'ru': 'Дуки-ди-Кашиас',
                'oid': '78',
                'language': 'португальском',
                'local': 'Duque de Caxias',
            },
        SiteModel.FORTALEZA:
            {
                'city': SiteModel.FORTALEZA,
                'channel_tg_id': -1002070930646,
                'ru': 'Форталеза',
                'oid': '79',
                'language': 'португальском',
                'local': 'Fortaleza',
            },
        SiteModel.GUARULUS:
            {
                'city': SiteModel.GUARULUS,
                'channel_tg_id': -1002123451225,
                'ru': 'Гуарульюс',
                'oid': '80',
                'language': 'португальском',
                'local': 'Guarulhos',
            },
        SiteModel.KAMPU:
            {
                'city': SiteModel.KAMPU,
                'channel_tg_id': -1002131340260,
                'ru': 'Кампу-Гранди',
                'oid': '81',
                'language': 'португальском',
                'local': 'Campo Grande',
            },
        SiteModel.KURITTIBA:
            {
                'city': SiteModel.KURITTIBA,
                'channel_tg_id': -1002118097967,
                'ru': 'Куритиба',
                'oid': '82',
                'language': 'португальском',
                'local': 'Curitiba',
            },
        SiteModel.RIO:
            {
                'city': SiteModel.RIO,
                'channel_tg_id': -1002117542756,
                'ru': 'Рио-де-Жанейро',
                'oid': '83',
                'language': 'португальском',
                'local': 'Rio de Janeiro',
            },
        SiteModel.SALVADOR:
            {
                'city': SiteModel.SALVADOR,
                'channel_tg_id': -1002040202223,
                'ru': 'Салвадор',
                'oid': '84',
                'language': 'португальском',
                'local': 'Salvador',
            },
        SiteModel.SANGONSALU:
            {
                'city': SiteModel.SANGONSALU,
                'channel_tg_id': -1002011356956,
                'ru': 'Сан-Гонсалу',
                'oid': '85',
                'language': 'португальском',
                'local': 'Sao Goncalo',
            },
        SiteModel.SANLUIS:
            {
                'city': SiteModel.SANLUIS,
                'channel_tg_id': -1002007196820,
                'ru': 'Сан-Луис',
                'oid': '86',
                'language': 'португальском',
                'local': 'San Luis',
            },
        SiteModel.SANPAULU:
            {
                'city': SiteModel.SANPAULU,
                'channel_tg_id': -1002082297035,
                'ru': 'Сан-Паулу',
                'oid': '87',
                'language': 'португальском',
                'local': 'Sao PaoloСан-Паулу',
            },
    }
    return cities
