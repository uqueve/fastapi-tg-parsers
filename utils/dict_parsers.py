from utils.models import SiteModel

from parsers.almata import AlmataParser
from parsers.astrahan import AstrahanParser
from parsers.bryansk import BryanskParser
from parsers.chelyabinsk import ChelyabinskParser
from parsers.cherepovec import CherepovecParser
from parsers.chita import ChitaParser
from parsers.gazeta_tashkent import TashkentParser
from parsers.krasnodar import KrasnodarParser
from parsers.novokuznetsk import NovokuznetskParser
from parsers.report_baku import ReportBakuParser
from parsers.smolensk import SmolenskParser
from parsers.sorochinsk import SorochinskParser
from parsers.stavropol import StavropolParser
from parsers.surgut import SurgutParser
from parsers.tallin_tallin import TallinTallinParser
from parsers.tumen import TumenParser
from parsers.ulanude import UlanUdeParser
from parsers.uralsk import UralskParser
from parsers.uralweb_ekat import UralwebEkatParser
from parsers.vladivostok import VladivostokParser


get_parser_object = {
    SiteModel.ALMATA: AlmataParser(),
    SiteModel.ASTRAHAN: AstrahanParser(),
    SiteModel.BRYANSK: BryanskParser(),
    SiteModel.CHELYABINSK: ChelyabinskParser(),
    SiteModel.CHEREPOVEC: CherepovecParser(),
    SiteModel.CHITA: ChitaParser(),
    SiteModel.TASHKENT: TashkentParser(),
    SiteModel.KRASNODAR: KrasnodarParser(),
    SiteModel.NOVOKUZNETSK: NovokuznetskParser(),
    SiteModel.BAKU: ReportBakuParser(),
    SiteModel.SMOLENSK: SmolenskParser(),
    SiteModel.SOROCHINSK: SorochinskParser(),
    SiteModel.STAVROPOL: StavropolParser(),
    SiteModel.SURGUT: SurgutParser(),
    SiteModel.TALLIN: TallinTallinParser(),
    SiteModel.TUMEN: TumenParser(),
    SiteModel.ULANUDE: UlanUdeParser(),
    SiteModel.URALSK: UralskParser(),
    SiteModel.EKATERINBURG: UralwebEkatParser(),
    SiteModel.VLADIVOSTOK: VladivostokParser(),
}
