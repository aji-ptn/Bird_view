# import necessary libraries

import cv2
import numpy as np


class perspective_click():
    def __init__(self):
        self.img = cv2.imread("/home/aji/Documents/Data for Homography/10-02-2022/front/021014_2006 ori1.png")
        # self.img = cv2.imread("/home/aji/Documents/Data for Homography/10-02-2022/front/021014_2006 ori1.png")
        self.img_main = cv2.imread("/home/aji/Documents/Data for Homography/10-02-2022/front/021013_5233 ori1.png")
        # self.img_main = cv2.imread("/home/aji/Documents/Data for Homography/10-02-2022/front/021013_5233 ori1.png")
        # self.img = cv2.imread('/home/aji/Documents/Data for Homography/Car_11_02/right2crop.png')
        self.point_front = []
        self.front_count = 1
        self.load_parameter()
        self.img = self.update_undistortion(self.img)
        self.img_main = self.update_undistortion(self.img_main)
        # self.img_copy = self.img.copy()
        # self.img = cv2.resize(self.img, (int(self.img.shape[1]/2), int(self.img.shape[0]/2)), cv2.INTER_AREA)
        self.main()

    def main(self):
        canvas = 4800, 2000
        # or object which you want to transform
        # print()
        pts1 = np.float32([[canvas[0]/2-800, canvas[1]-1100], [canvas[0]/2+800, canvas[1]-1100],
                           [canvas[0]/2-800, canvas[1]], [canvas[0]/2+800, canvas[1]]])
        # pts2 = np.float32([[486, 395], [776, 393],
        #                    [491, 597], [806, 586]])

        cv2.imshow('frame', self.img)  # Initial Capture
        cv2.setMouseCallback('frame', self.click_event_front)
        cv2.waitKey(0)
        pts2 = np.float32(self.point_front)
        cv2.destroyAllWindows()

        # Apply Perspective Transform Algorithm
        matrix = cv2.getPerspectiveTransform(pts2, pts1)
        # result = cv2.warpPerspective(self.img, matrix, canvas)
        result = cv2.warpPerspective(self.img_main, matrix, canvas)

        # Wrap the transformed image
        result = cv2.resize(result, (int(result.shape[1]/3), int(result.shape[0]/3)), cv2.INTER_AREA)
        cv2.imshow('frame1', result) # Transformed Capture
        cv2.imshow('frame1', result) # Transformed Capture
        # cv2.imwrite("/home/aji/Documents/Data for Homography/10-02-2022/front/021014_2006 opencv.png", result)
        cv2.waitKey(0)
        cv2.imwrite("/home/aji/Documents/Data for Homography/10-02-2022/front/021013_5233 opencv.png", result)



    def click_event_front(self, event, x, y, flags, params):
        # checking for left mouse clicks
        # self.img_copy = self.img.copy()
        if event == cv2.EVENT_LBUTTONDOWN:
            coordinate = [x, y]
            self.point_front.append(coordinate)
            # displaying the coordinates
            # on the image window
            font = cv2.FONT_HERSHEY_SIMPLEX
            for i, j in self.point_front:
                print("point", i, j)
                cv2.circle(self.img, (x, y), 5, (255, 0, 0), -1)
                cv2.putText(self.img, str(self.front_count) + ". " + str(x) + ',' + str(y), (x, y), font, 1, (255, 0, 0), 2)

                cv2.imshow('frame', self.img)
            self.front_count += 1

    def load_parameter(self):
        calib = cv2.FileStorage("calibration_entaniya.yaml", cv2.FILE_STORAGE_READ)
        self.camera_matrix = calib.getNode("camera_matrix").mat()
        self.dist_coeffs = calib.getNode("dist_coeffs").mat()
        self.resolution = calib.getNode("resolution").mat()
        calib.release()

    def update_undistortion(self, image):
        self.new_matrix = self.camera_matrix.copy()
        self.new_matrix[0, 0] = self.new_matrix[0][0]
        self.new_matrix[1, 1] = self.new_matrix[1][1]
        self.new_matrix[0, 2] = self.new_matrix[0][2]
        self.new_matrix[1, 2] = self.new_matrix[1][2]
        width, hight = self.resolution
        dim = width*4, hight*2
        self.new_matrix[0, 2] = dim[0]/3
        self.new_matrix[1, 2] = 100
        print(width, hight)
        map1, map2 = cv2.fisheye.initUndistortRectifyMap(self.camera_matrix, self.dist_coeffs, np.eye(3), self.new_matrix,
                                                         dim, cv2.CV_16SC2)
        undistorted_img = cv2.remap(image, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        undistorted_img = cv2.resize(undistorted_img, (int(undistorted_img.shape[1]/3), int(undistorted_img.shape[0]/3)), cv2.INTER_AREA)
        return undistorted_img

    def original_undistorted(self, image):
        width, hight = self.resolution
        map1, map2 = cv2.fisheye.initUndistortRectifyMap(self.camera_matrix, self.dist_coeffs, np.eye(3),
                                                         self.camera_matrix, (width, hight), cv2.CV_16SC2)
        undistorted_img = cv2.remap(image, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        return undistorted_img


if __name__ == '__main__':
    perspective_click()