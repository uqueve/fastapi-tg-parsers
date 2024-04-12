from parsers.gazeta_tashkent import GazetaTashkentParser
# from parsers.inalmaty_almata import InalmatyAlmataParser
from parsers.almata import AlmataParser
from parsers.mgorod_uralsk import MgorodUralskParser
from parsers.uralsk import UralskParser
from parsers.report_baku import ReportBakuParser
# from parsers.uralweb_ekat import UralwebEkatParser
from parsers.astrahan import AstrahanParser
from parsers.novokuznetsk import NovokuznetskParser
from parsers.ulanude import UlanUdeParser
from parsers.tallin_tallin import TallinTallinParser
from parsers.chita import ChitaParser
from parsers.cherepovec import CherepovecParser
from parsers.stavropol import StavropolParser
from utils.models import SiteModel


get_parser_object = {
    SiteModel.URALSK: MgorodUralskParser(),
    SiteModel.EKATERINBURG: UralskParser(),
    SiteModel.ALMATA: AlmataParser(),
    SiteModel.TASHKENT: GazetaTashkentParser(),
    SiteModel.BAKU: ReportBakuParser(),
    SiteModel.ASTRAHAN: AstrahanParser(),
    SiteModel.CHITA: ChitaParser(),
    SiteModel.NOVOKUZNETSK: NovokuznetskParser(),
    SiteModel.TALLIN: TallinTallinParser(),
    SiteModel.ULANUDE: UlanUdeParser(),
    SiteModel.CHEREPOVEC: CherepovecParser(),
    # SiteModel.STAVROPOL: StavropolParser(),
}
