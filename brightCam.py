import cv2
import numpy as np
import subprocess

originFactor = 0.4 #This number is added to correct the error
scaleFactor = 1/255 #This number helps to scale the final value between 0 and 1

#This function will help us to readjust the screen ratio
#Here cap is the Capture device initialized
def set_480p(cap):
    cap.set(3, 640)
    cap.set(4, 480)

#This function will take a snap and convert it to grayScale
def takeFrameMakeGray():
    _, frame = cap.read()
    return cv2.cvtColor(frame, cv2.CV_8UC3)
    #CV_8UC3 converts the images to grayscale

#This function returns the value of the brightness
#that is to be passed on to `xrandr`
def calculateBrightness(gray):
    brightnessMatrix = np.array(gray)
    pixels = np.count_nonzero(brightnessMatrix >= 0)
    sumOfBrightness = np.sum(brightnessMatrix)
    ratio = sumOfBrightness/pixels
    ratioInOne = ratio*scaleFactor
    return round(ratioInOne + originFactor, 2)

def findDisplayUnit():
    unit = subprocess.Popen(
        'xrandr | grep " connected" | cut -f1 -d " "',
        shell = True,
        stdout = subprocess.PIPE)
    #the unit.stdout.read() produces a byte-string with a new line character at the end
    #So, we execute the next line to avoid such difficulties
    displayUnit = unit.stdout.read().decode('utf-8').replace('\n', '')
    return displayUnit

if __name__ == '__main__':
    cap = cv2.VideoCapture(0) # This initializes the camera
    set_480p(cap)

    gray = takeFrameMakeGray()
    brightness = calculateBrightness(gray)

    displayUnit = findDisplayUnit()
    subprocess.call(
        f"xrandr --output {displayUnit} --brightness {brightness}",
        shell = True)
    #The above line sets the brightness by calling xrandr

    #Now let's free up the memory
    cap.release()
    cv2.destroyAllWindows()
