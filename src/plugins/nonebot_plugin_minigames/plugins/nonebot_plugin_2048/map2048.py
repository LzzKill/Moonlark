#  Moonlark - A new ChatBot
#  Copyright (C) 2024  Moonlark Development Team
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ##############################################################################
import copy
import random

from src.plugins.nonebot_plugin_finding_the_trail.utils.enums import Directions
from src.plugins.nonebot_plugin_minigames.plugins.nonebot_plugin_2048.image import draw_map


class Map2048:

    def __init__(self) -> None:
        self.map = [[0 for _ in range(4)] for _ in range(4)]
        self.score = 0
        self.put_number()

    def add_craft_score(self, number: int) -> bool:
        self.score += number * 7
        if number == 2048:
            self.score *= 3
        elif number == 4096:
            self.score *= 5
            return True
        else:
            return False

    def draw(self) -> bytes:
        return draw_map(self.map)

    def put_number(self, number: int = 2) -> None:
        free_pos = []
        for row in range(len(self.map)):
            for col in range(len(self.map[row])):
                if self.map[row][col] == 0:
                    free_pos.append((row, col))
        if not free_pos:
            raise ValueError("地图已满")
        target_pos = random.choice(free_pos)
        self.map[target_pos[0]][target_pos[1]] = number

    def move_up(self) -> None:
        for row in range(1, len(self.map)):
            for col in range(len(self.map[row])):
                while row > 0:
                    num = self.map[row][col]
                    if (origin := self.map[row - 1][col]) in [0, num]:
                        self.map[row - 1][col] += num
                        self.map[row][col] = 0
                        if origin == num:
                            if self.add_craft_score(num):
                                self.map[row - 1][col] = 0
                            break
                        row -= 1

    def move_down(self) -> None:
        for row in range(1, len(self.map)):
            row = len(self.map) - row
            for col in range(len(self.map[row])):
                while row < 4:
                    num = self.map[row][col]
                    if (origin := self.map[row + 1][col]) in [0, num]:
                        self.map[row + 1][col] += num
                        self.map[row][col] = 0
                        if origin == num:
                            if self.add_craft_score(num):
                                self.map[row - 1][col] = 0
                            break
                        row += 1

    def move_left(self) -> None:
        for row in range(len(self.map)):
            for col in range(1, len(self.map[row])):
                while col > 0:
                    num = self.map[row][col]
                    if (origin := self.map[row][col - 1]) in [0, num]:
                        self.map[row][col - 1] += num
                        self.map[row][col] = 0
                        if origin == num:
                            if self.add_craft_score(num):
                                self.map[row - 1][col] = 0
                            break
                        col -= 1

    def move_right(self) -> None:
        for row in range(len(self.map)):
            for col in range(len(self.map[row])):
                col = len(self.map[row]) - col
                while col < 4:
                    num = self.map[row][col]
                    if (origin := self.map[row][col + 1]) in [0, num]:
                        self.map[row][col + 1] += num
                        self.map[row][col] = 0
                        if origin == num:
                            if self.add_craft_score(num):
                                self.map[row - 1][col] = 0
                            break
                        col += 1

    def get_score(self) -> int:
        return self.score

    def move(self, direction: Directions) -> bool:
        origin = copy.deepcopy(self.map)
        match direction:
            case Directions.UP:
                self.move_up()
            case Directions.DOWN:
                self.move_down()
            case Directions.LEFT:
                self.move_left()
            case Directions.RIGHT:
                self.move_right()
        return not self.map == origin
