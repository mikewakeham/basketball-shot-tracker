import cv2
import matplotlib.pyplot as plt
import numpy as np 

def onclick(event, points, ax, fig):
    instructions = [
        "2nd point: right end of 3-point line",
        "3rd point: top-right of free-throw box",
        "4th point: top-left of free-throw box",
        "done!"
    ]

    ax.set_title(instructions[len(points)])
    if len(points) < 4:
        ix, iy = event.xdata, event.ydata
        ax.plot(ix, iy, 'ro')
        points.append((int(ix), int(iy)))
        fig.canvas.draw()
        print(f"selected point ({ix},{iy})")
    if len(points) == 4:
        plt.pause(0.5)
        plt.close(fig)

def select_points(video_path):
    video = cv2.VideoCapture(video_path)

    while True:
        try:
            frame_number = int(input("enter frame number to select points from: "))
            break
        except ValueError:
            print("enter integer value for frame number: ")

    video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    ret, frame = video.read()
    video.release()

    points = []
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        fig, ax = plt.subplots()
        ax.set_title("1st point: top of 3-point line")
        ax.imshow(frame)
        fig.canvas.mpl_connect('button_press_event', lambda event: onclick(event, points, ax, fig))
        plt.show()

        print("points:", points)
    else:
        print("couldnt read video")

    return points

def get_map_points():
    buffer = 20
    scale = 5
    half_court_length = 47 * scale
    court_width = 50 * scale
    top_left = (0 + buffer, 0 + buffer)
    bottom_right = (court_width + buffer, half_court_length + buffer)
    return top_left, bottom_right, scale

def get_key_points():
    top_left, bottom_right, scale = get_map_points()
    top_3point = (top_left[0] + (25 * scale), top_left[1] + (28 * scale))
    right_end_3point = (top_left[0] + (47 * scale), top_left[1])
    top_right_free_throw = (top_left[0] + 33 * scale, top_left[1] + 19 * scale)
    top_left_free_throw = (top_left[0] + 17 * scale, top_left[1] + 19 * scale)

    return (top_3point, right_end_3point, top_right_free_throw, top_left_free_throw)

def draw_court_map(frame):
    top_left, bottom_right, scale = get_map_points()
    line_color = (0,0,0)
    court_color = (150,205,227)
    line_thickness = scale // 2

    corner_length = scale * 14
    corner_width = scale * 3

    # draw court floor
    cv2.rectangle(frame, top_left, bottom_right, court_color, cv2.FILLED)

    # left corner line
    cv2.line(frame, (top_left[0] + corner_width, top_left[1]), (top_left[0] + corner_width, top_left[1] + corner_length), line_color, line_thickness)
    # right corner line
    cv2.line(frame, (bottom_right[0] - corner_width, top_left[1]), (bottom_right[0] - corner_width, top_left[1] + corner_length), line_color, line_thickness)

    # 3-point line arc
    center_position = (top_left[0] + (25 * scale), top_left[1] + (4 * scale))
    arc_radius = (24 * scale, 24 * scale)
    cv2.ellipse(frame, center_position, arc_radius, 0, 23, 157, line_color, line_thickness)

    # key rectangle
    key_top_left_point = (top_left[0] + 17 * scale, top_left[1])
    key_bottom_right_point = (top_left[0] + 33 * scale, top_left[1] + 19 * scale)
    key_circle_position = (top_left[0] + (25 * scale), top_left[1] + (19 * scale))
    key_circle_radius = (6 * scale, 6 * scale)

    cv2.rectangle(frame, key_top_left_point, key_bottom_right_point, line_color, line_thickness)
    cv2.ellipse(frame, key_circle_position, key_circle_radius, 0, 0, 180, line_color, line_thickness)

    # outline court
    cv2.rectangle(frame, top_left, bottom_right, line_color, line_thickness)

    return frame

