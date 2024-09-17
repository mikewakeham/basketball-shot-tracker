from ultralytics import YOLO 
import cv2
from draw import draw_bounding_box, RectangleStabilizer, BoxStabilizer, BackboardNetStabilizer, get_middle_position
from shot_detection import ball_near_net, is_shot
from shot_counter import Counter
from court_map import draw_court_map, select_points, shot_list
import math

model = YOLO('models/basketball_augmented.pt') # model for detecting basketball, net, backboard, and ball in net
input_path = "input_videos/basketball_clip1.mp4" # video being processed
output_path = "output_videos/example.mp4" # output video

def process_video(video_path, output_path, points):
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        print("could not open video")
        return
    
    fps = video.get(cv2.CAP_PROP_FPS) # video's FPS
    fourcc = cv2.VideoWriter_fourcc(*'XVID') 
    writer = cv2.VideoWriter(output_path, fourcc, fps, (int(video.get(3)), int(video.get(4))))

    frame_num = 0 # keeps track of current frame
    stabilizers = {} # dictionary to store stabilizer for each class
    shot = False # flag that keeps track of when ball is being shot
    counter = Counter() # keeps track of total and scored shots to be put onto screen
    last_shot_frame = -100 # stores index of last frame with shot flag set to True
    last_person_box = None
    shots = shot_list()

    while video.isOpened():
        ret, frame = video.read()

        if not ret:
            break

        # # start at frame 
        # if frame_num <= 1100:
        #     frame_num += 1
        #     continue

        # end at frame 
        if frame_num >= 65:
            break

        print (f"currently on frame {frame_num}")
        # adjust confidence and iou threshold to make model more selective
        results = model.predict(frame, conf=0.6, iou=0.4, save=False)

        # iterates through every box detected in the frame
        for box in results[0].boxes: 
            cls = int(box.cls[0]) # stores the class of the box 
            label = model.names[cls] # stores the name of the class



            # checks if this class is already in the stabilizers dictionary
            if label not in stabilizers: 
                # 'ball' and 'ball in net' classes use the box stabilizer
                if label == 'ball' or label == 'ball in net' or label == 'ball in hand': 
                    stabilizers[label] = BoxStabilizer()

                # 'net' and 'backboard' classes use the backboard and net stabilizer
                elif label == 'net' or label == 'backboard': 
                    stabilizers[label] = BackboardNetStabilizer()


            if label == 'ball in hand':
                first = True
                for person_box in results[0].boxes:
                    person_cls = int(box.cls[0]) # stores the class of the box 
                    person_label = model.names[person_cls] # stores the name of the class

                    if person_label == 'person':
                        if first:
                            last_person_box = person_box
                            first = False
                        else:
                            last_position = get_middle_position(last_person_box)
                            current_position = get_middle_position(person_box)
                            ball_position = get_middle_position(box)

                            if math.dist(last_position, ball_position) > math.dist(current_position, ball_position):
                                last_person_box = person_box



            # this section determines the status of a ball as being a shot or not a shot
            if label == 'ball': 
                # checks whether a position for the net exists and then determines if the ball is a shot
                if 'net' in stabilizers and ball_near_net(box, stabilizers['net'].get_position()):
                    # count the shot unless it has already been accounted for in the last 50 frames
                    if not shot and frame_num >= last_shot_frame + 50: 
                        counter.add_shots() 
                    shot = True # shot flag now True
                else:
                    # if the ball is ønot considered a shot in the current frame but was considered a shot in the previous one,
                    # update the variable that holds the index of the last shot frame 
                    if shot == True: 
                        last_shot_frame = frame_num - 1 
                        shots.add_shot(box, points, False)
                    shot = False # shot flag now False

            # if 'ball in net' is detected and the ball is determined to be a shot,
            # add 1 to scored tally and set the shot flag back to False
            if label == 'ball in net' and shot: 
                shot = False 
                shots.add_shot(box, points, True)
                counter.add_score() 

            # draw the bounding box for this box in the frame
            draw_bounding_box(frame, box, label, stabilizers[label])
            
            
        # draw 2d map of court
        draw_court_map(frame)

        # draw the counter for the frame
        # counter.draw_shot_counter(frame)

        # draw shots onto 2d map of court
        shots.draw_shots(frame)

        writer.write(frame)
        frame_num +=1
    
    video.release()
    writer.release()

points = select_points(input_path)

command = ""
while (command != quit):
    command = input("Type 'start' to begin video processing, 'redo' to restart selecting points, 'quit' to exit program\n")

    if command.lower() == "start":
        process_video(input_path, output_path, points)
    elif command.lower() == "redo":
        points = select_points(input_path)
    elif command.lower() == "quit":
        break
