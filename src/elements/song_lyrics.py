from typing import List, Tuple, Optional
from assemblyai import Transcript, WordSearchMatch
from elements.lyric_information import LyricInformation
import elements.stopwatch as stopwatch
import logging
logger = logging.getLogger(__name__)


class SongLyrics:
    def __init__(self, lyrics: Transcript) -> None:
        self.lyrics: List[LyricInformation] = []
        self.get_lyrics_from_transcript(lyrics)
        self.lyrics.sort(key=lambda info: info.start_time)
        logger.info(f"Song lyrics list: {self.lyrics}", extra={
                    "programTime": -1})

    """
        Generates a lyrics List according to the self.lyrics format (each word with start and end time).
    """

    def get_lyrics_from_transcript(self, lyrics: Transcript) -> None:
        transcript_text: Optional[str] = lyrics.text
        matches: List[WordSearchMatch] = lyrics.word_search(
            words=transcript_text.split())
        # logger.info(f"The lyrics transcript text is: {lyrics.text}")
        # logger.info(f"The matches are: {matches}")
        # Iterates for each match, and grabs the timestamps by the current occurence of the word
        current_occurrence_words: dict = {}
        for match in matches:
            current_lyric = match.text
            if not current_lyric in current_occurrence_words.keys():
                current_occurrence_words.update({current_lyric: 0})

            current_timestamp_index = current_occurrence_words[current_lyric]

            self.lyrics.append(LyricInformation(current_lyric, match.timestamps[current_timestamp_index][0],
                                                match.timestamps[current_timestamp_index][1]))

            next_occurence = current_occurrence_words.pop(current_lyric) + 1
            current_occurrence_words.update({current_lyric: next_occurence})

    """
        If the song is in between two lyrics, then this function will return the next one.
    """

    def get_lyric_by_timestamp(self, timestamp: float) -> LyricInformation:
        for lyric_information in self.lyrics:
            end_time_seconds = stopwatch.Stopwatch.milliseconds_to_seconds(
                lyric_information.end_time)
            if end_time_seconds > timestamp:
                return lyric_information

    def get_last_lyric(self) -> LyricInformation:
        return self.lyrics[-1]
