

# TODO: Fill in the blanks
class GameUI:
    def __init__(self) -> None:
        pass


    def incorrect_lyric_entered(self) -> None:
        pass

    def correct_lyric_entered(self) -> None:
        pass

    def present_current_lyric(self, current_word: str) -> None:
        pass

    def song_ended(self, player_success: bool) -> None:
        if player_success:
            self.__end_game_success()
        else:
            self.__end_game_failed()
        
    def __end_game_success(self) -> None:
        pass

    def __end_game_failed(self) -> None:
        pass