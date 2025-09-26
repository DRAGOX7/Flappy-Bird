"""
                        MADE BY:
                        Aseel Mohammad Mahmoud Athamnh
                        ID : 173205
                        -
                        Abdullah Talal Abdullah Aljafari
                        ID : 169506
"""

import pygame
import random

################################################################
######################GAME VARIABLES############################
################################################################


# Initialize pygame
pygame.init()

# Controller setup
joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

# FPS Setting
clock = pygame.time.Clock()
FPS = 60

# Create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("WING JUMP")

# Load the icon image
icon_image = pygame.image.load("parallax/birdicon.png")

# Set the icon for the window
pygame.display.set_icon(icon_image)

# Define font
font = pygame.font.SysFont('Bauhaus 93', 60)

# Define color
white = (255, 255, 255)

# Define initial health
health_player1 = 4  # 4 for full health
health_player2 = 4  # 4 for full health

# Define game variables
scroll = 0
flying = False
game_over = False
pipe_gap = 200  # Adjust the pipe gap to increase the space between the pipes
score = 0
pass_pipe = False

pipe_frequency = 1100
last_pipe = pygame.time.get_ticks() - pipe_frequency

# Define scrolling speed in pixels per second
scroll_speed = 750

# adding sound effects
pygame.mixer.init()

flysound = pygame.mixer.Sound("parallax/wingsound.mp3")

pipe_collide = pygame.mixer.Sound('parallax/flappy_collide.mp3')

diesound = pygame.mixer.Sound("parallax/flappy_die.mp3")

# Set volume for sounds
flysound.set_volume(0.5)  # Set flying sound volume to 50%
pipe_collide.set_volume(0.5)  # Set pipe collision sound volume to 50%
diesound.set_volume(0.5)  # Set die sound volume to 50%

################################################################
######################GAME IMAGES###############################
################################################################


# Load button images
one_player_img = pygame.image.load("Parallax/one_player.png").convert_alpha()
two_player_img = pygame.image.load("Parallax/two_players.png").convert_alpha()
restart_img = pygame.image.load("Parallax/restart.png").convert_alpha()

# Load health bar images
healthred_full_img = pygame.image.load("Parallax/redfullhealth.png").convert_alpha()
healthred_half_img = pygame.image.load("Parallax/redhealthhalf.png").convert_alpha()
healthred_1health_img = pygame.image.load("Parallax/1healthbar.png").convert_alpha()
health_empty_img = pygame.image.load("Parallax/0health.png").convert_alpha()

# Load health bar images for player 2
healthgreen_full_img = pygame.image.load("Parallax/greenfullhealth.png").convert_alpha()
healthgreen_half_img = pygame.image.load("Parallax/greenhalfheal.png").convert_alpha()
healthgreen_1health_img = pygame.image.load("Parallax/greenhealth1hp.png").convert_alpha()

# Load ground images
ground_images = [
    pygame.image.load("Parallax/ground.png").convert_alpha(),
    pygame.image.load("Parallax/ground20.png").convert_alpha(),
    pygame.image.load("Parallax/ground30.png").convert_alpha(),
    pygame.image.load("Parallax/ground40.png").convert_alpha(),
    pygame.image.load("Parallax/ground20.png").convert_alpha(),
    pygame.image.load("Parallax/ground50.png").convert_alpha()
]

ground_width = ground_images[0].get_width()
ground_height = ground_images[0].get_height()

# Load background images
bg_images = [
    [pygame.image.load(f"Parallax/plx-{i}.png").convert_alpha() for i in range(1, 6)],
    [pygame.image.load(f"Parallax/plx2-{i}.png").convert_alpha() for i in range(1, 5)],
    [pygame.image.load(f"Parallax/plx3-{i}.png").convert_alpha() for i in range(1, 4)],
    [pygame.image.load(f"Parallax/plx4-{i}.png").convert_alpha() for i in range(1, 11)],
    [pygame.image.load(f"Parallax/plx5-{i}.png").convert_alpha() for i in range(1, 5)],
    [pygame.image.load(f"Parallax/plx6-{i}.png").convert_alpha() for i in range(1, 10)]
]

