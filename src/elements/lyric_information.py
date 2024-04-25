
"""
    A struct that holds necessary information for a lyric in a song.
"""


class LyricInformation:

    def __init__(self, lyric: str, start_time: float, end_time: float) -> None:
        self.lyric = lyric
        self.start_time = start_time
        self.end_time = end_time

    def __eq__(self, value: object) -> bool:
        return self.lyric is value.lyric and self.start_time is value.start_time and self.end_time is value.end_time

    def __repr__(self) -> str:
        return f"Lyric: {self.lyric}. Start time: {self.start_time}. End time: {self.end_time}"
