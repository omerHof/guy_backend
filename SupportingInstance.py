class SupportingInstance (object):

    def __init__(self, entityId=None, symbolic_intervals=None, mean_duration=None, mean_offset_from_start=None,
                 mean_offset_from_end=None, mean_of_each_interval=None):
        self.__entityId: int = entityId
        # self.__duration: float = duration
        # self.__offset_from_start: float = offset_from_start
        # self.__offset_from_end: float = offset_from_end
        self.__symbolic_intervals = list()
        for item in symbolic_intervals:
            self.__symbolic_intervals.append(item)
        self.__mean_of_each_interval: list = mean_of_each_interval
        self.__mean_duration: float = mean_duration
        self.__mean_offset_from_start: float = mean_offset_from_start
        self.__mean_offset_from_end: float = mean_offset_from_end

    def set___mean_of_each_interval(self, mean_of_each_interval):
        self.__mean_of_each_interval = mean_of_each_interval

    def add_list_to_intervals(self, symbolic_list):
        for item in symbolic_list:
            self.__symbolic_intervals.append(item)

    def get_symbolic_intervals(self):
        return self.__symbolic_intervals
