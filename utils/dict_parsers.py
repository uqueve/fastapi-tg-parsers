from parsers.aksai import AksaiParser
from parsers.almata import AlmataParser
from parsers.arhangelsk import ArhangelskParser
from parsers.astrahan import AstrahanParser
from parsers.belgorod import BelgorodParser
from parsers.bryansk import BryanskParser
from parsers.chelyabinsk import ChelyabinskParser
from parsers.cherepovec import CherepovecParser
from parsers.chita import ChitaParser
from parsers.dnepropetrovsk import DnepropetrovskParser
from parsers.gazeta_tashkent import TashkentParser
from parsers.irkutsk import IrkutskParser
from parsers.kaliningrad import KaliningradParser
from parsers.karakol import KarakolParser
from parsers.kishinev import KishenevParser
from parsers.krasnodar import KrasnodarParser
from parsers.magadan import MagadanParser
from parsers.magnitogorsk import MagnitogorskParser
from parsers.minsk import MinskParser
from parsers.models.base import BaseParser
from parsers.moscow import MoscowParser
from parsers.murmansk import MurmanskParser
from parsers.narin import NarinParser
from parsers.novokuznetsk import NovokuznetskParser
from parsers.omsk import OmskParser
from parsers.report_baku import ReportBakuParser
from parsers.ridder import RidderParser
from parsers.samara import SamaraParser
from parsers.sankt_piter import SanktPiterParser
from parsers.smolensk import SmolenskParser
from parsers.sorochinsk import SorochinskParser
from parsers.stavropol import StavropolParser
from parsers.stepnogorsk import StepnogorskParser
from parsers.surgut import SurgutParser
from parsers.tallin_tallin import TallinTallinParser
from parsers.tbilisi import TbilisiParser
from parsers.tumen import TumenParser
from parsers.ulanude import UlanUdeParser
from parsers.uralsk import UralskParser
from parsers.uralweb_ekat import UralwebEkatParser
from parsers.vladimir import VladimirParser
from parsers.vladivostok import VladivostokParser
from parsers.volgograd import VolgogradParser
from parsers.ashhabad import AshhabadParser
from parsers.baranovichi import BaranovichiParser
from parsers.brest import BrestParser
from parsers.kineshma import KineshmaParser
from parsers.orenburg import OrenburgParser
from parsers.shimkent import ShimkentParser
from utils.models import SiteModel


def get_parser_objects() -> dict[SiteModel, BaseParser]:
    get_parser_object = {
        SiteModel.ASHHABAD: AshhabadParser(),
        SiteModel.BARANOVICHI: BaranovichiParser(),
        SiteModel.BREST: BrestParser(),
        SiteModel.KINESHMA: KineshmaParser(),
        SiteModel.ORENBURG: OrenburgParser(),
        SiteModel.SHIMKENT: ShimkentParser(),
        SiteModel.DNEPROPETROVSK: DnepropetrovskParser(),
        SiteModel.KARAKOL: KarakolParser(),
        SiteModel.KALININGRAD: KaliningradParser(),
        SiteModel.MINSK: MinskParser(),
        SiteModel.OMSK: OmskParser(),
        SiteModel.SANKT_PETERBURG: SanktPiterParser(),
        SiteModel.KISHINEV: KishenevParser(),
        SiteModel.MOSCOW: MoscowParser(),
        SiteModel.TBILISI: TbilisiParser(),
        SiteModel.NARIN: NarinParser(),
        SiteModel.MAGNITOGORSK: MagnitogorskParser(),
        SiteModel.VLADIMIR: VladimirParser(),
        SiteModel.RIDDER: RidderParser(),
        SiteModel.AKSAI: AksaiParser(),
        SiteModel.STEPNOGORSK: StepnogorskParser(),
        SiteModel.VOLGOGRAD: VolgogradParser(),
        SiteModel.ARHANGELSK: ArhangelskParser(),
        SiteModel.ALMATA: AlmataParser(),
        SiteModel.ASTRAHAN: AstrahanParser(),
        SiteModel.BELGOROD: BelgorodParser(),
        SiteModel.BRYANSK: BryanskParser(),
        SiteModel.CHELYABINSK: ChelyabinskParser(),
        SiteModel.CHEREPOVEC: CherepovecParser(),
        SiteModel.CHITA: ChitaParser(),
        SiteModel.TASHKENT: TashkentParser(),
        SiteModel.IRKUTSK: IrkutskParser(),
        SiteModel.KRASNODAR: KrasnodarParser(),
        SiteModel.MAGADAN: MagadanParser(),
        SiteModel.MURMANSK: MurmanskParser(),
        SiteModel.NOVOKUZNETSK: NovokuznetskParser(),
        SiteModel.BAKU: ReportBakuParser(),
        SiteModel.SAMARA: SamaraParser(),
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
    return get_parser_object
