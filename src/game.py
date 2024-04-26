import logging
import assemblyai as aai
import threading
from elements.song import Song
from elements.user_lyric_tracker import UserLyricTracker
from gui.game_ui import GameUI
from typing import List
from elements.stopwatch import Stopwatch
import math

mutex: threading.Lock = threading.Lock()
player_input: str = ""
# If FAILED_THRESHOLD seconds behind, the player failed entering the songs lyrics according to the beat
FAILED_THRESHOLD = 3

# Initialization
aai.settings.api_key = "625058c65a9c4255af2179587a57e19a"
logger = logging.getLogger(__name__)
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


def main():
    main_stopwatch: Stopwatch = Stopwatch()
    logging.basicConfig(filename="songbeats.log", level=logging.INFO)

    logger.info("Beggining Thread initialization")

    global player_input
    input_thread = threading.Thread(target=handle_player)
    logger.info("Song construction")
    song = Song(
        r"C:\Users\niran\Desktop\School\12thGrade\SongBeats\src\samples\Mood.mp3")
    logger.info(f"Song constructed at time: {main_stopwatch.get_elapsed()}")
    gameUI = GameUI()
    user_lyric_tracker = UserLyricTracker(song.song_lyrics.lyrics)
    song_thread = threading.Thread(target=play_song, args=(song, ""))
    words_display_thread = threading.Thread(
        target=display_song_lyrics, args=(song, ""))
    song_thread.start()
    words_display_thread.start()
    input_thread.start()
    print("Song started")
    # not song.song_ended()
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
