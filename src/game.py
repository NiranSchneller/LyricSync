import logging
import assemblyai as aai
from threading import Thread, Lock
from elements.song import Song
from elements.user_lyric_tracker import UserLyricTracker
from gui.game_ui import GameUI
from typing import List, Tuple, Union
from elements.stopwatch import Stopwatch
import math
from os import path
import os
import json
# If FAILED_THRESHOLD seconds behind, the player failed entering the songs lyrics according to the beat
FAILED_THRESHOLD = 3
BASE_JSON_FOLDER = r"samples\jsons"
BASE_SONGS_FOLDER = r"samples\songs"
BASE_LOGS_FOLDER = r"logs"
SONG_TO_PLAY = r"Mood.json"
# Initialization
aai.settings.api_key = "625058c65a9c4255af2179587a57e19a"
logger = logging.getLogger(__name__)
logging.basicConfig(filename=path.join(
    os.getcwd(), BASE_LOGS_FOLDER, "songbeats.log"), level=logging.INFO)

mutex: Lock = Lock()
player_input: str = ""
"""
    Each time player inputs and then lock the resource @player_input
"""


def handle_player():
    global player_input
    while True:
        current_input: str = input()
        mutex.acquire()
        player_input = current_input[::1]  # Copy
        mutex.release()


def has_player_entered_input() -> bool:
    mutex.acquire()
    out: bool = player_input != ""
    mutex.release()
    return out


def play_song(song: Song, placeholder: str):
    song.start_song()


def display_song_lyrics(song: Song, placeholder: str):
    previous_lyric = ""
    while True:
        current_lyric = song.get_current_lyric().lyric
        if current_lyric == "" or previous_lyric == current_lyric:
            continue
        print(current_lyric)
        previous_lyric = current_lyric


def dump_song_to_json(song: Song, baseFolder: str) -> None:
    with open(path.join(baseFolder, song.song_name.replace("mp3", "json")), "w") as json_file:
        json_file.write(json.dumps(song.json_format, indent=4))


def create_song(json_or_file_path: str) -> Song:
    if ".json" in json_or_file_path:
        json_string = ""
        with open(json_or_file_path, "r") as file:
            json_string += file.read()
        return Song.from_json(json_string)
    else:
        return Song(json_or_file_path, path.basename(json_or_file_path))


def create_game_objects(song_json_or_file_path: str, base_folder_for_dump) -> (Tuple[Stopwatch, Thread, Song, GameUI,
                                                                                     UserLyricTracker, Thread, Thread]):
    main_stopwatch: Stopwatch = Stopwatch()
    input_thread = Thread(target=handle_player)
    logger.info("Song construction")
    song: Song = create_song(song_json_or_file_path)
    logger.info(
        f"Song constructed at time: {main_stopwatch.get_elapsed()}. Dumping to matching JSON in folder /samples/jsons...")
    dump_song_to_json(song, base_folder_for_dump)
    print("Song started!")
    gameUI = GameUI()
    user_lyric_tracker = UserLyricTracker(song.song_lyrics.lyrics)
    song_thread = Thread(target=play_song, args=(song, ""))
    words_display_thread = Thread(
        target=display_song_lyrics, args=(song, ""))
    return main_stopwatch, input_thread, song, gameUI, user_lyric_tracker, song_thread, words_display_thread


def main():
    main_stopwatch, input_thread, song, gameUI, user_lyric_tracker, song_thread, words_display_thread = (
        create_game_objects(path.join(BASE_JSON_FOLDER, SONG_TO_PLAY), BASE_JSON_FOLDER))
    logger.info(f"cwd: {os.getcwd()}")
    global player_input

    song_thread.start()
    words_display_thread.start()
    input_thread.start()
    # not song.song_ended()
    print("Will start printing lyrics")
    while True:
        while not has_player_entered_input():  # Wait for input from the user
            if song.song_ended():  # While waiting for input, still check if song has finished
                break
            pass
        if song.song_ended():  # Check if quit inner while because song ended
            logger.info(f"Song ended at: {main_stopwatch.get_elapsed()}")
            break

        correct_word = user_lyric_tracker.lyric_entered(player_input)
        if not correct_word:
            logger.info(
                f"User typed incorrect word: {player_input}. lyric expected: {user_lyric_tracker.get_next_lyric_to_be_entered()} at time: {main_stopwatch.get_elapsed()}")
            gameUI.incorrect_lyric_entered()
            player_input = ""
            continue
        else:
            logger.info(
                f"Correct word entered: {player_input} at time: {main_stopwatch.get_elapsed()}")
            gameUI.correct_lyric_entered()

        current_lyric = song.get_current_lyric()
        logger.info(
            f"Current word that should be typed: {current_lyric}, time: {main_stopwatch.get_elapsed()}")

        # TODO: handle a user that is entering words too fast (or too slow...)
        if math.fabs(current_lyric.end_time - user_lyric_tracker.get_info_of_last_entered_lyric().end_time) > FAILED_THRESHOLD:
            logger.info(
                f"Word entered too fast/slow, quitting at time: {main_stopwatch.get_elapsed()}")
            break

        player_input = ""  # Reset the input

    player_success: bool = user_lyric_tracker.get_info_of_last_entered_lyric(
    ) is song.get_last_lyric()
    gameUI.song_ended(player_success)
    input_thread.join()
    song_thread.join()
    words_display_thread.join()


if __name__ == "__main__":
    main()
