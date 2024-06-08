# Chess themes module

class Themes:
    themes_names = ["Winter", "Fire"]
    themes = [{"untouched": {"white": (210, 220, 230), "black": (130, 155, 175)},
               "touched": {"white": (170, 220, 235), "black": (125, 185, 205)}, },

              {"untouched": {"white": (255, 220, 230), "black": (255, 155, 175)},
               "touched": {"white": (200, 180, 235), "black": (200, 140, 205)}}]
    current_theme_index = 0

    def set_next_theme(self):
        if self.current_theme_index < len(self.themes) - 1:
            self.current_theme_index += 1
        else:
            self.current_theme_index = 0

    def set_prev_theme(self):
        if self.current_theme_index > 0:
            self.current_theme_index -= 1
        else:
            self.current_theme_index = len(self.themes) - 1

    def get_current_theme(self):
        return self.themes[self.current_theme_index]
