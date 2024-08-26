# Tutorial: https://pygame-zero.readthedocs.io/en/stable/introduction.html
import pgzrun  # program must always start with this
from platformer import *

# our platformer constants
TILE_SIZE = 20
ROWS = 30
COLS = 20

# Pygame constants
WIDTH = TILE_SIZE * ROWS
HEIGHT = TILE_SIZE * COLS
TITLE = "Top-Down Perspective"

# global variables
jump_velocity = -10
gravity = 1
win = False
over = False

# build world
ground = build("topdown_ground.csv", 20)
walls = build("topdown_walls.csv", 20)
obstacles = build("topdown_obstacles.csv", 20)
hearts = build("topdown_hearts.csv", 20)

# define Sprites
# Sprite("sprite_image.png", start, num_frames, color_key, refresh)
color_key = (0, 0, 0)  # leave like this unless background shows up
idle = Sprite("player.png", (0, 0, 48, 48), 6, color_key, 5)
walk_down = Sprite("player.png", (0, 3 * 48, 48, 48), 6, color_key, 5)
walk_up = Sprite("player.png", (0, 5 * 48, 48, 48), 6, color_key, 5)
walk_left = Sprite("player.png", (0, 4 * 48, 48, 48), 6, color_key, 5)
walk_right = Sprite("player.png", (0, 4 * 48, 48, 48), 6, color_key, 5)
attach = Sprite("player.png", (0, 6 * 48, 48, 48), 4, color_key, 5)

# define SpriteActor
player = SpriteActor(idle)
player.bottomleft = (WIDTH / 2, HEIGHT - TILE_SIZE)
#player.scale = 3
# define Actor-specific variables
player.alive = True
player.jumping = False
player.velocity = 2
player.directions = ["idle"]


# displays the new frame
def draw():
    screen.clear()  # clears the screen
    screen.fill("lightslateblue")  # fills background color

    # draw ground
    for tile in ground:
        tile.draw()
    # draw walls
    for wall in walls:
        wall.draw()
    # draw obstacles
    for obstacle in obstacles:
        obstacle.draw()
    # draw hearts
    for heart in hearts:
        heart.draw()
    # draw the player if still alive
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
    if player.directions[-1] == "left" and player.left > 0:
        player.x -= player.velocity
        # flip image and change x velocity
        player.sprite = walk_left
        # if the movement caused a collision
        if player.collidelist(walls) != -1:
            # get object that player collided with
            collided = walls[player.collidelist(walls)]
            # use it to calculate position where there is no collision
            player.left = collided.right

    # handle player right movement
    if player.directions[-1] == "right" and player.right < WIDTH:
        player.x += player.velocity
        # flip image and change x velocity
        player.sprite = walk_right
        # if the movement caused a collision
        if player.collidelist(walls) != -1:
            # get object that player collided with
            collided = walls[player.collidelist(walls)]
            # use it to calculate position where there is no collision
            player.right = collided.left

    # handle player up movement
    if player.directions[-1] == "up" and player.top > 0:
        player.y -= player.velocity
        # flip image and change x velocity
        player.sprite = walk_up
        # if the movement caused a collision
        if player.collidelist(walls) != -1:
            # get object that player collided with
            collided = walls[player.collidelist(walls)]
            # use it to calculate position where there is no collision
            player.top = collided.bottom

    # handle player down movement
    if player.directions[-1] == "down" and player.bottom < HEIGHT:
        player.y += player.velocity
        # flip image and change x velocity
        player.sprite = walk_down
        # if the movement caused a collision
        if player.collidelist(walls) != -1:
            # get object that player collided with
            collided = walls[player.collidelist(walls)]
            # use it to calculate position where there is no collision
            player.bottom = collided.top

    # otherwise idle
    if player.directions[-1] == "idle":
        player.sprite = idle

    # player collided with obstacle, game over
    if player.collidelist(obstacles) != -1:
        player.alive = False
        over = True

    # check if player collected hearts
    for heart in hearts:
        if player.colliderect(heart):
            hearts.remove(heart)

    # check if player collected all hearts
    if len(hearts) == 0:
        win = True


# keyboard pressed event listener
def on_key_down(key):
    if key == keys.LEFT:
        player.directions.append("left")
    elif key == keys.RIGHT:
        player.directions.append("right")
    elif key == keys.UP:
        player.directions.append("up")
    elif key == keys.DOWN:
        player.directions.append("down")


# called when a keyboard button is released
def on_key_up(key):
    if key == keys.LEFT:
        player.directions.remove("left")
    elif key == keys.RIGHT:
        player.directions.remove("right")
    elif key == keys.UP:
        player.directions.remove("up")
    elif key == keys.DOWN:
        player.directions.remove("down")


pgzrun.go()  # program must always end with this
