import cv2
import os

video_path = 'extract_frames/videos/video1.mp4' # video that will have frames extracted
output_folder = 'extract_frames/video1_frames' # folder that will hold the extracted frames

cap = cv2.VideoCapture(video_path)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) # 
frame_count = 0 # keeps track of current frame
forward_back = 1 # flag that determines whether to step forward or back in the video

while cap.isOpened():
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow('Frame', frame)

    key = cv2.waitKey(0) & 0xFF
    if key == ord(','):
        forward_back = -1
    elif key == ord('.'):
        forward_back = 1
    elif key == ord('z'):  # 'z' for 1 frame
        frame_count += 1 * forward_back
    elif key == ord('x'):  # 'x' 10 frames
        frame_count += 10 * forward_back
    elif key == ord('c'):  # 'c' for 100 frames
        frame_count += 100 * forward_back
    elif key == ord('v'):  # 'v' for 1000 frames
        frame_count += 1000 * forward_back
    elif key == ord('s'):  # 's' to save
        # saves image of frame as the name of the clip and frame number
        frame_path = f"{output_folder}/{os.path.splitext(os.path.basename(video_path))[0]}_frame{frame_count}.jpg"
        cv2.imwrite(frame_path, frame)
        print(f'Saved: {frame_path}')
    elif key == ord('q'):  # 'q' to quit
        break


cap.release()
cv2.destroyAllWindows()
