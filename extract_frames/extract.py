import cv2
import os

# used to extract every 5 frames of a video and store it in random_output_frames
def extract_frames(input_video, output_folder, frame_step):
    vid = cv2.VideoCapture(input_video)

    frame_count = 0
    while(True):
        ret, frame = vid.read()

        if not ret:
            break
        
        # saves image of frame as the name of the clip and frame number
        if frame_count % frame_step == 0: 
            frame_filename = f"{output_folder}/{os.path.splitext(os.path.basename(input_video))[0]}_frame{frame_count}.jpg"
            cv2.imwrite(frame_filename, frame)

        frame_count += 1

    vid.release()

output_folder = 'extract_frames/random_output_frames' # folder that holds all extracted frames
input_video = 'extract_frames/videos/video1_clip1.mp4' # video to have its frames extracted
extract_frames(input_video, output_folder, 5)