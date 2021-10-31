import math

from lux.game_objects import Player as S_Player
from lux.game_objects import City as S_City
from lux.game_objects import Unit as S_Unit
from lux.game_objects import Cargo as S_Cargo
from lux.game_objects import CityTile as S_CityTile
from lux.game_map import Cell


class Player(S_Player):
    """
    Player Object

    [New Methods]: None
    """


class City(S_City):
    """
    City Object

    [New Methods]: None
    """


class Unit(S_Unit):
    """
    Unit Object

    [New Methods]: get_closest_tile
    """

    def get_closest_tile(self, tiles: list[Cell]) -> Cell:
        """Get the closest tile to the unit

        Args:
            tiles (list[Cell]): A list of tiles

        Returns:
            Cell: The closest tile
        """
        closest_dist = math.inf
        closest_tile = None
        for tile in tiles:
            dist = tile.pos.distance_to(self.pos)
            if dist < closest_dist:
                closest_dist = dist
                closest_tile = tile
        return closest_tile


class Cargo(S_Cargo):
    """
    Cargo Object

    [New Methods]: None
    """


class CityTile(S_CityTile):
    """
    CityTile Object

    [New Methods]: None
    """
