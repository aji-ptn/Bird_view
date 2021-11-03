import os
import cv2


camera_names = ["front", "rear", "left", "right"]

# --------------------------------------------------------------------
# chessboard size
# chess_h = 161
# chess_w = 208
chess_h = 175
chess_w = 225

# (shift_width, shift_height): how far away the bird-view looks outside
# of the calibration pattern in horizontal and vertical directions
# shift_w = 45
# shift_h = 45
shift_w = 45
shift_h = 45

# size of the gap between the calibration pattern and the car
# in horizontal and vertical directions
inn_shift_w = 30
inn_shift_h = 102

# total width/height of the stitched image

total_w = 660 + 2 * shift_w  # 750
total_h = 855 + 2 * shift_h  # 945

# four corners of the rectangular region occupied by the car
# top-left (x_left, y_top), bottom-right (x_right, y_bottom)

xl = chess_h + shift_w + inn_shift_w  # 310
xr = total_w - xl

yt = chess_h + shift_h + inn_shift_h
# yt = (yt)
yb = total_h - yt
print(yb)
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
total_h_half = int(total_h / 2)
chess_h_half = int(chess_h / 2)
total_w_half = int(total_w / 2)
chess_w_half = int(chess_w / 2)

project_keypoints = {
    "front": [(total_w_half - chess_w_half, shift_h), (total_w_half + chess_w_half, shift_h),
              (total_w_half - chess_w_half, shift_h + chess_h), (total_w_half + chess_w_half, shift_h + chess_h)],

    "left":  [(total_h_half - chess_w_half, shift_w), (total_h_half + chess_w_half, shift_w),
              (total_h_half - chess_w_half, shift_w + chess_h), (total_h_half + chess_w_half, shift_w + chess_h)],

    "right": [(total_h_half - chess_w_half, shift_w), (total_h_half + chess_w_half, shift_w),
              (total_h_half - chess_w_half, shift_w + chess_h), (total_h_half + chess_w_half, shift_w + chess_h)],

    "rear": [(total_w_half - chess_w_half, shift_h), (total_w_half + chess_w_half, shift_h),
             (total_w_half - chess_w_half, shift_h + chess_h), (total_w_half + chess_w_half, shift_h + chess_h)],
}

car_image = cv2.imread(os.path.join(os.getcwd(), "data", "car.png"))
car_image = cv2.resize(car_image, (xr - xl, int(yb - yt)))
