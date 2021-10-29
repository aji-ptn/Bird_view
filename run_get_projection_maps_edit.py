"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Manually select points to get the projection map
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import os
import numpy as np
import cv2
from surround_view import FisheyeCameraModel, PointSelector, display_image
import surround_view.param_settings_2 as settings


def get_projection_map(camera_name, image):
    global project_matrix
    und_image = image
    # cv2.imwrite("undis.png", und_image)
    name = camera_name
    gui = PointSelector(und_image, title=name)
    dst_points = settings.project_keypoints[name]
    choice = gui.loop()
    if choice > 0:
        src = np.float32(gui.keypoints)
        dst = np.float32(dst_points)
        project_matrix = cv2.getPerspectiveTransform(src, dst)
        proj_image = project(und_image, project_matrix, settings.project_shapes[camera_name])


        ret = display_image("Bird's View", proj_image)
        cv2.imwrite("result/third/ " + camera_name + ".png", proj_image)
        print(proj_image.shape)
        if ret > 0:
            return True
        if ret < 0:
            cv2.destroyAllWindows()

    return False

# project_matrix = None


def main():
    global camera_name
    # scale = [0.7, 0.8]
    # shift = [0, 0]
    camera_name = "rear"
    # camera_file = os.path.join(os.getcwd(), "yaml/second", camera_name + ".yaml")
    image_file = os.path.join(os.getcwd(), "images/third", camera_name + ".png")
    image = cv2.imread(image_file)
    # camera = FisheyeCameraModel(camera_file, camera_name)
    # camera.set_scale_and_shift(scale, shift)
    # print(camera)
    success = get_projection_map(camera_name, image)
    if success:
        print("saving projection matrix to yaml")
        save_data(project_matrix)
    else:
        print("failed to compute the projection map")


def save_data(project_matrix):
    fs = cv2.FileStorage("yaml/third/" + camera_name + ".yaml", cv2.FILE_STORAGE_WRITE)
    # fs.write("camera_matrix", K)
    # fs.write("dist_coeffs", D)
    # fs.write("resolution", np.int32(gray.shape[::-1]))
    fs.write("project_matrix", project_matrix)
    # fs.write("scale_xy", np.float32(scale_xy))
    # fs.write("shift_xy", np.float32(shift_xy))
    fs.release()


def project(image, matrix, shape):
    result = cv2.warpPerspective(image, matrix, shape)
    return result



if __name__ == "__main__":
    main()
