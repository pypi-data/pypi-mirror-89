from collections import OrderedDict
import numpy as np
from typing import List
import attr


@attr.s
class Struct(object):
    """ Basic struct-like object for data keeping. """

    start = attr.ib()
    end = attr.ib()
    num = attr.ib(default=None)


class ChoiceManagerHex:
    """
    Switch-like helper class. Contains the type of information
    held in each bit of a single event from the multiscaler, for all timepatches.
    """

    def __init__(self):
        self.__choice_table = {
            "0": self.timepatch_0,
            "5": self.timepatch_5,
            "1": self.timepatch_1,
            "1a": self.timepatch_1a,
            "2a": self.timepatch_2a,
            "22": self.timepatch_22,
            "32": self.timepatch_32,
            "2": self.timepatch_2,
            "5b": self.timepatch_5b,
            "Db": self.timepatch_Db,
            "f3": self.timepatch_f3,
            "43": self.timepatch_43,
            "c3": self.timepatch_c3,
            "3": self.timepatch_3,
        }

    def timepatch_0(self, dict_of_slices):
        dict_of_slices.pop("tag", None)
        dict_of_slices.pop("sweep", None)

        dict_of_slices["time_rel_sweep"].start = 0
        dict_of_slices["time_rel_sweep"].end = 3
        dict_of_slices["time_rel_sweep"].needs_bits = False

        dict_of_slices["chan_edge"].start = 3
        dict_of_slices["chan_edge"].end = 4

        return dict_of_slices

    def timepatch_5(self, dict_of_slices):
        dict_of_slices.pop("tag", None)

        dict_of_slices["sweep"].start = 0
        dict_of_slices["sweep"].end = 2
        dict_of_slices["sweep"].needs_bits = False

        dict_of_slices["time_rel_sweep"].start = 2
        dict_of_slices["time_rel_sweep"].end = 7
        dict_of_slices["time_rel_sweep"].needs_bits = False

        dict_of_slices["chan_edge"].start = 7
        dict_of_slices["chan_edge"].end = 8

        return dict_of_slices

    def timepatch_1(self, dict_of_slices):
        dict_of_slices.pop("tag", None)
        dict_of_slices.pop("sweep", None)

        dict_of_slices["time_rel_sweep"].start = 0
        dict_of_slices["time_rel_sweep"].end = 7
        dict_of_slices["time_rel_sweep"].needs_bits = False

        dict_of_slices["chan_edge"].start = 7
        dict_of_slices["chan_edge"].end = 8

        return dict_of_slices

    def timepatch_1a(self, dict_of_slices):
        dict_of_slices.pop("tag", None)

        dict_of_slices["sweep"].start = 0
        dict_of_slices["sweep"].end = 4
        dict_of_slices["sweep"].needs_bits = False

        dict_of_slices["time_rel_sweep"].start = 4
        dict_of_slices["time_rel_sweep"].end = 11
        dict_of_slices["time_rel_sweep"].needs_bits = False

        dict_of_slices["chan_edge"].start = 11
        dict_of_slices["chan_edge"].end = 12

        return dict_of_slices

    def timepatch_2a(self, dict_of_slices):
        dict_of_slices["tag"].start = 0
        dict_of_slices["tag"].end = 2
        dict_of_slices["tag"].needs_bits = False

        dict_of_slices["sweep"].start = 2
        dict_of_slices["sweep"].end = 4
        dict_of_slices["sweep"].needs_bits = False

        dict_of_slices["time_rel_sweep"].start = 4
        dict_of_slices["time_rel_sweep"].end = 11
        dict_of_slices["time_rel_sweep"].needs_bits = False

        dict_of_slices["chan_edge"].start = 11
        dict_of_slices["chan_edge"].end = 12

        return dict_of_slices

    def timepatch_22(self, dict_of_slices):
        dict_of_slices.pop("sweep", None)

        dict_of_slices["tag"].start = 0
        dict_of_slices["tag"].end = 2
        dict_of_slices["tag"].needs_bits = False

        dict_of_slices["time_rel_sweep"].start = 2
        dict_of_slices["time_rel_sweep"].end = 11
        dict_of_slices["time_rel_sweep"].needs_bits = False

        dict_of_slices["chan_edge"].start = 11
        dict_of_slices["chan_edge"].end = 12

        return dict_of_slices

    def timepatch_32(self, dict_of_slices):
        dict_of_slices["lost"] = True
        dict_of_slices.pop("tag", None)

        dict_of_slices["sweep"].start = 0
        dict_of_slices["sweep"].end = 2
        dict_of_slices["sweep"].needs_bits = True

        dict_of_slices["time_rel_sweep"].start = 2
        dict_of_slices["time_rel_sweep"].end = 11
        dict_of_slices["time_rel_sweep"].needs_bits = False

        dict_of_slices["chan_edge"].start = 11
        dict_of_slices["chan_edge"].end = 12

        return dict_of_slices

    def timepatch_2(self, dict_of_slices):
        dict_of_slices.pop("tag", None)
        dict_of_slices.pop("sweep", None)

        dict_of_slices["time_rel_sweep"].start = 0
        dict_of_slices["time_rel_sweep"].end = 11
        dict_of_slices["time_rel_sweep"].needs_bits = False

        dict_of_slices["chan_edge"].start = 11
        dict_of_slices["chan_edge"].end = 12

        return dict_of_slices

    def timepatch_5b(self, dict_of_slices):
        dict_of_slices["lost"] = True

        dict_of_slices["tag"].start = 0
        dict_of_slices["tag"].end = 4
        dict_of_slices["tag"].needs_bits = True

        dict_of_slices["sweep"].start = 4
        dict_of_slices["sweep"].end = 8
        dict_of_slices["sweep"].needs_bits = False

        dict_of_slices["time_rel_sweep"].start = 8
        dict_of_slices["time_rel_sweep"].end = 15
        dict_of_slices["time_rel_sweep"].needs_bits = False

        dict_of_slices["chan_edge"].start = 15
        dict_of_slices["chan_edge"].end = 16

        return dict_of_slices

    def timepatch_Db(self, dict_of_slices):
        dict_of_slices["tag"].start = 0
        dict_of_slices["tag"].end = 4
        dict_of_slices["tag"].needs_bits = False

        dict_of_slices["sweep"].start = 4
        dict_of_slices["sweep"].end = 8
        dict_of_slices["sweep"].needs_bits = False

        dict_of_slices["time_rel_sweep"].start = 8
        dict_of_slices["time_rel_sweep"].end = 15
        dict_of_slices["time_rel_sweep"].needs_bits = False

        dict_of_slices["chan_edge"].start = 15
        dict_of_slices["chan_edge"].end = 16

        return dict_of_slices

    def timepatch_f3(self, dict_of_slices):
        dict_of_slices["lost"] = True

        dict_of_slices["tag"].start = 0
        dict_of_slices["tag"].end = 4
        dict_of_slices["tag"].needs_bits = False

        dict_of_slices["sweep"].start = 4
        dict_of_slices["sweep"].end = 6
        dict_of_slices["sweep"].needs_bits = True

        dict_of_slices["time_rel_sweep"].start = 6
        dict_of_slices["time_rel_sweep"].end = 15
        dict_of_slices["time_rel_sweep"].needs_bits = False

        dict_of_slices["chan_edge"].start = 15
        dict_of_slices["chan_edge"].end = 16

        return dict_of_slices

    def timepatch_43(self, dict_of_slices):
        dict_of_slices.pop("sweep", None)

        dict_of_slices["lost"] = True

        dict_of_slices["tag"].start = 0
        dict_of_slices["tag"].end = 4
        dict_of_slices["tag"].needs_bits = True

        dict_of_slices["time_rel_sweep"].start = 4
        dict_of_slices["time_rel_sweep"].end = 15
        dict_of_slices["time_rel_sweep"].needs_bits = False

        dict_of_slices["chan_edge"].start = 15
        dict_of_slices["chan_edge"].end = 16

        return dict_of_slices

    def timepatch_c3(self, dict_of_slices):
        dict_of_slices.pop("sweep", None)

        dict_of_slices["tag"].start = 0
        dict_of_slices["tag"].end = 4
        dict_of_slices["tag"].needs_bits = False

        dict_of_slices["time_rel_sweep"].start = 4
        dict_of_slices["time_rel_sweep"].end = 15
        dict_of_slices["time_rel_sweep"].needs_bits = False

        dict_of_slices["chan_edge"].start = 15
        dict_of_slices["chan_edge"].end = 16

        return dict_of_slices

    def timepatch_3(self, dict_of_slices):
        # NOT IMPLEMENTED IN THE ACTUAL CODE
        dict_of_slices.pop("sweep", None)

        dict_of_slices["tag"].start = 0
        dict_of_slices["tag"].end = 2
        dict_of_slices["tag"].needs_bits = True

        dict_of_slices["time_rel_sweep"].start = 2
        dict_of_slices["time_rel_sweep"].end = 15
        dict_of_slices["time_rel_sweep"].needs_bits = False

        dict_of_slices["chan_edge"].start = 15
        dict_of_slices["chan_edge"].end = 16

        return dict_of_slices

    def __generate_dict_from_indices(self) -> OrderedDict:
        """
        Generate a basic template dictionary to be populated with slicing indices.
        :param slices:
        :return:
        """
        slice_dict: OrderedDict = OrderedDict()
        keys = ["lost", "tag", "sweep", "time_rel_sweep", "chan_edge"]

        slice_dict[keys[0]] = False
        for key in keys[1:]:
            slice_dict[key] = Struct(np.nan, np.nan)

        return slice_dict

    def process(self, case):
        """
        Generate a dictionary and populate it with the proper value, accoring to the timepatch (==case).
        """
        assert isinstance(case, str)

        dict_of_slices = self.__generate_dict_from_indices()
        populated_dict_of_slices = self.__choice_table[case](dict_of_slices)

        return populated_dict_of_slices


