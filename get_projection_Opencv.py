"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Manually select points to get the projection map
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import os
import numpy as np
import cv2
from surround_view import PointSelector, display_image
import surround_view.param_settings_2 as settings
import Moildev

import os
print(os.getcwd())


class Projection():
    def __init__(self):
        self.project_matrix = None
        self.camera_name = "front"
        # --------------------------------------------
        self.folder_path = "thirteen (copy)"
        # self.scale_xy = (533.0850, 532.2079)
        # self.shift_xy = (1280.1692, 464.6976)
        # --------------------------------------------
        # self.folder_path = "twelveth"
        # self.calibration = "moildev"
        # self.alpha = 0
        # self.beta = 0
        # self.zoom = 3
        # --------------------------------------------
        # self.x = float(input("value : "))


        self.camera_matrix = None
        self.resolution = None
        self.dist_coeffs = None
        self.main()

    def get_projection_map(self, camera_name, image):
        name = camera_name
        gui = PointSelector(image, title=name)
        dst_points = settings.project_keypoints[name]
        choice = gui.loop()
        if choice > 0:
            src = np.float32(gui.keypoints)
            print(src)
            dst = np.float32(dst_points)
            print(dst)
            self.project_matrix = cv2.getPerspectiveTransform(src, dst)
            proj_image = self.project(image, self.project_matrix, settings.project_shapes[camera_name])
            ret = display_image("Bird's View", proj_image)
            proj_image = self.rotate(self.camera_name, proj_image)
            cv2.imwrite("data/" + self.folder_path + "/cutting/" + self.camera_name + ".png", proj_image)
            print(proj_image.shape)
            if ret > 0:
                return True
            if ret < 0:
                cv2.destroyAllWindows()
        return False

    def main(self):
        # image_file = os.path.join(os.getcwd(), "data/", self.folder_path, "/original/", self.camera_name + ".png")
        image_file = ("data/" + self.folder_path + "/original/" + self.camera_name + ".png")
        print(image_file)
        image = cv2.imread(image_file)
        self.load_parameter()
        image = self.update_undistortion(image)

        image = self.resize(image)
        success = self.get_projection_map(self.camera_name, image)
        cv2.imwrite("data/" + self.folder_path + "/undistortion/" + self.camera_name + ".png", image)
        if success:
            print("saving projection matrix to yaml")
            self.save_data()
        else:
            print("failed to compute the projection map")

    def rotate(self, camera_name, image):
        if camera_name == "front":
            return image.copy()
        elif camera_name == "rear":
            return image.copy()[::-1, ::-1, :]
        elif camera_name == "left":
            return cv2.transpose(image)[::-1]
        elif camera_name == "right":
            return np.flip(cv2.transpose(image), 1)
        else:
            return image.copy()

    def resize(self, image):
        width = int(image.shape[1] / 2)
        height = int(image.shape[0] / 2)
        dim = (width, height)
        print(dim)
        resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        return resized

    def load_parameter(self):
        calib = cv2.FileStorage("data/" + self.folder_path + "/yaml/" + self.camera_name + ".yaml", cv2.FILE_STORAGE_READ)
        # calib = cv2.FileStorage("calibration_entaniya.yaml", cv2.FILE_STORAGE_READ)
        self.camera_matrix = calib.getNode("camera_matrix").mat()
        self.dist_coeffs = calib.getNode("dist_coeffs").mat()
        self.resolution = calib.getNode("resolution").mat()
        self.new_camera_matrix = calib.getNode("new_camera_matrix").mat()
        print(self.new_camera_matrix)

        # project_matrix = calib.getNode("project_matrix").mat()
        # if project_matrix is not None:
        #     self.project_matrix = project_matrix

        calib.release()
        # self.create_matrix()

    def update_undistortion(self, image):
        self.new_matrix = self.camera_matrix.copy()
        self.new_matrix[0, 0] = self.new_camera_matrix[0][0]
        self.new_matrix[1, 1] = self.new_camera_matrix[1][1]
        self.new_matrix[0, 2] = self.new_camera_matrix[0][2]
        self.new_matrix[1, 2] = self.new_camera_matrix[1][2]
        width, hight = self.resolution
        dim = width*3.5, hight*2
        self.new_matrix[0, 2] = dim[0]/2
        # self.new_matrix[1, 2] = dim[0]/2
        print(width, hight)
        map1, map2 = cv2.fisheye.initUndistortRectifyMap(self.camera_matrix, self.dist_coeffs, np.eye(3), self.new_matrix,
                                                         dim, cv2.CV_16SC2)
        undistorted_img = cv2.remap(image, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        return undistorted_img

    def original_undistorted(self, image):
        width, hight = self.resolution
        map1, map2 = cv2.fisheye.initUndistortRectifyMap(self.camera_matrix, self.dist_coeffs, np.eye(3),
                                                         self.camera_matrix, (width, hight), cv2.CV_16SC2)
        undistorted_img = cv2.remap(image, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        return undistorted_img

    def save_data(self):
        print("data/" + self.folder_path + "/yaml/" + self.camera_name + ".yaml")
        fs = cv2.FileStorage("data/" + self.folder_path + "/yaml/" + self.camera_name + ".yaml", cv2.FILE_STORAGE_WRITE)
        fs.write("camera_matrix", self.camera_matrix)
        fs.write("dist_coeffs", self.dist_coeffs)
        fs.write("new_camera_matrix", self.new_camera_matrix)
        fs.write("resolution", self.resolution)
        fs.write("project_matrix", self.project_matrix)
        fs.release()

    def project(self, image, matrix, shape):
        result = cv2.warpPerspective(image, matrix, shape)
        return result


if __name__ == '__main__':
    Projection()