bg_width = bg_images[0][0].get_width()
bg_height = bg_images[0][0].get_height()


################################################################
######################GAME FUNCTIONS############################
################################################################


def draw_text(text, font, text_col, x, y):
    """
    Draw text on the screen.

    Args:
        text (str): Text to display.
        font (pygame.font.Font): Font object.
        text_col (tuple): Color of the text (RGB).
        x (int): X-coordinate of the text.
        y (int): Y-coordinate of the text.
    """

    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_health_bar(health, player):
    """
       Draw health bar for a player.

       Args:
           health (int): Health value.
           player (int): Player number (1 or 2).
   """

    if player == 1:
        pos = (20, 20)
        if health == 4:
            screen.blit(healthred_full_img, pos)
        elif health == 3:
            screen.blit(healthred_half_img, pos)
        elif health == 2:
            screen.blit(healthred_1health_img, pos)
        elif health == 1:
            screen.blit(health_empty_img, pos)
    elif player == 2:
        pos = (20, 80)  # Adjust position to display the second health bar below the first
        if health == 4:
            screen.blit(healthgreen_full_img, pos)
        elif health == 3:
            screen.blit(healthgreen_half_img, pos)
        elif health == 2:
            screen.blit(healthgreen_1health_img, pos)
        elif health == 1:
            screen.blit(health_empty_img, pos)


def reset_game():
    """
    Reset game variables and return score to reset score to zero.
    """

    global game_over, flying, pass_pipe, last_pipe, score, health_player1, health_player2

    # Reset pipes
    pipe_group.empty()

    # Reset bird position
    flappy.rect.x = 100
    flappy.rect.y = int(SCREEN_HEIGHT / 3)
    if len(bird_group) > 1:
        flappy2.rect.x = 100
        flappy2.rect.y = int(SCREEN_HEIGHT / 2)

    # Reset game variables

    score = 0
    game_over = False
    flying = False
    pass_pipe = False
    last_pipe = pygame.time.get_ticks() - pipe_frequency
    health_player1 = 4  # Reset health to full
    health_player2 = 4  # Reset health to full
    return score


def handle_collision(player):
    """
    Handle collision with pipes.

    Args:
        player (int): Player number (1 or 2).
    """

    global health_player1, health_player2, game_over, pipe_group, last_pipe

    # Reset bird position
    flappy.rect.x = 100
    flappy.rect.y = int(SCREEN_HEIGHT / 3)
    if len(bird_group) > 1:
        flappy2.rect.x = 100
        flappy2.rect.y = int(SCREEN_HEIGHT / 2)

    # Reset pipes
    pipe_group.empty()
    last_pipe = pygame.time.get_ticks() - pipe_frequency

    # Decrease health of the respective player
    if player == 1:
        health_player1 -= 1
        if health_player1 == 0:
            # Optionally set game_over to True here if needed
            pass  # Or handle the game over condition as per your game's logic
    elif player == 2:
        health_player2 -= 1
        if health_player2 == 0:
            # Optionally set game_over to True here if needed
            pass  # Or handle the game over condition as per your game's logic


