import numpy as np
import random
from Candidates import Candidates
from enum import Enum


class BorderTypes(Enum):
    NONE = 0
    SEAMLESS = 1

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


class Wave:
    def __init__(self, _number_of_tiles, _north_south_adjacency_matrix, _east_west_adjacency_matrix, _field_width,
                 _field_height, _border_type):
        if not ((_number_of_tiles,
                 _number_of_tiles) == _north_south_adjacency_matrix.shape == _north_south_adjacency_matrix.shape):
            raise Exception("_number_of_tiles and adjacency_matrices shap mismatch! num x num == shape")

        self.number_of_tiles = _number_of_tiles
        self.field_width = _field_width
        self.field_height = _field_height
        self.north_south_adjacency_matrix = _north_south_adjacency_matrix
        self.east_west_adjacency_matrix = _east_west_adjacency_matrix
        self.border_type = _border_type

        candidates = [i for i in range(_number_of_tiles)]

        self.candidate_field = np.array(
            [[Candidates(candidates, j, i) for i in range(_field_width)] for j in range(_field_height)],
            dtype=object)

        for i in range(_field_width * _field_height):
            self.collapse_once()

    def print_neighbor_matrices(self):
        print("--- NORTH - SOUTH ---")
        print(self.north_south_adjacency_matrix)
        print("--- ------------- ---")
        print("--- East - WEST ---")
        print(self.east_west_adjacency_matrix)
        print("--- ------------- ---")

    def print_field(self):
        print("--- Field ---")
        print(self.candidate_field)
        print("--- ------------- ---")

    def __get_a_rnd_lowest_cardinality__(self, set_of_candidates):
        min_val = len(np.amin(set_of_candidates))
        lowest = [x for x in set_of_candidates if len(x) == min_val]
        low = random.choice(lowest)
        return low

    def __get_non_final_cardinalities__(self):
        flattened = np.ravel(self.candidate_field)  # Flatten the matrix into a 1D array
        positives = [x for x in flattened if x.is_final == False]  # Filter positive values
        return positives

    def collapse_once(self):

        set_of_candidates = self.__get_non_final_cardinalities__()
        candidate = self.__get_a_rnd_lowest_cardinality__(set_of_candidates)
        candidate_index = candidate.get_index()
        final_candidate = candidate.get_random_candidate()

        if final_candidate == -1:
            return

        north_neighbors = self.north_south_adjacency_matrix.T[final_candidate]
        self.__update_neighbor(candidate_index, (-1, 0), north_neighbors)

        south_neighbors = self.north_south_adjacency_matrix[final_candidate]
        self.__update_neighbor(candidate_index, (1, 0), south_neighbors)

        east_neighbors = self.east_west_adjacency_matrix[final_candidate]
        self.__update_neighbor(candidate_index, (0, 1), east_neighbors)

        west_neighbors = self.east_west_adjacency_matrix.T[final_candidate]
        self.__update_neighbor(candidate_index, (0, -1), west_neighbors)

    def __update_neighbor(self, candidate_index, offset, neighbors):
        neighbor_index = candidate_index[0] + offset[0], candidate_index[1] + offset[1]

        if self.border_type == BorderTypes.NONE:
            if not self.__valid_neighbor_index__(neighbor_index):
                return
        elif self.border_type == BorderTypes.SEAMLESS:
            neighbor_index = self.__get_wrapped_neighbor_index__(neighbor_index)

        if self.candidate_field[neighbor_index].is_final:
            return

        neighbor_candidates = np.where(neighbors == True)
        self.candidate_field[neighbor_index].intersect_with(neighbor_candidates)

    def __get_wrapped_neighbor_index__(self, neighbor_index):
        row = neighbor_index[0]
        col = neighbor_index[1]

        if neighbor_index[0] < 0:
            row = self.field_height - 1
        if neighbor_index[0] >= self.field_height:
            row = 0
        if neighbor_index[1] < 0:
            col = self.field_width - 1
        if neighbor_index[1] >= self.field_width:
            col = 0

        return row, col

    def __valid_neighbor_index__(self, neighbor_index):
        if neighbor_index[0] < 0 or neighbor_index[0] >= self.field_height:
            return False
        if neighbor_index[1] < 0 or neighbor_index[1] >= self.field_width:
            return False
        return True

    def __str__(self):
        str_builder = "-" * self.field_width + "\n"

        for x in range(self.field_height):
            for y in range(self.field_width):
                str_builder += str(self.candidate_field[x, y])
            str_builder += "\n"

        str_builder += "-" * self.field_width + "\n"

        return str_builder

    def __str_cardinality__(self):
        str_builder = "===== cardinality field=====\n"
        str_builder += "-" * self.field_width + "\n"

        for x in range(self.field_width):
            for y in range(self.field_height):
                str_builder += self.candidate_field[x, y].__str_cardinality__()
            str_builder += "\n"

        str_builder += "-" * self.field_width + "\n"
        str_builder += "=========================\n"
        return str_builder
