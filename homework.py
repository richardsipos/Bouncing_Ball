import cv2
import numpy as np
import easygui
import time

# Constants for window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
RACKET_WIDTH = 200
RACKET_HEIGHT = 20

# Color constants
BORDER_COLOR = (255, 128, 0)
BLUE_COLOR = (255, 255, 0)
RACKET_COLOR = (255, 128, 0)

# Global variables
game_canvas = None
x_ball_coord, y_ball_coord = 300, 100
y_ball_direction = 1
x_ball_direction = 1

x_racket_top_left = (WINDOW_WIDTH // 2) - (RACKET_WIDTH // 2)  
y_racket_top_left = WINDOW_HEIGHT - 10 - RACKET_HEIGHT
y_racket_bottom_right = WINDOW_HEIGHT - 10  
ball_radius = 20


    

def redraw():

    global game_canvas, x_ball_coord, y_ball_coord, x_racket_top_left, y_racket_top_left, y_racket_bottom_right, border
    
    game_canvas = np.zeros((WINDOW_HEIGHT-20, WINDOW_WIDTH-40, 3), dtype=np.uint8)
    cv2.circle(game_canvas, (x_ball_coord, y_ball_coord), ball_radius, BLUE_COLOR, -1)

    # Draw the racket
    x_racket_bottom_right = x_racket_top_left + RACKET_WIDTH
    cv2.rectangle(game_canvas, (x_racket_top_left, y_racket_top_left), (x_racket_bottom_right, y_racket_bottom_right), RACKET_COLOR, -1)

    border = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)
    border[:] = BORDER_COLOR
    y_offset = (border.shape[0] - game_canvas.shape[0])
    x_offset = (border.shape[1] - game_canvas.shape[1]) // 2
    border[y_offset:y_offset + game_canvas.shape[0], x_offset:x_offset + game_canvas.shape[1]] = game_canvas

def update_game_state():
    global x_ball_coord, y_ball_coord, x_ball_direction, y_ball_direction 

    # Left and right wall touch
    if (x_ball_coord <= 20) or (x_ball_coord + ball_radius + 20 >= WINDOW_WIDTH-20):
        x_ball_direction *= -1 
    
    # Upper wall touch
    if y_ball_coord <= 20:
        y_ball_direction *= -1

    # Racket touch
    if(y_ball_coord + ball_radius >= y_racket_top_left and y_ball_coord + ball_radius <= y_racket_bottom_right) and (x_ball_coord + ball_radius >= x_racket_top_left) and (x_ball_coord - ball_radius <= x_racket_top_left + RACKET_WIDTH):
        y_ball_direction = -1
    elif (y_ball_coord + ball_radius >= y_racket_top_left) and (x_ball_coord + ball_radius >= x_racket_top_left) and (x_ball_coord - ball_radius <= x_racket_top_left + RACKET_WIDTH):
        y_ball_direction *= -1
    elif y_ball_coord >= WINDOW_HEIGHT - RACKET_HEIGHT:
        easygui.msgbox("You lost the game!", title="Game Over")
        return False

    return True

# Mouse event
def MouseCallBackFunc(event, x, y, flags, userdata):
    global x_racket_top_left
    if event == cv2.EVENT_MOUSEMOVE:
        x_racket_top_left = max(0, min(x - (RACKET_WIDTH // 2), WINDOW_WIDTH - RACKET_WIDTH) - 40)

def main():
    global x_ball_coord, y_ball_coord, x_racket_top_left

    # Create a window and mouse event
    cv2.namedWindow("Display window", cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback("Display window", MouseCallBackFunc)

    # Set the ball and racket speed
    ball_speed = 2
    racket_speed = 10

    # Inifinite loop for the game
    while True:
        start_time = time.time()
        # Keyboard event
        key = cv2.waitKey(1) & 0xFF

        # Ball movement
        y_ball_coord += ball_speed * y_ball_direction
        x_ball_coord += ball_speed * x_ball_direction

        # Keyboard controls for the racket
        if key == 27:  # Escape key to exit
            break
        elif key == ord('a') and x_racket_top_left >= 10:
            x_racket_top_left -= racket_speed
        elif key == ord('d') and x_racket_top_left + RACKET_WIDTH < WINDOW_WIDTH - 40:
            x_racket_top_left += racket_speed
        elif key == ord('a') and x_racket_top_left >= 0:
            x_racket_top_left = 0
        elif key == ord('d') and x_racket_top_left + RACKET_WIDTH >= WINDOW_WIDTH:
            x_racket_top_left = WINDOW_WIDTH - RACKET_WIDTH - 40

        # Check the game state, if the game persists
        if not update_game_state():
            break

        # Redraw the game elements
        redraw()

        cv2.imshow("Display window", border)

        # Ensure a consistent frames
        time.sleep(max(0.01 - (time.time() - start_time), 0))

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
