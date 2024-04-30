from typing import List
from elements.lyric_information import LyricInformation
from elements.stopwatch import Stopwatch
from elements.song_lyrics import SongLyrics
import logging
import assemblyai as aai
from typing import Dict, Union
import json
import pygame
"""
    This class represents a song. Once a song is started, the get_current_lyric function is used
    to get the current lyric according to a timer initialized when the song was started.
    
    The song indicates whether it is finished or not according to the corresponding function.

    Not calling start_song before song_ended can lead to undesirable results.
"""

logger = logging.getLogger(__name__)


class Song:
    def __init__(self, song_url: str, song_name: str, transcribe: bool = True) -> None:
        # Generating the transcript and all the lyrics + timestamps

        if transcribe:
            self.song_lyrics: SongLyrics = SongLyrics(
                aai.Transcriber().transcribe(song_url))
        else:
            self.song_lyrics = SongLyrics()
        self.timer: Stopwatch = Stopwatch()
        self.ended: bool = False
        self.song_url = song_url
        self.song_name = song_name

    def start_song(self):
        pygame.init()
        pygame.mixer.music.load(self.song_url)
        pygame.mixer.music.play()

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

    @property
    def json_format(self) -> Dict[str, Union[str, List[Dict[str, str | float]]]]:
        return {
            "song_url": self.song_url,
            "song_name": self.song_name,
            "song_lyrics": self.song_lyrics.json_format
        }

    @staticmethod
    def from_json(json_string: str) -> "Song":
        json_format = json.loads(json_string)
        song_lyrics = SongLyrics()

        temp = json_format["song_lyrics"]
        song_lyrics_lyrics = []
        for dictionary in temp:
            song_lyrics_lyrics.append(LyricInformation(
                dictionary["lyric"], (dictionary["start_time"]), dictionary["end_time"]))

        song_lyrics.lyrics = song_lyrics_lyrics

        out = Song(json_format["song_url"], json_format["song_name"], False)
        out.song_lyrics = song_lyrics
        return out
