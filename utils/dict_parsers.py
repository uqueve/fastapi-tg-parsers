from parsers.gazeta_tashkent import GazetaTashkentParser
from parsers.inalmaty_almata import InalmatyAlmataParser
from parsers.mgorod_uralsk import MgorodUralskParser
from parsers.report_baku import ReportBakuParser
from parsers.uralweb_ekat import UralwebEkatParser
from utils.models import SiteModel


get_parser_object = {
    SiteModel.URALSK: MgorodUralskParser(),
    SiteModel.EKATERINBURG: UralwebEkatParser(),
    SiteModel.ALMATA: InalmatyAlmataParser(),
    SiteModel.TASHKENT: GazetaTashkentParser(),
    SiteModel.BAKU: ReportBakuParser()
}
