import os
import cv2


camera_names = ["front", "back", "left", "right", "eta_front"]

# --------------------------------------------------------------------
# (shift_width, shift_height): how far away the birdview looks outside
# of the calibration pattern in horizontal and vertical directions
shift_w = 300
shift_h = 300

# size of the gap between the calibration pattern and the car
# in horizontal and vertical directions
inn_shift_w = 20
inn_shift_h = 50

# total width/height of the stitched image
total_w = 600 + 2 * shift_w  # 1200
total_h = 1000 + 2 * shift_h  # 1600

# four corners of the rectangular region occupied by the car
# top-left (x_left, y_top), bottom-right (x_right, y_bottom)
xl = shift_w + 180 + inn_shift_w  # 500
xr = total_w - xl  # 500
yt = shift_h + 200 + inn_shift_h  # 550
yb = total_h - yt  # 550
# --------------------------------------------------------------------

project_shapes = {
    "front": (total_w, yt),
    "back":  (total_w, yt),
    "left":  (total_h, xl),
    "right": (total_h, xl),
    "eta_front": (total_h, yt)
}

# pixel locations of the four points to be chosen.
# you must click these pixels in the same order when running
# the get_projection_map.py script
project_keypoints = {
    "front": [(shift_w + 120, shift_h),
              (shift_w + 480, shift_h),
              (shift_w + 120, shift_h + 160),
              (shift_w + 480, shift_h + 160)],

    "back":  [(shift_w + 120, shift_h),
              (shift_w + 480, shift_h),
              (shift_w + 120, shift_h + 160),
              (shift_w + 480, shift_h + 160)],

    "left":  [(shift_h + 280, shift_w),
              (shift_h + 840, shift_w),
              (shift_h + 280, shift_w + 160),
              (shift_h + 840, shift_w + 160)],

    "right": [(shift_h + 160, shift_w),
              (shift_h + 720, shift_w),
              (shift_h + 160, shift_w + 160),
              (shift_h + 720, shift_w + 160)],


    "eta_front": [(shift_w + 120, shift_h),
                  (shift_w + 480, shift_h),
                  (shift_w + 120, shift_h + 160),
                  (shift_w + 480, shift_h + 160)],

    "eta_front": [(shift_w + 120, shift_h),
                  (shift_w + 480, shift_h),
                  (shift_w + 120, shift_h + 160),
                  (shift_w + 480, shift_h + 160)],

    "eta_front": [(shift_w + 120, shift_h),
                  (shift_w + 480, shift_h),
                  (shift_w + 120, shift_h + 160),
                  (shift_w + 480, shift_h + 160)],

    "eta_front": [(shift_w + 120, shift_h),
                  (shift_w + 480, shift_h),
                  (shift_w + 120, shift_h + 160),
                  (shift_w + 480, shift_h + 160)],

}

car_image = cv2.imread(os.path.join(os.getcwd(), "images", "car.png"))
car_image = cv2.resize(car_image, (xr - xl, yb - yt))
