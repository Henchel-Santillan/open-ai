import cv2
import numpy as np

def process_core(image):
    '''
    Returns an inverted preprocessed binary image, with noise
    reduction achieved with greyscaling, Gaussian Blur, Otsu's Threshold, and 
    an open morph.
    '''
    #apply greyscaling, Gaussian Blur, and Otsu's Threshold
    greyscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(greyscale, (3, 3), 0)
    threshold = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    
    #apply an open morph to invert image to remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    invert = 255 - cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel, iterations=1)
    
    return invert

def find_houghlines(image, width, height):
    hough_lines = None
    
    lines = cv2.HoughLinesP(image, 1, np.pi/180, 50, minLineLength=50, maxLineGap=5)
    
    #generates blank black image with single color layer
    if lines is not None and len(lines) != 0:
        hough_lines = np.zeros((height, width), dtype=np.uint8)
        
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(hough_lines, (x1, y1), (x2, y2), (255, 255, 255), 2)
        
    return hough_lines

def find_bounds(image):
    rect_bounds = None
    
    #Run contour recognition
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    #Take list of sorted contours by largest area to smallest area
    #If at least one contour is identified, can process visual approx. of contour bounds
    if len(sorted(contours, key=cv2.contourArea, reverse=True)) > 0:
        contour_bounds = None
        #Pre-determined image size factor constant
        SFACTOR = 20  
        
        for contour in contours:
            #Minimum intended size of a single cell is not reached, likely a cutoff, not worth approx.
            if (image[0] * image[1]) / SFACTOR > cv2.contourArea(contour):
                break
            
            approximation = cv2.approxPolyDP(contour, cv2.arcLength(contour, True), True)
            
            #This means that the approximated polygon is a quad
            if len(approximation) == 4:
                contour_bounds = approximation
                break 
            
        if contour_bounds is not None:
            rect_bounds = np.zeros((4, 2), dtype=np.float32)
            corners = contour_bounds.reshape(-1, 2)
            
            rect_bounds[0] = corners[np.argmin(contour_bounds.sum(axis=1))]
            rect_bounds[2] = corners[np.argmax(contour_bounds.sum(axis=1))]
            
            rect_bounds[1] = corners[np.argmin(np.diff(corners, axis=1))]
            rect_bounds[3] = corners[np.argmax(np.diff(corners, axis=1))]
            
    return rect_bounds

#Transform the perspective to render as if looking down on paper (top-down view)
def transform(image, perspective):
    pass

#Process the grid based on expected clean binary image input
def process_grid(image, width, height):
    grid = None
    detected = False
    
    hough_lines = find_houghlines(image, width, height)
    
    


