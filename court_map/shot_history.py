import cv2
import numpy as np
from court_map import get_key_points

class shot_list:
    def __init__(self):
        self.positions = []

    def draw_shots(self,):
        return
        
    def add_shot(self, person_box, court_points, scored):
        if scored: 
            color = (0,255,0)
        else:
            color = (0,0,255)

        matrix = transformation_matrix(court_points, get_key_points())
        x1, y1, x2, y2 = map(int, person_box.xyxy[0].tolist())
        person_position = (x2 - ((x2 - x1) // 2), y2)

        print(map_position(person_position, matrix))
        self.positions.append(map_position(person_position, matrix))
            
    def draw_shots(self, frame):
        for shot_position in self.positions:
            cv2.circle(frame, shot_position, 3, (0,0,0), 40)

def transformation_matrix(court_points, map_points):
        court_points = np.float32(court_points)
        map_points = np.float32(map_points)
        matrix = cv2.getPerspectiveTransform(court_points, map_points)
        return matrix
    
def map_position(person_position, transformation_matrix):
    points = np.array([[person_position]], dtype=np.float32)
    transformed_points = cv2.perspectiveTransform(points, transformation_matrix)
    return tuple(map(int, transformed_points[0, 0]))