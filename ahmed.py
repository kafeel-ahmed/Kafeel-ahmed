
# SNAKES GAME
# Use ARROW KEYS to play, SPACE BAR for pausing/resuming and Esc Key for exiting
# Adapted from https://gist.github.com/sanchitgangwar/2158089

import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint, choice

def update_anim(snake, key, symbol):
    # Calculates the new coordinates of the head of the snake.
    snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1), snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)])

    # If snake crosses the boundaries, make it enter from the other side
    if snake[0][0] == 0: snake[0][0] = 18
    if snake[0][1] == 0: snake[0][1] = 58
    if snake[0][0] == 19: snake[0][0] = 1
    if snake[0][1] == 59: snake[0][1] = 1

    # Exit if snake crosses the boundaries (Uncomment to enable)
    #if snake[0][0] == 0 or snake[0][0] == 19 or snake[0][1] == 0 or snake[0][1] == 59: break

    last = snake.pop()
    win.addch(last[0], last[1], ' ')
    win.addch(snake[0][0], snake[0][1], symbol)


def get_dir(first, second, dir):
    """ dir should be "towards" if second should move towards first
    or "away" if second should move away from first
    if first is to the NW of second, xdif and ydif are neg."""
    x_dif = first[1]-second[1]
    y_dif = first[0]-second[0]
    if abs(x_dif) >= abs(y_dif):
        if dir == "towards":
            if x_dif<0:
                return KEY_LEFT
            else:
                return KEY_RIGHT
        else:
            if x_dif<0:
                return KEY_RIGHT
            else:
                return KEY_LEFT
    else:
        if dir == "towards":
            if y_dif<0:
                return KEY_UP
            else:
                return KEY_DOWN
        else:
            if x_dif<0:
                return KEY_DOWN
            else:
                return KEY_UP


def get_next_move(you, enemy, food):
    if randint(0,3)==0: # move randomly 1/4 of the time
        return(choice(key_choices), choice(key_choices))
    else:   # move in the best direction
        return(get_dir(you, enemy, "towards"), get_dir(you, food, "away"))


curses.initscr()
win = curses.newwin(20, 60, 0, 0)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)

key = KEY_RIGHT                                                    # Initializing values
score = 0
endgame = False
key_choices = [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN]

you = [[4,10]]                                     # Initial snake co-ordinates
enemy = [[15,30]]
food = [[11,20]]                                                     # First food co-ordinates

win.addch(you[0][0], you[0][1], 'o')
win.addch(food[0][0], food[0][1], '*')                                   # Prints the food
win.addch(enemy[0][0], enemy[0][1], 'X')

try:
    while key != 27 and endgame == False:                                                   # While Esc key is not pressed


        win.border(0)
        win.addstr(0, 2, 'Score : ' + str(score) + ' ')                # Printing 'Score' and
        win.addstr(0, 27, " Holly's Game ")
        win.timeout(520)          # Increases the speed of Snake as its length increases

        prevKey = key                                                  # Previous key pressed
        event = win.getch()
        key = key if event == -1 else event


        if key == ord(' '):                                            # If SPACE BAR is pressed, wait for another
            key = -1                                                   # one (Pause/Resume)
            while key != ord(' '):
                key = win.getch()
            key = prevKey
            continue

        if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:     # If an invalid key is pressed
            key = prevKey

        update_anim(you, key, 'o')
        if you[0] == enemy[0]:
            endgame = True
        if you[0] == food[0]:                                            # When snake eats the food
            food = []
            score += 1
            while food == []:
                food = [[randint(1, 18), randint(1, 58)]]                 # Calculating next food's coordinates
                if food in you: food = []
            win.addch(food[0][0], food[0][1], '*')

        enemy_move, food_move = get_next_move(you[0], enemy[0], food[0])

        update_anim(enemy, enemy_move, 'X')
        if you[0] == enemy[0]:
            endgame = True

        update_anim(food, food_move, '*')    #choice(key_choices)
        if you[0] == food[0]:                                            # When snake eats the food
            food = []
            score += 1
            while food == []:
                food = [[randint(1, 18), randint(1, 58)]]                 # Calculating next food's coordinates
                if food in you: food = []
            win.addch(food[0][0], food[0][1], '*')


finally:
    curses.endwin()
    print("\nScore - " + str(score))
