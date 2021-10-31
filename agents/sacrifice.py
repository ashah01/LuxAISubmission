import math, sys
from lux import game
from lux.game import Game
from lux.game_map import Cell, RESOURCE_TYPES
from lux.constants import Constants
from lux.game_constants import GAME_CONSTANTS
from lux import annotate

DIRECTIONS = Constants.DIRECTIONS
game_state = None


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
            elif cell.has_resource():
                resource_tiles.append(cell)

    # unit actions
    for unit in player.units:
        if unit.can_act():
            # if unit does not have 100 wood, then then move towards a wood tile
            if unit.get_cargo_space_left() > 0:
                proximal_tile = unit.get_closest_tile(resource_tiles)
                if proximal_tile:
                    actions.append(unit.move_to_tile(proximal_tile))
            elif (
                unit.can_build(game_state.map)
                and not game_state.map.get_cell_by_pos(unit.pos).citytile
            ):
                actions.append(unit.build_city())
            elif not unit.can_build(game_state.map):
                proximal_tile = unit.get_closest_tile(empty_tiles)
                if proximal_tile:
                    actions.append(unit.move_to_tile(proximal_tile))

            # if unit is on an empty tile (w/o a city or a resource tile), then create a city
            # else find shortest path to tile that is empty and then move in that direction

    # citytile actions
    # for k, city in player.cities.items():
    #     for citytile in city.citytiles:
    #         if citytile.can_act():
    #             actions.append(citytile.build_worker())

    return actions
