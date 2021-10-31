import math, sys
from lux.game import Game
from lux.game_map import Cell, RESOURCE_TYPES
from lux.constants import Constants
from lux.game_constants import GAME_CONSTANTS
from custom.game_objects import Unit
from lux import annotate

DIRECTIONS = Constants.DIRECTIONS
game_state = None


def get_closest_tile(tiles: list[Cell], unit: Unit):
    closest_dist = math.inf
    closest_tile = None
    for tile in tiles:
        dist = tile.pos.distance_to(unit.pos)
        if dist < closest_dist:
            closest_dist = dist
            closest_tile = tile
    return closest_tile


def agent(observation, configuration):
    global game_state

    ### Do not edit ###
    if observation["step"] == 0:
        game_state = Game()
        game_state._initialize(observation["updates"])
        game_state._update(observation["updates"][2:])
        game_state.id = observation.player
    else:
        game_state._update(observation["updates"])

    actions = []

    ### AI Code goes down here! ###
    player = game_state.players[observation.player]
    opponent = game_state.players[(observation.player + 1) % 2]
    width, height = game_state.map.width, game_state.map.height

    empty_tiles: list[Cell] = []
    resource_tiles: list[Cell] = []
    for y in range(height):
        for x in range(width):
            cell = game_state.map.get_cell(x, y)
            if not (cell.has_resource() or cell.citytile):
                empty_tiles.append(cell)
            if cell.has_resource():
                resource_tiles.append(cell)

    # unit actions
    for unit in player.units:
        if unit.can_act():
            if unit.get_cargo_space_left() > 0:

                proximal_tile = get_closest_tile(resource_tiles, unit)
                if proximal_tile:
                    move_dir = unit.pos.direction_to(proximal_tile.pos)
                    actions.append(unit.move(move_dir))
            else:
                pass

            # if unit does not have 100 wood, then:
            # if unit is not adjacent to a wood tile, move towards it
            # else get resources from wood tile.
            # if unit is on an empty tile (w/o a city or a resource tile), then create a city
            # else find shortest path to tile that is empty and then move in that direction

    # citytile actions

    return actions
