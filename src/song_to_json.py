import assemblyai as aai
from elements import song
import os
import json
BASE_SONGS_FOLDER = r"samples\songs"
BASE_JSON_FOLDER = r"samples\jsons"
SONG_TO_FORMAT = r"Mood.mp3"

aai.settings.api_key = "625058c65a9c4255af2179587a57e19a"


def dump_song_to_json(song: song.Song, baseFolder: str) -> None:
    with open(os.path.join(baseFolder, song.song_name.replace("mp3", "json")), "w") as json_file:
        json_file.write(json.dumps(song.json_format, indent=4))

if __name__ == "__main__":
    dump_song_to_json(song.Song(os.path.join(BASE_SONGS_FOLDER, SONG_TO_FORMAT), SONG_TO_FORMAT), BASE_JSON_FOLDER)
    print("Song dumped to JSON!")