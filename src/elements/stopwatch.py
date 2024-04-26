import time

"""
    The timer is in seconds and has high percision.
"""
class Stopwatch:

    def __init__(self) -> None:
        self.start_time = self.__get_time_reference() # For fractions of a second

    def get_elapsed(self) -> float:
        return self.__get_time_reference() - self.start_time

    def __get_time_reference(self) -> float: # In seconds
        return Stopwatch.microseconds_to_seconds(time.time_ns())

    def reset(self):
        self.start_time = self.__get_time_reference()

    @staticmethod
    def microseconds_to_seconds(microseconds: float) -> float:
        return microseconds / 10**9
    
    @staticmethod
    def milliseconds_to_seconds(milliseconds: float) -> float:
        return milliseconds / 10**3
