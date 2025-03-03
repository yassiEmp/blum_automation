import cv2 as cv
import realtimeCapture
import pyautogui
import pygetwindow as gw

def findThepoint():
    capture = realtimeCapture.realtimeCapture()
    try:
        window = gw.getWindowsWithTitle("TelegramDesktop")[0]
    except IndexError:
        print("Telegram window not found")
        exit()

    # Load the template once in grayscale and resize for faster matching
    fleur = cv.imread("fleur.png", cv.IMREAD_GRAYSCALE)
    fleur_resized = cv.resize(fleur, (int(fleur.shape[1] * 0.5), int(fleur.shape[0] * 0.5)))

    for img in capture:
        # Convert the captured image to grayscale and downscale
        plan_gray = cv.cvtColor(img, cv.COLOR_BGRA2GRAY)
        plan_resized = cv.resize(plan_gray, (int(plan_gray.shape[1] * 0.5), int(plan_gray.shape[0] * 0.5)))

        # Perform template matching on the downscaled images
        result = cv.matchTemplate(plan_resized, fleur_resized, cv.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        threshold = 0.59

        if max_val <= threshold:
            print('No match found')
            cv.imshow("capture", cv.cvtColor(img, cv.COLOR_BGRA2BGR))  # Show original size
        else:
            # If matches are found, rescale the location to original size
            max_loc = (int(max_loc[0] * 2), int(max_loc[1] * 2))
            rectangle = [int(max_loc[0]), int(max_loc[1]), fleur.shape[1], fleur.shape[0]]

            # Draw the rectangle and perform the click
            point = (rectangle[0] + int(rectangle[2] / 2), rectangle[1] + int(rectangle[3] / 2))

            # Translate the click point to the window's position
            point = (point[0] + window.left+1, point[1] + window.top+4)
            pyautogui.moveTo(point)
            pyautogui.click()

        if cv.waitKey(1) & 0xFF == ord("q"):
            break

    cv.destroyAllWindows()

findThepoint()
