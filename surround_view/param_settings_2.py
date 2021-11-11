import os
import cv2

camera_names = ["front", "rear", "left", "right"]

# --------------------------------------------------------------------
# chessboard size
check_h = 175
check_w = 225

# (outher_width, outher_height): how far away the bird-view looks outside
# of the calibration pattern in horizontal and vertical directions
outher_w = 45
outher_h = 45

# Box size
box_h = 360
box_w = 310

# total width/height of the stitched image

total_w = 660 + 2 * outher_w  # 750
total_h = 855 + 2 * outher_h  # 945

# size of the gap between the calibration pattern and the car
# in horizontal and vertical directions
inner_w = int((total_w - outher_w * 2 - box_w - check_h * 2) / 2)
inner_h = int((total_h - outher_w * 2 - box_h - check_h * 2) / 2)

# four corners of the rectangular region occupied by the car
# top-left (x_left, y_top), bottom-right (x_right, y_bottom)
xl = check_h + outher_w + inner_w  # 310
xr = total_w - xl
yt = check_h + outher_h + inner_h
yb = total_h - yt
# --------------------------------------------------------------------

project_shapes = {
    "front": (total_w, yt),
    "rear":  (total_w, yt),
    "left":  (total_h, xl),
    "right": (total_h, xl),
}

# pixel locations of the four points to be chosen.
# you must click these pixels in the same order when running
# the get_projection_map.py script
project_keypoints = {
    "front": [(total_w/2 - check_w/2, outher_h), (total_w/2 + check_w/2, outher_h),
              (total_w/2 - check_w/2, outher_h + check_h), (total_w/2 + check_w/2, outher_h + check_h)],

    "left":  [(total_h/2 - check_w/2, outher_w), (total_h/2 + check_w/2, outher_w),
              (total_h/2 - check_w/2, outher_w + check_h), (total_h/2 + check_w/2, outher_w + check_h)],

    "right": [(total_h/2 - check_w/2, outher_w), (total_h/2 + check_w/2, outher_w),
              (total_h/2 - check_w/2, outher_w + check_h), (total_h/2 + check_w/2, outher_w + check_h)],

    "rear": [(total_w/2 - check_w/2, outher_h), (total_w/2 + check_w/2, outher_h),
             (total_w/2 - check_w/2, outher_h + check_h), (total_w/2 + check_w/2, outher_h + check_h)],
}
car_image = cv2.imread(os.path.join(os.getcwd(), "data", "box.png"))
car_image = cv2.resize(car_image, (xr - xl, yb - yt))
