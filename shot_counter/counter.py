import cv2

# keeps track and draws the total and scored shots
class Counter:
    def __init__(self):
        self.total_shots = 0 
        self.scored_shots = 0

    def draw_shot_counter(self, frame):
        # draws the score tally 
        cv2.putText(frame, f'Score: {self.scored_shots}', (40, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,0), 10)
        cv2.putText(frame, f'Score: {self.scored_shots}', (40, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (100,255,100), 3)

        # draws the shots tally
        cv2.putText(frame, f'Shots: {self.total_shots}', (40, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,0), 10)
        cv2.putText(frame, f'Shots: {self.total_shots}', (40, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (100,100,255), 3)

        return frame
    
    # adds 1 to total shots
    def add_shots(self):
        self.total_shots += 1

    # adds 1 to scored shots
    def add_score(self):
        self.scored_shots += 1