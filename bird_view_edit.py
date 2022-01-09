import os
import numpy as np
import cv2
from PIL import Image

# from surround_view.bird_code import Bird_View

from surround_view import display_image, bird_code
import surround_view.param_settings_2 as settings


class Bird_view_process():
    def __init__(self):
        self.names = settings.camera_names
        self.folder_path = "eleventh"
        self.birdview = bird_code.BirdView()
        self.main()

    def main(self):

        images = [os.path.join(os.getcwd(), "data/", self.folder_path + "/undistortion/" + name + ".png") for name in
                  self.names]
        yamls = [os.path.join(os.getcwd(), "data/", self.folder_path + "/yaml/" + name + ".yaml") for name in
                 self.names]

        projected = []
        for image_file, yamls, name in zip(images, yamls, self.names):
            img = cv2.imread(image_file)    # Read undistorted image
            matrix = self.read_matrix(yamls)    # read matrix
            shape = settings.project_shapes[name]   # take size for projection image

            img = self.project(img, matrix, shape)  # projection process
            cv2.imwrite("data/" + self.folder_path + "/cutting/" + name + ".png", img)
            img = self.rotate(name, img)    # rotate image
            projected.append(img)
        #
        # for project1, name in zip(projected, names):
        #     print(name)
        #     cv2.imwrite("data/" + folder_path + "/cutting/" + name + ".png", project1)
        #     cv2.imshow(name, project1)
        #     cv2.waitKey()

        Gmat, Mmat = self.birdview.get_weights_and_masks(projected)
        self.birdview.update_frames(projected)
        self.birdview.make_luminance_balance()
        self.birdview.stitch_all_parts()
        self.birdview.make_white_balance()
        self.birdview.copy_car_image()
        ret = display_image("BirdView Result", self.birdview.image)
        cv2.imwrite("data/" + self.folder_path + "/Resulttlaover.png", self.birdview.image)

        if ret > 0:
            Image.fromarray((Gmat * 255).astype(np.uint8)).save("weights.png")
            Image.fromarray(Mmat.astype(np.uint8)).save("masks.png")

    def project(self, image, matrix, shape):
        result = cv2.warpPerspective(image, matrix, shape)
        return result

    def read_matrix(self, file):
        fs = cv2.FileStorage(file, cv2.FILE_STORAGE_READ)
        matrix = fs.getNode("project_matrix").mat()
        beta = fs.getNode("beta").mat()
        print(beta)
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
    Bird_view_process()
