import cv2
import numpy as np
    
# turns the bounding box into a square and stabilizes it according to previous box sizes
class BoxStabilizer:
    def __init__(self, alpha=0.1):
        self.alpha = alpha # how much the average will change according to the most recent size given
        self.average = None # the running average

    # method for updating the stabilizer
    def update(self, size): 
        if self.average is None: 
            self.average = size # the very first bounding box size is set as the initial average
        else:
            # update the running average with the addition of the current size
            self.average = self.alpha * size + (1 - self.alpha) * self.average # changes in the average are scaled by alpha

        return int(self.average) 
    
# is the same stabilizer as BoxStabilizer but keeps the general shape
class RectangleStabilizer:
    def __init__(self, alpha=0.05):
        self.alpha = alpha # how much the average will change according to the most recent size given
        self.xaverage = None
        self.yaverage = None

    def update(self, x_length, y_length):
        if self.xaverage is None:
            self.xaverage = x_length
            self.yaverage = y_length
            
        else:
            self.xaverage = self.alpha * x_length + (1- self.alpha) * self.xaverage
            self.yaverage = self.alpha * y_length + (1- self.alpha) * self.yaverage
        return (int(self.xaverage), int(self.yaverage))
    
# sets the bounding box for the net and backboard depending on the highest confidence level box for each.
class BackboardNetStabilizer:
    def __init__(self):
        self.confidence = 0.5 # initial confidence level that must be surpassed
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
    
    # updates the old bounding box with the new one if the new confidence is higher than the old one
    def update(self, confidence, x1, y1, x2, y2):
        if confidence >= self.confidence or self.x1 == None:
            self.x1 = x1
            self.y1 = y1
            self.x2 = x2
            self.y2 = y2
            self.confidence = confidence
        return self.x1, self.y1, self.x2, self.y2
    
    # returns position for the bounding box
    def get_position(self): 
        return self.x1, self.y1, self.x2, self.y2
    
# helper function that returns the center coordinate of the bounding box
def get_middle_position(box):
    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

    width = x2 - x1
    height = y2 - y1
    center_x = x1 + width // 2
    center_y = y1 + height // 2

    return (center_x, center_y)

# function that stabilizes then draws the bounding box with its corresponding label and color
def draw_bounding_box(image, box, label='', stabilizer=None, color=(255,255,255)):
    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist()) # stores xyxy format of bounding box
    confidence = box.conf[0] # stores confidence of bounding box
    center_x, center_y = get_middle_position(box) # stores center position of bounding box

    # stabilizes box and sets corresponding color for 'ball' and 'ball in net'  
    if label == 'ball' or label == 'ball in net' or label == 'ball in hand': 
        if label == 'ball in hand': label = 'ball' # make 'ball in hand' drawn as just 'ball'
        if label == 'ball': color = (0,0,255) # set 'ball' color to red
        elif label == 'ball in net': color = (0,255,0) # set 'ball in net' color to green

        current_size = max(x2 - x1, y2 - y1) # finds the larger side of the rectangular bounding box
        stable_size = stabilizer.update(current_size) # uses that larger side to update stabilizer and get the stabilized size

        # sets new xyxy coordinates according to the stabilized sides
        x1 = center_x - stable_size // 2
        y1 = center_y - stable_size // 2
        x2 = center_x + stable_size // 2
        y2 = center_y + stable_size // 2

    # stabilizes box and sets corresponding color for 'backboard' and 'net'
    elif label == 'backboard' or label == 'net':
        if label == 'backboard': color = (255,165,0) # sets 'backboard' to sky blue
        else: color = (255,255,0) # sets 'net' to turquoise

        x1, y1, x2, y2 = stabilizer.update(confidence, x1, y1, x2, y2) # sets new xyxy coordinates 

    cv2.rectangle(image, (x1, y1), (x2, y2), color, 2) # draws the bounding box
    cv2.putText(image, f"{label} {confidence:.2f}%", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2) # draws the text label above box

    return image