# Tutorial: https://pygame-zero.readthedocs.io/en/stable/introduction.html
import pgzrun  # program must always start with this
from platformer import *
#from pgzhelper import  *

# Pygame constants
WIDTH = 600
HEIGHT = 400
TITLE = "Platformer"

# global variables
jump_velocity = -10
gravity = 1
win = False
over = False
icon_coletado = False

# define Sprites
# Sprite("sprite_image.png", start, num_frames, color_key, refresh)
color_key = (0, 0, 0)  # leave like this unless background shows up
player_idle = Sprite("player.png", (0, 48, 48, 48), 6, color_key, 5)
player_walk = Sprite("player.png", (0, 4 * 48, 48, 48), 6, color_key, 5)

# define SpriteActor
player = SpriteActor(player_idle)
player.bottomleft = (0, HEIGHT - 60)
player.scale = 3
# define Actor-specific variables
player.alive = True
player.jumping = False
player.velocity_x = 3
player.velocity_y = 0

platforms = Actor("platform")
platforms.pos = (WIDTH / 2,HEIGHT - 18)


# displays the new frame
def draw():
    screen.clear()  # clears the screen
    screen.fill("skyblue")  # fills background color
    # draw the player if still alive
    if player.alive:
        player.draw()


    # draw messages over top
    if over:
        screen.draw.text("Game Over", center=(WIDTH / 2, HEIGHT / 2))
    if win:
        screen.draw.text("You win!", center=(WIDTH / 2, HEIGHT / 2))# Escreva o seu código aqui :-)


def update():
    # declare scope of global variables
    global win, over

    # if game is over, no more updating game state, just return
    if over or win:
        return

    # handle player left movement
    if keyboard.LEFT and player.left > 0:
        player.x -= player.velocity_x
        # flip image and change sprite
        player.sprite = player_walk
        player.flip_x = True


    elif keyboard.RIGHT and player.right < WIDTH:
        player.x += player.velocity_x
        # flip image and change sprite
        player.sprite = player_walk
        player.flip_x = False

    move_player()
        # handle gravity
    #player.y += player.velocity_y
    player.velocity_y += gravity

         # get object that fox collided with


# keyboard pressed event listener
def move_player():
    if keyboard.left:
        player.velocity_y = jump_velocity
        player.jumping = True
    elif keyboard.right:
        player.velocity_y = jump_velocity
        player.jumping = True
    else:
        player.sprite = player_idle

pgzrun.go()
