"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Manually select points to get the projection map
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import argparse
import os
import numpy as np
import cv2
from surround_view import FisheyeCameraModel, PointSelector, display_image
import surround_view.param_settings as settings
from datetime import datetime
date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
print(f"filename_{date}")


def get_projection_map(camera_model, image):
    und_image = camera_model.undistort(image)
    name = camera_model.camera_name
    gui = PointSelector(und_image, title=name)
    dst_points = settings.project_keypoints[name]
    choice = gui.loop()
    if choice > 0:
        src = np.float32(gui.keypoints)
        dst = np.float32(dst_points)
        print(dst_points)
        # print(src)
        print(dst)
        camera_model.project_matrix = cv2.getPerspectiveTransform(src, dst)
        proj_image = camera_model.project(und_image)

        ret = display_image("Bird's View", proj_image)
        cv2.imwrite(f"result {date}.png", proj_image)
        if ret > 0:
            return True
        if ret < 0:
            cv2.destroyAllWindows()

    return False


def main():
    scale = [0.7, 0.8]
    shift = [-150, -100]
    camera_name = "left"
    camera_file = os.path.join(os.getcwd(), "yaml", camera_name + ".yaml")
    image_file = os.path.join(os.getcwd(), "images", camera_name + ".png")
    image = cv2.imread(image_file)
    camera = FisheyeCameraModel(camera_file, camera_name)
    camera.set_scale_and_shift(scale, shift)
    success = get_projection_map(camera, image)
    if success:
        print("saving projection matrix to yaml")
        camera.save_data()
    else:
        print("failed to compute the projection map")


if __name__ == "__main__":
    main()
