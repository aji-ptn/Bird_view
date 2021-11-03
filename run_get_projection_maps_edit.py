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


class Projection():
    def __init__(self):
        self.project_matrix = None
        self.camera_name = "right"
        self.folder_path = "sixth"
        self.alpha = -46.8
        self.beta = -1
        self.zoom = 3.5
        self.main()

    def get_projection_map(self, camera_name, image):
        name = camera_name
        gui = PointSelector(image, title=name)
        dst_points = settings.project_keypoints[name]
        choice = gui.loop()
        if choice > 0:
            src = np.float32(gui.keypoints)
            dst = np.float32(dst_points)
            self.project_matrix = cv2.getPerspectiveTransform(src, dst)
            proj_image = self.project(image, self.project_matrix, settings.project_shapes[camera_name])
            ret = display_image("Bird's View", proj_image)
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
        # image = self.get_anypoint(image)
        image = self.resize(image)
        success = self.get_projection_map(self.camera_name, image)
        cv2.imwrite("data/" + self.folder_path + "/undistortion/" + self.camera_name + ".png", image)
        if success:
            print("saving projection matrix to yaml")
            self.save_data(self.project_matrix)
        else:
            print("failed to compute the projection map")

    def resize(self, image):
        width = int(image.shape[1] / 2)
        height = int(image.shape[0] / 2)
        dim = (width, height)
        resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        return resized

    def get_anypoint(self, image):
        moildev = Moildev.Moildev("param.json")
        image = moildev.anypoint(image, self.alpha, self.beta, self.zoom, mode=2)
        return image

    def save_data(self, project_matrix):
        print("data/" + self.folder_path + "/yaml/" + self.camera_name + ".yaml")
        fs = cv2.FileStorage("data/" + self.folder_path + "/yaml/" + self.camera_name + ".yaml", cv2.FILE_STORAGE_WRITE)
        fs.write("project_matrix", project_matrix)
        fs.write("Alhpa ", self.alpha)
        fs.write("Beta ", self.beta)
        fs.write("Zoom ", self.zoom)
        fs.release()

    def project(self, image, matrix, shape):
        result = cv2.warpPerspective(image, matrix, shape)
        return result


if __name__ == '__main__':
    Projection()