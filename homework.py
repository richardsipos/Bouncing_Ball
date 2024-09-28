import cv2
import numpy as np
import easygui
import random
import time

# Constants for window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
RACKET_WIDTH = 200
RACKET_HEIGHT = 40

# Color constants
GREEN_COLOR = (35, 250, 50)
BLUE_COLOR = (255, 0, 0)
RACKET_COLOR = (155, 100, 50)

# Global variables
game_canvas = None
x_ball_coord, y_ball_coord = 300, 100
game_on = True 
y_ball_direction = 1
x_ball_direction = 1

x_racket_top_left = (WINDOW_WIDTH // 2) - (RACKET_WIDTH // 2)  
y_racket_top_left = WINDOW_HEIGHT - 10 - RACKET_HEIGHT
y_racket_bottom_right = WINDOW_HEIGHT - 10  
ball_radius = 20



def redraw():
    global game_canvas
    
    game_canvas = np.zeros((WINDOW_HEIGHT-20, WINDOW_WIDTH-40, 3), dtype=np.uint8)
    cv2.circle(game_canvas, (x_ball_coord, y_ball_coord), ball_radius, (255, 0, 0), -1)
    x_racket_bottom_right = x_racket_top_left + RACKET_WIDTH
    
    # Create border in which game will be played
    border = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)
    border[:] = [30, 250, 60]
    
    # Draw the rocket
    cv2.rectangle(game_canvas, (x_racket_top_left, y_racket_top_left), (x_racket_bottom_right, y_racket_bottom_right), (155, 100, 50), -1)

    # Display the updated canvas
    y_offset = (border.shape[0] - game_canvas.shape[0])
    x_offset = (border.shape[1] - game_canvas.shape[1]) // 2
    border[y_offset:y_offset + game_canvas.shape[0], x_offset:x_offset + game_canvas.shape[1]] = game_canvas

    cv2.imshow("Display window", border)

def update_game_state():
    global x_ball_coord, y_ball_coord, game_on, y_ball_direction, x_ball_direction

    # Left and right wall collision
    if (x_ball_coord <= 20) or (x_ball_coord + ball_radius + 20 >= WINDOW_WIDTH-20):
        print("entered here", x_ball_coord, " coords ", y_ball_coord)
        x_ball_direction *= -1 
        
    
    # Top wall collision
    if y_ball_coord <= 20:
        y_ball_direction *= -1

    # Hit the racket, first win, then fail
    if (y_ball_coord + ball_radius >= y_racket_top_left) and (x_ball_coord + ball_radius >= x_racket_top_left) and (x_ball_coord - ball_radius <= x_racket_top_left + RACKET_WIDTH):
        y_ball_direction *= -1
    elif y_ball_coord >= WINDOW_HEIGHT - RACKET_HEIGHT:
        game_on = False
        easygui.msgbox("You lost the game!", title="Game Over")
        return False

    print(x_ball_direction, ", ", y_ball_direction)
    return True

# Mouse callback function
def MouseCallBackFunc(event, x, y, flags, userdata):
    global x_ball_coord, y_ball_coord, x_racket_top_left,y_racket_top_left, elapsed_time, current_time, last_update_time
    if event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):
        x_racket_top_left = max(0, min(x - (RACKET_WIDTH // 2), WINDOW_WIDTH - RACKET_WIDTH) - 40 )
        redraw()

def main():
    global x_ball_coord, y_ball_coord, game_on, x_racket_top_left, y_racket_top_left 
    # Create a black game_canvas
    # game_canvas = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)
    # Initial draw
    cv2.namedWindow("Display window", cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback("Display window", MouseCallBackFunc)

    redraw()  # Initial redraw, no need to assign to game_on here

    ball_speed = 2
    racket_speed = 10
    last_update_time = time.time()
    
    # Game loop
    while game_on:
        current_time = time.time()
        elapsed_time = current_time - last_update_time

        if elapsed_time >= 1/60:  # Cap at 60 FPS
            key = cv2.waitKey(1) & 0xFF

            y_ball_coord += ball_speed * y_ball_direction
            # if (x_ball_coord <= 29 and x_ball_coord > 20):
            #     x_ball_coord = 20 * x_ball_direction

            # if(x_ball_coord + ball_radius + 10 > WINDOW_WIDTH - 20 and x_ball_coord + ball_radius + 19 >= WINDOW_WIDTH-  20):
            #     x_ball_coord = WINDOW_WIDTH - 20 - ball_radius * x_ball_direction

            x_ball_coord += ball_speed * x_ball_direction
            print("racketleft: ", x_racket_top_left, " racketright: ", x_racket_top_left + RACKET_WIDTH)

            if key == 27:
                break
            elif key == ord('a') and x_racket_top_left >= 10:
                x_racket_top_left -= racket_speed
            elif key == ord('d') and x_racket_top_left + RACKET_WIDTH < WINDOW_WIDTH - 40:
                x_racket_top_left += racket_speed
            
            if not update_game_state():
                break

            redraw()
            last_update_time = current_time

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