def draw_bg():
    """
    Draw the background of the game.
    """

    # to determine which images set should appear
    bg_set_index = (score // 10) % len(bg_images)
    for i, bg_image in enumerate(bg_images[bg_set_index]):
        scroll_speed = 0.2 + 0.1 * i
        scaled_image = pygame.transform.scale(bg_image, (bg_width, SCREEN_HEIGHT))
        screen.blit(scaled_image, (
        (-scroll * scroll_speed) % bg_width - bg_width, 0))  # To cover far left and the speed of the scrolling
        screen.blit(scaled_image,
                    ((-scroll * scroll_speed) % bg_width, 0))  # To cover the middle and the speed of scrolling
        screen.blit(scaled_image, (
        (-scroll * scroll_speed) % bg_width + bg_width, 0))  # To cover far right and the speed of the scrolling


def draw_ground():
    """
    Draw the ground of the game.
    """

    # to determine which ground should appear
    ground_set_index = (score // 10) % len(ground_images)
    ground_image = ground_images[ground_set_index]

    total_ground_images = SCREEN_WIDTH // ground_image.get_width() + 2  # to cover the whole screen
    initial_ground_pos = (scroll * 0.6) % ground_image.get_width()  # the speed of scrolling

    # drawing the grounds
    for i in range(total_ground_images):
        screen.blit(ground_image,
                    ((i * ground_image.get_width() - initial_ground_pos), SCREEN_HEIGHT - ground_image.get_height()))


def main_menu():
    """
    Main menu of the game.
    """

    run = True
    while run:

        # Main menu background image
        screen.fill((0, 0, 0))
        draw_bg()

        # determining which game has been chosen
        if one_player_button.draw():
            run_game(1)
        if two_player_button.draw():
            run_game(2)

        # Game quitting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()


################################################################
######################GAME CLASSES##############################
################################################################


class Bird(pygame.sprite.Sprite):
    """
    Represents a bird in the game.
    """

    def __init__(self, x, y, bird_type):

        """
               Initialize Bird object.

               Args:
                   x (int): Initial x-coordinate of the bird.
                   y (int): Initial y-coordinate of the bird.
                   bird_type (int): Type of bird (1 or 2).
               """

        pygame.sprite.Sprite.__init__(self)
        # Load bird images based on type
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            if bird_type == 1:
                img = pygame.image.load(f'Parallax/bird{num}.png').convert_alpha()
            else:
                img = pygame.image.load(f'Parallax/bird_{num}.png').convert_alpha()
            self.images.append(img)
        # Set initial image and position
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        # Set initial velocity and button state
        self.vel = 0
        self.clicked = False
        self.button_pressed = False
        self.bird_type = bird_type

    def update(self):

        """
        Update the bird's position and animation.
        """

        global game_over
        if flying and not game_over:
            # Apply gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            self.rect.y += int(self.vel)

            # Check if bird hits the ground
            if self.rect.bottom >= SCREEN_HEIGHT - ground_height:
                self.rect.bottom = SCREEN_HEIGHT - ground_height
                self.vel = -10  # Play the die sound when bird hits the ground
                diesound.play()

            # Check if bird goes above the screen
            if self.rect.top <= 0:
                self.rect.top = 0
                self.vel = 0  # Stop upward movement
                self.vel = 5  # Start falling down

        if game_over:
            # Fall down if not already at the bottom
            if self.rect.bottom < SCREEN_HEIGHT - ground_height:
                self.rect.y += int(self.vel)
                self.vel = 0  # Stop upward movement
                self.vel = 5  # Start falling down
            else:
                # Ensure the bird stays at the bottom
                self.rect.bottom = SCREEN_HEIGHT - ground_height
            # Rotate the bird to indicate it has lost
            self.image = pygame.transform.rotate(self.images[self.index], -90)
        else:
            # Check for jump input
            keys = pygame.key.get_pressed()
            jump_pressed = False
            if self.bird_type == 1:
                jump_pressed = keys[pygame.K_SPACE]
                if joystick:
                    jump_pressed = jump_pressed or joystick.get_button(0)  # "X" button
                    jump_pressed = jump_pressed or joystick.get_button(1)  # "Square" button

            else:
                # For the second bird
                jump_pressed = keys[pygame.K_UP]
                if joystick:
                    jump_pressed = jump_pressed or joystick.get_button(2)  # "O" button
                    jump_pressed = jump_pressed or joystick.get_button(3)  # "Triangle" button

            if jump_pressed and not self.button_pressed:
                self.button_pressed = True
                self.vel = -10
                flysound.play()  # Play the flying sound
            if not jump_pressed:
                self.button_pressed = False

            # Handle the animation
            self.counter += 1
            flap_cooldown = 15

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # Rotation
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)


class Button():
    """
    Represents a button in the game.
    """

    def __init__(self, x, y, image):

        """
        Initialize Button object.

        Args:
            x (int): Initial x-coordinate of the button.
            y (int): Initial y-coordinate of the button.
            image (pygame.Surface): Image of the button.
        """

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):

        """
        Draw the button and check for mouse click.

        Returns:
            bool: True if the button is clicked, False otherwise.
        """

        action = False
        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Check if mouse is over the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True  # Button is clicked

        # Draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


