import assemblyai as aai
aai.settings.api_key = "625058c65a9c4255af2179587a57e19a" # Secret lol
import logging
from elements.song_lyrics import SongLyrics
from elements.stopwatch import Stopwatch
from elements.lyric_information import LyricInformation
from typing import List
"""
    This class represents a song. Once a song is started, the get_current_lyric function is used
    to get the current lyric according to a timer initialized when the song was started.

    The song indicates whether it is finished or not according to the corresponding function.

    Not calling start_song before song_ended can lead to undesirable results.
"""
class Song:
    def __init__(self, song_url: str) -> None:
        # Generating the transcript and all the lyrics + timestamps
        self.song_lyrics: SongLyrics = SongLyrics(aai.Transcriber().transcribe(song_url))
        self.timer: Stopwatch = Stopwatch()
        self.ended: bool = False

    def start_song(self):
        self.timer.reset()
        self.ended = False

    """
        Has to be called after start_song() to get desirable results.

        Will return the current lyric the song is 
    """
    def get_current_lyric(self) -> LyricInformation:
        return self.song_lyrics.get_lyric_by_timestamp(self.timer.get_elapsed())

    def get_last_lyric(self) -> LyricInformation:
        return self.song_lyrics.get_last_lyric()


    def song_ended(self) -> bool:
        if self.timer.get_elapsed() > self.song_lyrics.get_last_lyric().end_time:
            self.ended = True
        return self.ended
    
    def get_all_lyrics(self) -> List[str]:
        return [lyric_info.lyric for lyric_info in self.song_lyrics.lyrics]






        