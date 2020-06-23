import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien

def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet."""
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, score_board, play_button, ship,
                 aliens, bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, score_board, play_button, ship,
                              aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, score_board, play_button,
                      ship, aliens, bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()
        
        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Reset the game statistics
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images.
        score_board.prep_score()
        score_board.prep_high_score()
        score_board.prep_level()
        score_board.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
              
def update_screen(ai_settings, screen, stats, score_board, ship, aliens,
                  bullets, play_button):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)

    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites(): # Group.sprite(): return >> """get a list of sprites in the group."""
        bullet.draw_bullet()
        
    ship.blitme()
    aliens.draw(screen)
    # When you call draw() on a group,
    # Pygame automatically draws each element in the group at the position
    # defined by its rect attribute.

    # Draw the score information.
    score_board.show_score()

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, score_board, ship, aliens,
                   bullets):
    """Update position of bullets and get rid of old bullets."""
    # Update bullet position.
    bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
            
    check_bullet_alien_collisions(ai_settings, screen, stats, score_board,
                                  ship, aliens, bullets)

def check_high_score(stats, score_board):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        score_board.prep_high_score()
    
def check_bullet_alien_collisions(ai_settings, screen, stats, score_board,
                                  ship, aliens, bullets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # """pygame.sprite.groupcollide(group_a, group_b, do_kill_a, do_kill_b):
    #    return dict;
    #    It returns a dictionary of all sprites in the first group that collide.
    #    The value for each item in the dictionary is a list of the sprites in
    #    the second group it collides with.
    #    """

    # Check whether the dictionary has value.
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            score_board.prep_score() # Create a new image for the updated score.
            # print(collisions) # See the len(aliens) and other details
        check_high_score(stats, score_board)

    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level.
        # Destroy existing bullets [= bullets that disappered but exist;
        # because of the memory], speed up the game, and create new fleet.
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level.
        stats.level += 1
        score_board.prep_level()
        
        create_fleet(ai_settings, screen, ship, aliens)

def get_aliens_number_in_row(ai_settings, alien_width):
    """Determine the number of aliens that fit in row."""
    available_space_x = ai_settings.screen_width
    aliens_number_in_row = available_space_x // (2 * alien_width)
    return aliens_number_in_row

def get_rows_number(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height - (3 * alien_height)
                         - ship_height)
    rows_number = int(available_space_y / (2 * alien_height))
    return rows_number

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    alien = Alien(ai_settings, screen)
    aliens_number_in_row = get_aliens_number_in_row(ai_settings,
                                                    alien.rect.width)
    rows_number = get_rows_number(ai_settings, ship.rect.height,
                                  alien.rect.height)
    for row_number in range(rows_number):
        for alien_number in range(aliens_number_in_row):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    """Respond appropraitely if any aliens have reached the edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
    
def ship_hit(ai_settings, screen, stats, score_board, ship, aliens, bullets):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        stats.ships_left -= 1

        # Update scoreboard.
        score_board.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        sleep(0.2)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, screen, stats, score_board, ship, aliens,
                        bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, score_board, ship, aliens,
                     bullets)
            break
    
def update_aliens(ai_settings, screen, stats, score_board, ship, aliens,
                  bullets):
    """Check if the fleet is at an edge,
         and then update the positions of all aliens in the fleet.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()    

    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, score_board, ship, aliens, bullets)
    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, screen, stats, score_board, ship, aliens,
                        bullets)
