
# Tutorial: https://pygame-zero.readthedocs.io/en/stable/introduction.html
import pgzrun  # o programa deve sempre começar com este
from platformer import *

# nossas constantes de plataforma
TILE_SIZE = 18
ROWS = 30
COLS = 20

# Constantes Pygame
WIDTH = TILE_SIZE * ROWS
HEIGHT = TILE_SIZE * COLS
TITLE = "Platformer"


#variáveis ​​globais
jump_velocity = -10
gravity = 1
win = False
over = False

# construir mundo
platforms = build("platformer_platforms.csv", 18)
obstacles = build("platformer_obstacles.csv", 18)
mushrooms = build("platformer_mushrooms.csv", 18)

# definir Sprites
# Sprite("sprite_image.png", start, num_frames, color_key, refresh)
color_key = (0, 0, 0)  # leave like this unless background shows up
fox_stand = Sprite("player.png", (0, 48, 48, 48), 6, color_key, 5)
fox_walk = Sprite("player.png", (0, 4 * 48 * 48, 48, 48), 6, color_key, 5)

# definir sprite dos atores
fox = SpriteActor(fox_stand)
fox.bottomleft = (0, HEIGHT)
fox.scale = 3
# definir variáveis ​​específicas do ator
fox.alive = True
fox.jumping = False
fox.velocity_x = 3
fox.velocity_y = 0


# exibe o novo quadro
def draw():
    screen.clear()  # clears the screen
    screen.fill("lightslateblue")  # fills background color
    # draw platforms
    for platform in platforms:
        platform.draw()
    # draw obstacles
    for obstacle in obstacles:
        obstacle.draw()
    # draw mushrooms
    for mushroom in mushrooms:
        mushroom.draw()
    # draw the fox if still alive
    if fox.alive:
        fox.draw()

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

    # handle fox left movement
    if keyboard.LEFT and fox.left > 0:
        fox.x -= fox.velocity_x
        # flip image and change sprite
        fox.sprite = fox_walk
        fox.flip_x = True
        # if the movement caused a collision
        if fox.collidelist(platforms) != -1:
            # get object that fox collided with
            collided = platforms[fox.collidelist(platforms)]
            # use it to calculate position where there is no collision
            fox.left = collided.right

    # handle fox right movement
    elif keyboard.RIGHT and fox.right < WIDTH:
        fox.x += fox.velocity_x
        # flip image and change sprite
        fox.sprite = fox_walk
        fox.flip_x = False
        # if the movement caused a collision
        if fox.collidelist(platforms) != -1:
            # get object that fox collided with
            collided = platforms[fox.collidelist(platforms)]
            # use it to calculate position where there is no collision
            fox.right = collided.left

    # handle gravity
    fox.y += fox.velocity_y
    fox.velocity_y += gravity
    # if the movement caused a collision, move position back
    if fox.collidelist(platforms) != -1:
        # get object that fox collided with
        collided = platforms[fox.collidelist(platforms)]
        # moving down - hit the ground
        if fox.velocity_y >= 0:
            # move fox up to no collision position
            fox.bottom = collided.top
            # no longer jumping
            fox.jumping = False
        # moving up - bumped their head
        else:
            # move fox down to no collision position
            fox.top = collided.bottom
        # reset velocity
        fox.velocity_y = 0

    # fox collided with obstacle, game over
    if fox.collidelist(obstacles) != -1:
        fox.alive = False
        over = True

    # check if fox collected mushrooms
    for mushroom in mushrooms:
        if fox.colliderect(mushroom):
            mushrooms.remove(mushroom)

    # check if fox collected all mushrooms
    if len(mushrooms) == 0:
        win = True


# keyboard pressed event listener
def on_key_down(key):
    # up key and not already jumping
    if key == keys.UP and not fox.jumping:
        fox.velocity_y = jump_velocity
        fox.jumping = True


# called when a keyboard button is released
def on_key_up(key):
    # change to forward facing image when left/right keys released
    if key == keys.LEFT or key == keys.RIGHT:
        fox.sprite = fox_stand


pgzrun.go()  # program must always end with this
