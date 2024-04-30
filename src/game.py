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

BASE_JSON_FOLDER = r"samples\jsons"
BASE_LOGS_FOLDER = r"logs"
SONG_TO_PLAY = r"Godzilla.json"

# Initialization
logger = logging.getLogger(__name__)
logging.basicConfig(filename=path.join(
    os.getcwd(), BASE_LOGS_FOLDER, "songbeats.log"), level=logging.INFO)

input_queue = queue.Queue()  # Thread safe

def handle_player():
    while True:
        input_queue.put(input())


def has_player_entered_input() -> bool:
    return input_queue.get() is not None

def display_song_lyrics(song: Song):
    previous_lyric = ""
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
                                                                UserLyricTracker, Thread]):
    main_stopwatch: Stopwatch = Stopwatch()
    
    song: Song = create_song(song_json_or_file_path)
    gameUI = GameUI()
    user_lyric_tracker = UserLyricTracker(song.song_lyrics.lyrics)

    input_thread = Thread(target=handle_player)
    words_display_thread = Thread(target=display_song_lyrics, args=[song])
    
    return main_stopwatch, input_thread, song, gameUI, user_lyric_tracker, words_display_thread


def get_chosen_song() -> str:
    options = [file for file in os.listdir(BASE_JSON_FOLDER)]
    options = {i + 1 : file for i, file in enumerate(options)}

    for number,file in options.items():
        print(f"{number} - {file}")

    chosen: int = int(input("Select the corresponding number to the song you'd like to parse: "))

    return options[chosen]

def main():
    main_stopwatch, input_thread, song, gameUI, user_lyric_tracker, words_display_thread = (
        create_game_objects(path.join(BASE_JSON_FOLDER, get_chosen_song())))

    song.start_song()
    words_display_thread.start()
    input_thread.start()


if __name__ == "__main__":
    main()
