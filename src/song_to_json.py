import assemblyai as aai
from elements import song
import os
import traceback
import json
BASE_SONGS_FOLDER = r"samples\songs"
BASE_JSON_FOLDER = r"samples\jsons"
aai.settings.api_key = "625058c65a9c4255af2179587a57e19a"


def get_chosen_song() -> str:
    options = [file for file in os.listdir(BASE_SONGS_FOLDER)]
    options = {i + 1: file for i, file in enumerate(options)}

    for number, file in options.items():
        print(f"{number} - {file}")

    chosen: int = int(
        input("Select the corresponding number to the song you'd like to parse: "))

    return options[chosen]


def dump_song_to_json(song: song.Song, baseFolder: str) -> None:
    with open(os.path.join(baseFolder, song.song_name.replace("mp3", "json")), "w") as json_file:
        json_file.write(json.dumps(song.json_format, indent=4))


if __name__ == "__main__":
    try:
        chosen_song: str = get_chosen_song()
        dump_song_to_json(song.Song(os.path.join(
            BASE_SONGS_FOLDER, chosen_song), chosen_song), BASE_JSON_FOLDER)
        print("Song dumped to JSON!")
    except:
        print(f"An error has occurred! Stacktrace: {traceback.print_exc()}")
