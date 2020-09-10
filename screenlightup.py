import cv2
import numpy as np

scaleFactor = 15/255 #This number helps to scale the final value between 0 and 15

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
    #The count_nonzero method counts the number of elements in the array
    #This helps us to find the number of pixels in the array
    sumOfBrightness = np.sum(brightnessMatrix)
    #the numpy sum function helps us to get the sum all values in the numpy array
    ratio = sumOfBrightness/pixels #This will give the average brightness of a pixel
    ratioInFifteen = ratio*scaleFactor #Scales it from a range of 0-255 to 0-15
    return int(round(ratioInFifteen, 0))

if __name__ == '__main__':
    cap = cv2.VideoCapture(0) # This initializes the camera
    set_480p(cap)

    gray = takeFrameMakeGray()
    brightness = calculateBrightness(gray)

    with open('/sys/class/backlight/acpi_video0/brightness', 'w') as brightness_file:
        brightness_file.write(f'{brightness}')
    #The above line sets the brightness

    #Now let's free up the memory
    cap.release()
    cv2.destroyAllWindows()
