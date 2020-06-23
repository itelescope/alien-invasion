import pygame.font

class Button:

    def __init__(self, ai_settings, screen, the_message):
        """Initialize button attribute."""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center # center is a predefined attribute; just revalue it!

        # The button message needs to be prepped only once.
        self.prep_msg(the_message)

    def prep_msg(self, the_message):
        """Turn message into a rendered image and center text on the button."""
        self.message_image = self.font.render(the_message, True,
                                                self.text_color, self.button_color)
        self.message_image_rect = self.message_image.get_rect()
        self.message_image_rect.center = self.rect.center # center is a predefined attribute; just revalue it.

    def draw_button(self):
        """Draw blank button and then draw the message."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.message_image, self.message_image_rect)
