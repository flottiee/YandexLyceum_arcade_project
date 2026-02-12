import arcade
import constants
from pathlib import Path
import sys
import os
import random

PROJECT_ROOT = Path(__file__).parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from views.menu_view import MenuView

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.SCREEN_TITLE)
        
        self.music_list = []
        self.current_song_index = 0
        self.music_player = None
        
        self.setup_music()
        self.play_next_song()

    def setup_music(self):
        """Ищет музыку в подпапке soundtracks"""
        music_path = PROJECT_ROOT / "assets" / "sounds" / "soundtracks"
        if music_path.exists():
            self.music_list = [
                str(f) for f in music_path.iterdir() 
                if f.suffix.lower() in ('.mp3', '.wav', '.ogg')
            ]
            random.shuffle(self.music_list)

    def play_next_song(self):
        """Запускает следующий трек"""
        if not self.music_list:
            return

        # Если что-то играло — ставим на паузу (чтобы не было наслоения)
        if self.music_player:
            self.music_player.pause()

        song_path = self.music_list[self.current_song_index]
        song = arcade.load_sound(song_path)
        
        self.music_player = song.play(volume=0.1)
        
        self.current_song_index = (self.current_song_index + 1) % len(self.music_list)

    def on_update(self, delta_time):
        """Этот метод работает всегда, пока открыто окно"""
        # Если музыка затихла — включаем следующую
        if self.music_player and not self.music_player.playing:
            self.play_next_song()

def main():
    window = MyGame()
    menu = MenuView()
    window.show_view(menu)
    arcade.run()

if __name__ == "__main__":
    main()