class ChoiceManagerBinary:
    def __init__(self) -> None:
        self.__choice_table = {
            "0": self.timepatch_0,
            "5": self.timepatch_5,
            "1": self.timepatch_1,
            "1a": self.timepatch_1a,
            "2a": self.timepatch_2a,
            "22": self.timepatch_22,
            "32": self.timepatch_32,
            "2": self.timepatch_2,
            "5b": self.timepatch_5b,
            "Db": self.timepatch_Db,
            "f3": self.timepatch_f3,
            "43": self.timepatch_43,
            "c3": self.timepatch_c3,
            "3": self.timepatch_3,
        }

    def timepatch_0(self, dict_of_slices) -> OrderedDict:
        dict_of_slices.pop("tag", None)
        dict_of_slices.pop("sweep", None)

        dict_of_slices["time_rel_sweep"].start = 0
        dict_of_slices["time_rel_sweep"].end = 12
        dict_of_slices["time_rel_sweep"].cols = 16

        dict_of_slices["edge"].start = 12
        dict_of_slices["edge"].end = 13
        dict_of_slices["edge"].cols = 8

        dict_of_slices["chan"].start = 13
        dict_of_slices["chan"].end = 15
        dict_of_slices["chan"].cols = 8

        return dict_of_slices

    def timepatch_5(self, dict_of_slices) -> OrderedDict:
        dict_of_slices.pop("tag", None)

        dict_of_slices["sweep"].start = 0
        dict_of_slices["sweep"].end = 8

        dict_of_slices["time_rel_sweep"].start = 8
        dict_of_slices["time_rel_sweep"].end = 28

        dict_of_slices["chan_edge"].start = 28
        dict_of_slices["chan_edge"].end = 32

        return dict_of_slices

    def timepatch_1(self, dict_of_slices) -> OrderedDict:
        dict_of_slices.pop("tag", None)
        dict_of_slices.pop("sweep", None)

        dict_of_slices["time_rel_sweep"].start = 0
        dict_of_slices["time_rel_sweep"].end = 28

        dict_of_slices["chan_edge"].start = 28
        dict_of_slices["chan_edge"].end = 32

        return dict_of_slices

    def timepatch_1a(self, dict_of_slices) -> OrderedDict:
        dict_of_slices.pop("tag", None)

        dict_of_slices["sweep"].start = 0
        dict_of_slices["sweep"].end = 16

        dict_of_slices["time_rel_sweep"].start = 16
        dict_of_slices["time_rel_sweep"].end = 44

        dict_of_slices["chan_edge"].start = 44
        dict_of_slices["chan_edge"].end = 48

        return dict_of_slices

    def timepatch_2a(self, dict_of_slices) -> OrderedDict:
        dict_of_slices["tag"].start = 0
        dict_of_slices["tag"].end = 8

        dict_of_slices["sweep"].start = 8
        dict_of_slices["sweep"].end = 16

        dict_of_slices["time_rel_sweep"].start = 16
        dict_of_slices["time_rel_sweep"].end = 44

        dict_of_slices["chan_edge"].start = 44
        dict_of_slices["chan_edge"].end = 48

        return dict_of_slices

    def timepatch_22(self, dict_of_slices) -> OrderedDict:
        dict_of_slices.pop("sweep", None)

        dict_of_slices["tag"].start = 0
        dict_of_slices["tag"].end = 8

        dict_of_slices["time_rel_sweep"].start = 8
        dict_of_slices["time_rel_sweep"].end = 44

        dict_of_slices["chan_edge"].start = 44
        dict_of_slices["chan_edge"].end = 48

        return dict_of_slices

    def timepatch_32(self, dict_of_slices) -> OrderedDict:
        dict_of_slices["lost"] = 1
        dict_of_slices.pop("tag", None)

        dict_of_slices["sweep"].start = 1
        dict_of_slices["sweep"].end = 8

        dict_of_slices["time_rel_sweep"].start = 8
        dict_of_slices["time_rel_sweep"].end = 44

        dict_of_slices["chan_edge"].start = 44
        dict_of_slices["chan_edge"].end = 48

        return dict_of_slices

    def timepatch_2(self, dict_of_slices) -> OrderedDict:
        dict_of_slices.pop("tag", None)
        dict_of_slices.pop("sweep", None)

        dict_of_slices["time_rel_sweep"].start = 0
        dict_of_slices["time_rel_sweep"].end = 44

        dict_of_slices["chan_edge"].start = 44
        dict_of_slices["chan_edge"].end = 48

        return dict_of_slices

    def timepatch_5b(self, dict_of_slices) -> OrderedDict:
        dict_of_slices["lost"].start = 0
        dict_of_slices["lost"].end = 1
        dict_of_slices["lost"].cols = 8

        dict_of_slices["tag"].start = 1
        dict_of_slices["tag"].end = 16
        dict_of_slices["tag"].cols = 16

        dict_of_slices["sweep"].start = 16
        dict_of_slices["sweep"].end = 32

        dict_of_slices["time_rel_sweep"].start = 32
        dict_of_slices["time_rel_sweep"].end = 60
        dict_of_slices["time_rel_sweep"].cols = 32

        dict_of_slices["edge"].start = 60
        dict_of_slices["edge"].end = 61
        dict_of_slices["edge"].cols = 8

        dict_of_slices["chan"].start = 61
        dict_of_slices["chan"].end = 64
        dict_of_slices["chan"].cols = 8

        return dict_of_slices

    def timepatch_Db(self, dict_of_slices) -> OrderedDict:
        dict_of_slices["tag"].start = 0
        dict_of_slices["tag"].end = 16

        dict_of_slices["sweep"].start = 16
        dict_of_slices["sweep"].end = 32

        dict_of_slices["time_rel_sweep"].start = 32
        dict_of_slices["time_rel_sweep"].end = 60

        dict_of_slices["chan_edge"].start = 60
        dict_of_slices["chan_edge"].end = 64

        return dict_of_slices

    def timepatch_f3(self, dict_of_slices) -> OrderedDict:
        dict_of_slices["lost"].start = 0
        dict_of_slices["lost"].end = 1
        dict_of_slices["lost"].cols = 8

        dict_of_slices["tag"].start = 1
        dict_of_slices["tag"].end = 17
        dict_of_slices["tag"].cols = 16

        dict_of_slices["sweep"].start = 17
        dict_of_slices["sweep"].end = 24
        dict_of_slices["sweep"].cols = 8

        dict_of_slices["time_rel_sweep"].start = 24
        dict_of_slices["time_rel_sweep"].end = 60
        dict_of_slices["time_rel_sweep"].cols = 40

        dict_of_slices["edge"].start = 60
        dict_of_slices["edge"].end = 61
        dict_of_slices["edge"].cols = 8

        dict_of_slices["chan"].start = 61
        dict_of_slices["chan"].end = 64
        dict_of_slices["chan"].cols = 8

        return dict_of_slices

    def timepatch_43(self, dict_of_slices) -> OrderedDict:
        dict_of_slices.pop("sweep", None)

        dict_of_slices["lost"] = 1

        dict_of_slices["tag"].start = 1
        dict_of_slices["tag"].end = 16

        dict_of_slices["time_rel_sweep"].start = 16
        dict_of_slices["time_rel_sweep"].end = 60

        dict_of_slices["chan_edge"].start = 60
        dict_of_slices["chan_edge"].end = 64

        return dict_of_slices

    def timepatch_c3(self, dict_of_slices) -> OrderedDict:
        dict_of_slices.pop("sweep", None)

        dict_of_slices["tag"].start = 0
        dict_of_slices["tag"].end = 16

        dict_of_slices["time_rel_sweep"].start = 16
        dict_of_slices["time_rel_sweep"].end = 60

        dict_of_slices["chan_edge"].start = 60
        dict_of_slices["chan_edge"].end = 64

        return dict_of_slices

    def timepatch_3(self, dict_of_slices) -> OrderedDict:
        dict_of_slices.pop("sweep", None)

        dict_of_slices["lost"] = 1

        dict_of_slices["tag"].start = 1
        dict_of_slices["tag"].end = 6

        dict_of_slices["time_rel_sweep"].start = 6
        dict_of_slices["time_rel_sweep"].end = 60

        dict_of_slices["chan_edge"].start = 60
        dict_of_slices["chan_edge"].end = 64

        return dict_of_slices

    def __generate_dict_from_indices(self) -> OrderedDict:
        """
        Generate a basic template dictionary to be populated with slicing indices.
        :param slices:
        :return:
        """
        from pysight.nd_hist_generator.movie import Struct

        slice_dict: OrderedDict = OrderedDict()
        keys: List[str] = ["lost", "tag", "sweep", "time_rel_sweep", "edge", "chan"]

        for key in keys:
            slice_dict[key] = Struct(np.nan, np.nan)

        return slice_dict

    def process(self, case: str) -> OrderedDict:
        """
        Generate a dictionary and populate it with the proper value, accoring to the timepatch (==case).
        """
        assert isinstance(case, str)

        dict_of_slices: OrderedDict = self.__generate_dict_from_indices()
        populated_dict_of_slices: OrderedDict = self.__choice_table[case](
            dict_of_slices
        )

        return populated_dict_of_slices
