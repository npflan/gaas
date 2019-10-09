#from games.specs.nginx import NginxGameSpec
#from games.specs.csgo import CSGoGameSpec
#from games.specs.css import CSSGameSpec
from gaas.games.specs.factorio import FactorioGameSpec
from gaas.games.specs.csgo import CSGoGameSpec
from gaas.games.specs.modernwarfare import Cod4xGameSpec
from gaas.games.specs.modernwarfare2 import Cod4mw2GameSpec
from gaas.games.specs.teeworlds import TeeWorldsGameSpec


ENABLED_GAMES={
    #CSSGameSpec.id: CSSGameSpec(),
    CSGoGameSpec.id: CSGoGameSpec(),
    FactorioGameSpec.id: FactorioGameSpec(),
    Cod4xGameSpec.id: Cod4xGameSpec(),
    Cod4mw2GameSpec.id: Cod4mw2GameSpec(),
    TeeWorldsGameSpec.id: TeeWorldsGameSpec()
}

def get_enabled():
    return ENABLED_GAMES

def get_game_by_id(game_id):
    if game_id not in ENABLED_GAMES:
        raise Exception("GameID {} not found.".format(game_id))
    return ENABLED_GAMES[game_id]