import cv2
import numpy as np
import sys


class Undistortion(object):
    def __init__(self):
        self.K = None
        self.D = None
        self.resolution = None
        self.image = "data/eleventh/original/left.png"
        self.image = cv2.imread(self.image)
        self.parameters_path = "calibrattion.yaml"
        self.read_parameter()
        self.dim_undistortion(self.image)

    def read_parameter(self):
        fs = cv2.FileStorage(self.parameters_path, cv2.FILE_STORAGE_READ)
        self.camera_matrix = fs.getNode("camera_matrix").mat()
        dist_coeffs = fs.getNode("dist_coeffs").mat()
        self.resolution = fs.getNode("resolution").mat().flatten()
        fs.release()
        self.K = np.array(self.camera_matrix)
        self.D = np.array(dist_coeffs)

    def calculate(self):
        # scale_x = float(input("scale x = "))
        # scale_y = float(input("scale y = "))
        # self.scale_xy = (scale_x, scale_y)
        #
        # shift_x = float(input("scale x = "))
        # shift_y = float(input("scale y = "))
        # self.shift_xy = (shift_x, shift_y)

        self.scale_xy = (1, 1)
        self.shift_xy = (0, 0)

        self.new_matrix = self.camera_matrix.copy()
        self.new_matrix[0, 0] *= self.scale_xy[0]
        self.new_matrix[1, 1] *= self.scale_xy[1]
        self.new_matrix[0, 2] += self.shift_xy[0]
        self.new_matrix[1, 2] += self.shift_xy[1]

        return self.new_matrix

    def undistortion(self, img_path):
        matrix = self.calculate()
        width = int(img_path.shape[1])
        height = int(img_path.shape[0])

        map1, map2 = cv2.fisheye.initUndistortRectifyMap(self.K, self.D, np.eye(3), matrix, (width, height), cv2.CV_16SC2)
        undistorted_img = cv2.remap(img_path, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        width = int(img_path.shape[1] / 2)
        height = int(img_path.shape[0] / 2)
        dim = (width, height)
        image = cv2.resize(undistorted_img, dim, interpolation=cv2.INTER_AREA)
        cv2.imshow("resiz", image)
        # cv2.waitKey()
        cv2.waitKey(0)
        # matrix = self.calculate()
        cv2.destroyAllWindows()

    def dim_undistortion(self, img_path, balance=0, dim2=None, dim3=None):
        width = int(img_path.shape[1])
        height = int(img_path.shape[0])
        DIM = (width, height)
        dim1 = self.image.shape[:2][::-1]  # dim1 is the dimension of input image to un-distort
        print(dim1)
        assert dim1[0] / dim1[1] == DIM[0] / DIM[1], "Image to undistort needs to have same aspect ratio as the ones used in calibration"
        if not dim2:
            dim2 = dim1
            print(dim2)
        if not dim3:
            dim3 = dim1
            print(dim3)
        scaled_K = self.K * dim1[0] / DIM[0]  # The values of K is to scale with image dimension.
        scaled_K[2][2] = 1.0  # Except that K[2][2] is always 1.0
        print(scaled_K)

        # This is how scaled_K, dim2 and balance are used to determine the final K used to un-distort image. OpenCV document failed to make this clear!
        new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K, self.D, dim2, np.eye(3), balance=balance)
        map1, map2 = cv2.fisheye.initUndistortRectifyMap(scaled_K, self.D, np.eye(3), new_K, dim3, cv2.CV_16SC2)
        undistorted_img = cv2.remap(self.image, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        width = int(self.image.shape[1] / 2)
        height = int(self.image.shape[0] / 2)
        dim = (width, height)
        image1 = cv2.resize(undistorted_img, dim, interpolation=cv2.INTER_AREA)
        # image2 = cv2.resize(self.image, dim, interpolation=cv2.INTER_AREA)
        cv2.imshow("undistorted", image1)
        # cv2.imshow("distorted", image2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()



if __name__ == '__main__':
    Undistortion()
