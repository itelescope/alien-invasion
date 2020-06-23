import pygame.font
from ship import Ship
from pygame.sprite import Group

# The font.render()
# method also takes a Boolean value to turn antialiasing on or off
# (antialiasing makes the edges of the text smoother). The remaining
# arguments are the specified font color and background color.
# We set antialiasing to True

#     """pygame.font.render(text, antialias, color, background=None) -> Surface
#        draw text on a new Surface"""

# """pygame.font.SysFont(name, size, bold=False, italic=False,
#                          constructor=None) -> Font
#    create a pygame Font from system font resources
#    (freetype alternative)
#    ... """

class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ai_settings, screen, stats):
        """Initialize scorekeeping attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # Font settings for scoring information.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score images.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.ai_settings.bg_color)

        # Display score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        # y=0 is at the top; x=0 is at left,
        # so it is clear why we KNOW where put the top of scoreboard,
        # but not the right side of it, therefore we have to write it
        # in terms of the right side of screen_rect.
        

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        rounded_high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(rounded_high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                    self.text_color, self.ai_settings.bg_color)

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top

    def prep_level(self):
        """Turn the level into a rendered image."""
        level = self.stats.level
        level_str = str(level)
        self.level_image = self.font.render(level_str, True, self.text_color,
                                            self.ai_settings.bg_color)

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
            
        
    def show_score(self):
        """Draw scores and ships to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
            #"""draw all sprites onto the surface
            #   Group.draw(suface): return None
            #   Draws all of the member sprites onto the given surface.
            #   """
        

    
