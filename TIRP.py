import ParseOutputFile
import operator as op
from functools import reduce


class TIRP (object):

    def __init__(self, tirp_size=None, symbols=None, relation=None, supporting_instances=None,
                 supporting_entities=None, vertical_support=None, mean_horizontal_support=None, mean_duration=None,
                 mean_offset_from_start=None, mean_offset_from_end=None):
        self.__tirp_size: int = tirp_size
        self.__symbols: list = symbols
        self.__rel: list = relation
        self.__supporting_instances: list = supporting_instances
        self.__supporting_entities: list = supporting_entities
        self.__vertical_support: int = vertical_support
        self.__mean_horizontal_support: float = mean_horizontal_support
        self.__mean_duration: float = round(mean_duration, 2)
        self.__mean_offset_from_start: float = mean_offset_from_start
        self.__mean_offset_from_end: float = mean_offset_from_end
        self.__mean_of_each_interval = list()
        self.__mean_offset_from_first_symbol = list()
        self.__childes = list()

        # init mean_of_each_interval list and mean_offset_from_first_symbol list
        counter = 0;
        for i in range(0, tirp_size):
            self.__mean_of_each_interval.append(0)
            self.__mean_offset_from_first_symbol.append(0)
        for instance in supporting_instances:
            for symbolic in instance.get_symbolic_intervals():
                counter = counter + 1
                start_time_of_TIRP = symbolic[0].getStartTime()
                for i in range(0, tirp_size):
                    end_time = symbolic[i].getEndTime()
                    start_time = symbolic[i].getStartTime()
                    duration = int(end_time) - int(start_time) + 1
                    mean_from_start = int(start_time) - int(start_time_of_TIRP)
                    self.__mean_offset_from_first_symbol[i] += mean_from_start
                    self.__mean_of_each_interval[i] += duration
        # make it mean
        for i in range(0, tirp_size):
            self.__mean_of_each_interval[i] = self.__mean_of_each_interval[i] / counter
            self.__mean_offset_from_first_symbol[i] = self.__mean_offset_from_first_symbol[i] / counter

    def get_tirp_size(self) -> int:
        return self.__tirp_size

    def get_rel_size(self) -> int:
        return len(self.__rel)

    def get_vertical_support(self) -> int:
        return self.__vertical_support

    def get_supporting_instances(self):
        return self.__supporting_instances

    def get_unique_name(self):
        TIRP_name = ""
        for symbol in self.__symbols:
            TIRP_name += symbol + '-'
        TIRP_name += ','
        for rel in self.__rel:
            TIRP_name += rel + '.'
        return TIRP_name

    def get_symbols(self):
        return self.__symbols

    def get_rels(self):
        return self.__rel

    @staticmethod
    def ncr(n, r):
        r = min(r, n - r)
        numer = reduce(op.mul, range(n, n - r, -1), 1)
        denom = reduce(op.mul, range(1, r + 1), 1)
        return numer / denom

    def set_childes(self, TIRPs_in_output_file):
        """
        This method finds the TIRP's immediate childes and adds them to the childes list property of the TIRP
        :param TIRPs_in_output_file: The file that contains all the TIRPs that start with the first symbol
        :return:
        """
        for TIRP_element in TIRPs_in_output_file:
            if TIRP_element.get_tirp_size() == self.__tirp_size + 1 and self.__tirp_size == 1:
                self.__childes.append(TIRP_element)
                TIRP_element.set_childes(TIRPs_in_output_file)
            elif TIRP_element.get_tirp_size() == self.__tirp_size + 1:
                is_match = True
                for i in range(0, len(self.get_symbols())):
                    if self.__symbols[i] != TIRP_element.get_symbols()[i]:
                        is_match = False
                        break
                if is_match:
                    num_of_rels = int(TIRP.ncr(self.get_rel_size(), 2))
                    for i in range(0, num_of_rels):
                        if self.__rel[i] != TIRP_element.get_rels()[i]:
                            is_match = False
                            break
                    if is_match:
                        self.__childes.append(TIRP_element)
                        TIRP_element.set_childes(TIRPs_in_output_file)

