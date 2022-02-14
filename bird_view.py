import os
import numpy as np
import cv2
from PIL import Image

from surround_view import display_image, BirdView
import surround_view.param_settings_2 as settings


class Bird_view():
    def __init__(self):
        self.names = settings.camera_names
        self.folder_path = "thirteen"
        self.main()

    def main(self):
        names = settings.camera_names
        folder_path = "thirteen"  # ------------------------------------------------------------------------------
        images = [os.path.join(os.getcwd(), "data/", folder_path + "/undistortion/" + name + ".png") for name in self.names]
        yamls = [os.path.join(os.getcwd(), "data/", folder_path + "/yaml/" + name + ".yaml") for name in self.names]

        projected = []
        for image_file, yamls, name in zip(images, yamls, names):
            img = cv2.imread(image_file)
            matrix = self.read_matrix(yamls)
            shape = settings.project_shapes[name]

            img = self.project(img, matrix, shape)
            img = self.rotate(name, img)

            projected.append(img)
        #
        # for project1, name in zip(projected, names):
        #     print(name)
        #     cv2.imwrite("data/" + folder_path + "/cutting/" + name + ".png", project1)
        #     cv2.imshow(name, project1)
        #     cv2.waitKey()

        birdview = BirdView()
        Gmat, Mmat = birdview.get_weights_and_masks(projected)
        birdview.update_frames(projected)
        birdview.make_luminance_balance().stitch_all_parts()
        birdview.make_white_balance()
        birdview.copy_car_image()
        ret = display_image("BirdView Result", birdview.image)
        cv2.imwrite("data/" + folder_path + "/Resulttla.png", birdview.image)

        if ret > 0:
            Image.fromarray((Gmat * 255).astype(np.uint8)).save("weights.png")
            Image.fromarray(Mmat.astype(np.uint8)).save("masks.png")

    def project(self, image, matrix, shape):
        result = cv2.warpPerspective(image, matrix, shape)
        return result

    def read_matrix(self, file):
        fs = cv2.FileStorage(file, cv2.FILE_STORAGE_READ)
        matrix = fs.getNode("project_matrix").mat()
        return matrix

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


if __name__ == "__main__":
    Bird_view()
