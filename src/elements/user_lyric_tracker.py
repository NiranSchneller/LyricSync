from elements.lyric_information import LyricInformation
from typing import List

class UserLyricTracker:

    def __init__(self, lyrics: List[LyricInformation]) -> None:
        self.lyrics = lyrics
        self.current_lyric_index = 0


    """
        An outside owner should call this function whenever the user entered a word.

        The returned boolean is a sort of status code, in the sense that:
        1. if it is false, it means the words don't match and the user needs to enter the correct word
        2.  if it is true, it means that the words match and the user can continue to type the next word
    """
    def lyric_entered(self, input: str) -> bool:
        if input is self.lyrics[self.current_lyric_index].lyric:
            self.current_lyric_index += 1
            return True
        return False
    
    def get_next_lyric_to_be_entered(self) -> str:
        return self.lyrics[self.current_lyric_index].lyric

    """
        self.lyrics[self.current_lyric_index] is the info of the next lyric that should be entered by the user

    """
    def get_info_of_last_entered_lyric(self) -> LyricInformation:
        return self.lyrics[self.current_lyric_index - 1]

    
    
