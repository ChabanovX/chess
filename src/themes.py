
class Themes:
    current_theme_index = 0
    themes = [
        {
            "name": "sky",
            "colors": {
                "untouched": {"white": (210, 220, 230), "black": (130, 155, 175)},
                "touched": {"white": (170, 220, 235), "black": (125, 185, 205)},
            }
        },
        
        {
            "name": "green",
            "colors": {
                "untouched": {"white": (232, 233, 203), "black": (110, 136, 77)},
                "touched": {"white": (243, 243, 138), "black": (182, 195, 75)},
            }
        },
        
        {
            "name": "brown",
            "colors": {
                "untouched": {"white": (230, 209, 169), "black": (168, 126, 90)},
                "touched": {"white": (242, 231, 121), "black": (211, 190, 81)},
            }
        },
    ]

    def set_next_theme(self):
        self.current_theme_index = (self.current_theme_index + 1) % len(self.themes)

    def set_prev_theme(self):
        self.current_theme_index = (self.current_theme_index - 1) % len(self.themes)

    def get_current_theme(self):
        return self.themes[self.current_theme_index]
