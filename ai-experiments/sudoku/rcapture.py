import cv2
import pytesseract

#Absolute path to PyTesseract .exe file
pytesseract.pytesseract.Tesseract_cmd = ""

#initialize video stream
vstream = cv2.VideoCapture(0)

if not vstream.isOpened():
    vstream.release()
    #should write to a label(?)
    print("Error opening camera.")

grid_height, grid_width = 450, 450
v_width, v_height = int(vstream.get(3)), int(vstream.get(4))
font = cv2.FONT_HERSHEY_PLAIN



