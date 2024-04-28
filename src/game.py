import logging
from threading import Thread, Event
from elements.song import Song
from elements.user_lyric_tracker import UserLyricTracker
from gui.game_ui import GameUI
from typing import List, Tuple, Union
from elements.stopwatch import Stopwatch
import math
from os import path
import os
import json
import queue
import pyqt6_tools
# If FAILED_THRESHOLD seconds behind, the player failed entering the songs lyrics according to the beat
FAILED_THRESHOLD = 3
BASE_JSON_FOLDER = r"samples\jsons"
BASE_LOGS_FOLDER = r"logs"
SONG_TO_PLAY = r"Mood.json"
# Initialization
logger = logging.getLogger(__name__)
logging.basicConfig(filename=path.join(
    os.getcwd(), BASE_LOGS_FOLDER, "songbeats.log"), level=logging.INFO)

input_queue = queue.Queue()  # Thread safe
"""
    Each time player inputs and then lock the resource @player_input
"""


def handle_player():
    while True:
        input_queue.put(input())


def has_player_entered_input() -> bool:
    return input_queue.get() is not None

def play_song(song: Song, placeholder: str):
    song.start_song()
    print("Song started!")


def display_song_lyrics(song: Song, display_event: Event):
    previous_lyric = ""
    display_event.wait()
    while True:
        current_lyric = song.get_current_lyric().lyric
        if previous_lyric != current_lyric:
            print(current_lyric)
        previous_lyric = current_lyric




def create_song(json_or_file_path: str) -> Song:
    if ".json" in json_or_file_path:
        json_string = ""
        with open(json_or_file_path, "r") as file:
            json_string += file.read()
        return Song.from_json(json_string)
    else:
        return Song(json_or_file_path, path.basename(json_or_file_path))


def create_game_objects(song_json_or_file_path: str) -> (Tuple[Stopwatch, Thread, Song, GameUI,
                                                                                     UserLyricTracker, Thread, Thread, Event]):
    main_stopwatch: Stopwatch = Stopwatch()
    input_thread = Thread(target=handle_player)
    logger.info("Song construction")
    song: Song = create_song(song_json_or_file_path)
    logger.info(f"Song constructed at time: {main_stopwatch.get_elapsed()}")
    gameUI = GameUI()
    user_lyric_tracker = UserLyricTracker(song.song_lyrics.lyrics)
    song_thread = Thread(target=play_song, args=(song, ""))

    display_event = Event()
    words_display_thread = Thread(
        target=display_song_lyrics, args=(song, display_event))
    return main_stopwatch, input_thread, song, gameUI, user_lyric_tracker, song_thread, words_display_thread, display_event


def main():
    main_stopwatch, input_thread, song, gameUI, user_lyric_tracker, song_thread, words_display_thread, display_event = (
        create_game_objects(path.join(BASE_JSON_FOLDER, SONG_TO_PLAY)))
    global player_input

    song.start_song()    
    words_display_thread.start()
    input_thread.start()

    display_event.set()


if __name__ == "__main__":
    main()
