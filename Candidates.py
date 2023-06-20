import random

import numpy as np

class Candidates:
    def __init__(self, _candidates, _pos_x, _pos_y):
        self.candidates = _candidates
        self.pos_x = _pos_x
        self.pos_y = _pos_y
        self.cardinality = len(_candidates)
        self.is_final = self.cardinality == 1


    def __update_values__(self, new_candidates):
        self.candidates = new_candidates
        self.cardinality = len(new_candidates)


    def intersect_with(self, others):
        intersection = np.intersect1d(self.candidates, others)
        self.__update_values__(intersection)

    def get_random_candidate(self):
        candidate = random.choice(self.candidates)
        self.is_final = True
        self.__update_values__([candidate])
        return candidate


    def get_index(self):
        return self.pos_x, self.pos_y


    #region Default Overrides
    def __len__(self):
        return 0 if self.is_final else self.cardinality

    def __lt__(self, other):
        return self.cardinality < other

    def __le__(self, other):
        return self.cardinality <= other

    def __eq__(self, other):
        return self.cardinality == other

    def __ne__(self, other):
        return self.cardinality != other

    def __gt__(self, other):
        return self.cardinality > other

    def __ge__(self, other):
        return self.cardinality >= other

    def __str__(self):
        return "C:" + str(self.candidates)

    def __str_cardinality__(self):
        return str(self.cardinality)
    #endregion

