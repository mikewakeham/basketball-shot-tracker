import math

# returns center coordinate of bounding box
def get_box_position(xyxy):
    x1, y1, x2, y2 = xyxy

    width = x2 - x1
    height = y2 - y1
    center_x = x1 + width // 2
    center_y = y1 + height // 2

    return (center_x, center_y)

# determines whether the ball is close enough to net to be considered a shot
def ball_near_net(ball_box, net_xyxy):
    # stores xyxy values of the ball bounding box
    x1, y1, x2, y2 = map(int, ball_box.xyxy[0].tolist())
    ball_xyxy = x1, y1, x2, y2 

    # stores position of the net and ball
    net_position = get_box_position(net_xyxy)
    ball_position = get_box_position(ball_xyxy)

    # stores distance between net and ball
    net_ball_distance = math.dist(net_position, ball_position)

    # threshold distance that marks the max distance between net and ball to be considered a shot
    # threshold is set to distance between center point of net and 3 widths of the net
    threshold_distance = abs(net_position[0] - (net_position[0] + 3*(net_xyxy[2]-net_xyxy[0])))

    # consider ball a shot if it is within the threshold distance and the ball is above the net
    if (net_ball_distance < threshold_distance and ball_xyxy[3] < net_position[1]):
        return True
    return False

def is_shot(ball_box, backboard_xyxy):
    ball_x1, ball_y1, ball_x2, ball_y2 = map(int, ball_box.xyxy[0].tolist())

    backboard_x1, backboard_y1, backboard_x2, backboard_y2, = backboard_xyxy

    if ball_x2 < backboard_x1 or backboard_x2 < ball_x1 or ball_y2 < backboard_y1 or backboard_y2 < ball_y1:
        return False
    return True