# Create buttons
one_player_button = Button(SCREEN_WIDTH // 2 - 68, SCREEN_HEIGHT // 2 - 50, one_player_img)
two_player_button = Button(SCREEN_WIDTH // 2 - 68, SCREEN_HEIGHT // 2, two_player_img)
restart_button = Button(SCREEN_WIDTH // 2 - 68, SCREEN_HEIGHT // 2 - 50, restart_img)


class Pipe(pygame.sprite.Sprite):
    """
    Represents a pipe obstacle in the game.
    """

    def __init__(self, x, y, position):

        """
        Initialize Pipe object.

        Args:
            x (int): Initial x-coordinate of the pipe.
            y (int): Initial y-coordinate of the pipe.
            position (int): Position of the pipe (1 for top, -1 for bottom).
        """

        pygame.sprite.Sprite.__init__(self)
        # Load pipe image and set position based on input
        self.image = pygame.image.load('Parallax/pipe.png').convert_alpha()
        self.rect = self.image.get_rect()
        gap_size = 200  # Adjust this value to set the size of the gap

        if position == 1:
            # Top pipe position
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - gap_size + 100]
        elif position == -1:
            # Top pipe position
            self.rect.topleft = [x, y - 100]  # Adjust the position to make the pipe visible

    def update(self):

        """
        Update the position of the pipe.
        """

        if not game_over:
            # Move the pipe to the left
            self.rect.x -= scroll_speed * dt
            # Remove the pipe if it goes off the screen
            if self.rect.right < 0:
                self.kill()  # Remove the pipe from sprite group


################################################################
######################RUN GAME FUNCTION#########################
################################################################


def run_game(players):
    """
    Run the main game loop.

    Args:
        players (int): Number of players (1 or 2).
    """

    global scroll, flying, game_over, score, pass_pipe, last_pipe, pipe_group, flappy, flappy2, dt, health_player1, health_player2, scroll_speed, pipe_frequency, pipe_gap

    # Initialize game variables
    difficulty_increase_time = 20  # Time interval in seconds to increase difficulty
    last_difficulty_increase = pygame.time.get_ticks()

    scroll = 0
    flying = False
    game_over = False
    score = 0
    pass_pipe = False
    last_pipe = pygame.time.get_ticks() - pipe_frequency

    # Clear existing bird and pipe groups
    bird_group.empty()
    pipe_group.empty()

    # Create first bird
    flappy = Bird(100, int(SCREEN_HEIGHT / 3), 1)
    bird_group.add(flappy)

    # Create second bird if in two players mode
    if players == 2:
        flappy2 = Bird(100, int(SCREEN_HEIGHT / 2), 2)
        bird_group.add(flappy2)

    # Reset player health
    health_player1 = 4
    health_player2 = 4

    run = True
    return_to_menu = False

    # Main game loop
    while run:
        dt = clock.tick(FPS) / 1000.0  # Get elapsed time in seconds

        if not game_over:
            scroll += scroll_speed * dt  # Scroll the screen

        # Spawn pipes if game is not over and player is flying
        if not game_over and flying:
            time_now = pygame.time.get_ticks()  # Get current time
            if time_now - last_pipe > pipe_frequency:  # Check if it's time to spawn a new pipe
                pipe_height = random.randint(-100, 100)  # Generate random height for the gap between pipes
                btm_pipe = Pipe(SCREEN_WIDTH, SCREEN_HEIGHT - ground_height + pipe_height,
                                -1)  # Create bottom pipe at screen width, adjusted by ground height and pipe gap
                top_pipe = Pipe(SCREEN_WIDTH, SCREEN_HEIGHT - ground_height + pipe_height - pipe_gap,
                                1)  # Create top pipe with gap above bottom pipe
                pipe_group.add(btm_pipe)  # Add pipes to the pipe group
                pipe_group.add(top_pipe)  # Add pipes to the pipe group
                last_pipe = time_now  # Update time of last pipe spawn

        # Handle bird-ground collision
        if not game_over:
            for bird in bird_group:  # Iterate over each bird in the bird group
                if bird.rect.bottom >= SCREEN_HEIGHT - ground_height:  # Check if the bird's bottom edge has reached or passed the ground
                    bird.rect.bottom = SCREEN_HEIGHT - ground_height  # If yes, adjust the bird's position to stay above the ground
                    if len(bird_group) == 2:  # If there are two players, handle collision for each player separately
                        player_num = 1 if bird == flappy else 2  # Determine player number based on the bird's identity
                        handle_collision(player_num)  # Reduce health of the respective player
                        bird.rect.x = 100  # Reset bird's position
                        bird.rect.y = int(SCREEN_HEIGHT / 3) if player_num == 1 else int(
                            SCREEN_HEIGHT / 2)  # Reset bird's position
                    elif len(bird_group) == 1:  # If there is only one player, handle collision for that player
                        handle_collision(1)  # Reduce health of player 1
                        bird.rect.x = 100  # Reset the bird's position
                        bird.rect.y = int(SCREEN_HEIGHT / 3)  # Reset the bird's position

        if pygame.sprite.groupcollide(bird_group, pipe_group, False, False):  # Check for collision
            pipe_collide.play()  # Play the pipe collision sound
            for bird in pygame.sprite.groupcollide(bird_group, pipe_group, False,
                                                   False):  # Iterate over birds and pipes involved in collision
                player_num = 1 if bird == flappy else 2  # Determine player number based on the bird's identity
                handle_collision(player_num)  # Reduce health of the respective player

        # Increase game difficulty over time
        if pygame.time.get_ticks() - last_difficulty_increase > difficulty_increase_time * 1000:  # Check if it's time to increase difficulty based on elapsed time
            scroll_speed += 10  # Increase scroll speed
            pipe_frequency -= 75  # Decrease time between pipe spawns
            pipe_gap -= 10  # Decrease gap size between pipes
            last_difficulty_increase = pygame.time.get_ticks()  # Update the time of the last difficulty increase

        # Update bird and pipe positions
        bird_group.update()
        pipe_group.update()

        screen.fill((0, 0, 0))  # Clear screen before drawing
        draw_bg()  # Draw the background
        pipe_group.draw(screen)  # Draw pipes first
        draw_ground()  # Draw ground after pipes
        bird_group.draw(screen)  # draw all the sprites in the group onto screen

        # Draw health bars
        draw_health_bar(health_player1, 1)
        if players == 2:
            draw_health_bar(health_player2, 2)

        # Check the score
        if len(pipe_group) > 0:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                    and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and not pass_pipe:
                pass_pipe = True
            if pass_pipe:
                if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                    score += 1
                    pass_pipe = False

        draw_text(str(score), font, white, int(SCREEN_WIDTH / 2), 20)

        if health_player1 == 0 or health_player2 == 0:
            game_over = True

        # Check for game over and reset
        if game_over and len(bird_group) == 2:
            # Display winner text in two players mode only
            winner_text = font.render(f"Player {2 if health_player2 > 0 else 1} has won", True, white)
            screen.blit(winner_text, (SCREEN_WIDTH // 2 - winner_text.get_width() // 2, restart_button.rect.top - 90))
            # Display restart button
            if restart_button.draw():
                score = reset_game()

        # Display restart button and score in one player mode
        if game_over and len(bird_group) == 1:
            if restart_button.draw():
                score = reset_game()
            draw_text(f"Your Score: {score}", font, white, int(SCREEN_WIDTH / 2 - 140), restart_button.rect.top - 90)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not flying and not game_over:
                    flying = True
                if event.key == pygame.K_ESCAPE:
                    return_to_menu = True
                    run = False
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0 and not flying and not game_over:  # X button
                    flying = True
                elif event.button == 1 and not flying and not game_over:  # square button
                    flying = True
                elif event.button == 2 and not flying and not game_over:  # o button
                    flying = True
                elif event.button == 3 and not flying and not game_over:  # triangle button
                    flying = True

        # Update display
        pygame.display.update()

    # Return to main menu if requested
    if return_to_menu:
        main_menu()


# Initialize groups
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

# Run the main menu
main_menu()