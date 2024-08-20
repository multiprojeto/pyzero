#Assets
#https://craftpix.net/freebies/free-pixel-art-tiny-hero-sprites/
#https://craftpix.net/freebies/free-simple-platformer-game-kit-pixel-art/
#https://craftpix.net/file-licenses/
# Tutorial: https://pygame-zero.readthedocs.io/en/stable/introduction.html
import pgzrun
from platformer import *

# our platformer constants
TILE_SIZE = 16
ROWS = 30
COLS = 20

# Pygame constants
WIDTH = TILE_SIZE * ROWS
HEIGHT = TILE_SIZE * COLS
TITLE = "Platformer"


# global variables
jump_velocity = -10
gravity = 1
win = False
over = False

# build world
platforms = build("platformer_platforms.csv", 16)
bgs = build("platformer_bgs.csv", 16)
items = build("platformer_items.csv", 16)

# define Sprites
# Sprite("sprite_image.png", start, num_frames, color_key, refresh)
color_key = (0, 0, 0)  # leave like this unless background shows up
player_idle = Sprite("owlet_monster_idle.png", (0, 0, 32, 32), 4, color_key, 5)
player_walk = Sprite("owlet_monster_run.png", (0, 0, 32, 32), 6, color_key, 5)

# define SpriteActor
player = SpriteActor(player_idle)
player.bottomleft = (20, HEIGHT / 2)
# define Actor-specific variables
player.alive = True
player.jumping = False
player.velocity_x = 3
player.velocity_y = 0


# displays the new frame
def draw():
    screen.clear()  # clears the screen
    screen.fill("black")  # fills background col
    # draw platforms
    

    for bg in bgs:
        bg.draw()

    for platform in platforms:
        platform.draw()
        
    for item in items:
        item.draw()






    if player.alive:
        player.draw()

    # draw messages over top
    if over:
        screen.draw.text("Game Over", center=(WIDTH / 2, HEIGHT / 2))
    if win:
        screen.draw.text("You win!", center=(WIDTH / 2, HEIGHT / 2))



 # updates game state between drawing of each frame
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
        if player.collidelist(platforms) != -1:
            # get object that player collided with
            collided = platforms[player.collidelist(platforms)]
            # use it to calculate position where there is no collision
            player.left = collided.right


    elif keyboard.RIGHT and player.right < WIDTH:
        player.x += player.velocity_x
        # flip image and change sprite
        player.sprite = player_walk
        player.flip_x = False
        # if the movement caused a collision
        if player.collidelist(platforms) != -1:
            # get object that player collided with
            collided = platforms[player.collidelist(platforms)]
            # use it to calculate position where there is no collision
            player.right = collided.left

    # handle gravity
    player.y += player.velocity_y
    player.velocity_y += gravity
    # if the movement caused a collision, move position back
    if player.collidelist(platforms) != -1:
        # get object that player collided with
        collided = platforms[player.collidelist(platforms)]
        # moving down - hit the ground
        if player.velocity_y >= 0:
            # move player up to no collision position
            player.bottom = collided.top
            # no longer jumping
            player.jumping = False
        # moving up - bumped their head
        else:
            # move player down to no collision position
            player.top = collided.bottom
        # reset velocity
        player.velocity_y = 0
    # check if fox collected mushrooms
    for item in items:
        if player.colliderect(item):
            items.remove(item)

# keyboard pressed event listener
def on_key_down(key):
    # up key and not already jumping
    if key == keys.SPACE and not player.jumping:
        player.velocity_y = jump_velocity
        player.jumping = True


# called when a keyboard button is released
def on_key_up(key):
    # change to forward facing image when left/right keys released
    if key == keys.LEFT or key == keys.RIGHT:
        player.sprite = player_idle
pgzrun.go()  # program must always end with this
