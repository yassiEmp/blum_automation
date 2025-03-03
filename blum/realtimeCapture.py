import time
from mss import mss
import cv2 as cv
import numpy as np
import pygetwindow as gw

def realtimeCapture():
    # Find the Telegram window
    try:
        window = gw.getWindowsWithTitle("TelegramDesktop")[0]
    except IndexError:
        print("Telegram window not found")
        exit()

    with mss() as sct:
        while True:
            # Check if the window is still visible or minimized
            if not window.visible or window.isMinimized:
                print("Window is not visible or is minimized")
                break
            
            # Define the monitor region based on the window's position and size
            monitor = {
                "top": window.top,
                "left": window.left,
                "width": window.width,
                "height": window.height,
                "mon": -1  # Use -1 to capture the correct monitor dynamically
            }
            
            # Capture the screen and convert it to a numpy array
            img = np.array(sct.grab(monitor))
            
            yield img

            # Break the loop if 'q' is pressed
            if cv.waitKey(1) & 0xFF == ord("q"):
                break

    # Cleanup the OpenCV window
    cv.destroyAllWindows()

if __name__ == "__main__":
    realtimeCapture()
    # for img in realtimeCapture():
    #     cv.imshow("capture", cv.cvtColor(img, cv.COLOR_BGRA2BGR))
