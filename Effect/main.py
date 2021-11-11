from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import sys
import cv2
import numpy as np
from untitled import Ui_MainWindow
from utils import MoilUtils


class Controller(Ui_MainWindow):
    def __init__(self, MainWindow):
        super(Ui_MainWindow, self).__init__()
        self.parent = MainWindow
        self.setupUi(self.parent)
        self.K = None
        self.D = None
        self.resolution = None
        self.image_name = "right"
        self.image = "/home/aji/Documents/My/Github/Bird_view/data/eleventh/original/" + self.image_name + ".png"
        # self.image = "http://192.168.50.74:8000/stream.mjpg"
        self.image = cv2.imread(self.image)
        self.parameters_path = "../calibrattion.yaml"
        MoilUtils.showImageToLabel(self.lbl_ori, self.image, 500)
        self.camera_matrix = None
        self.resolution = None
        self.dist_coeffs = None
        self.read_parameter()
        self.undistorted()
        self.original_undistortion()
        self.label_4.hide()
        self.doubleSpinBox_fy.hide()
        self.connect()

    def connect(self):
        self.btn_save.clicked.connect(self.save)
        self.btn_reset.clicked.connect(self.reset)
        self.doubleSpinBox_fx.valueChanged.connect(self.undistorted)
        self.doubleSpinBox_fy.valueChanged.connect(self.undistorted)
        self.doubleSpinBox_Cx.valueChanged.connect(self.undistorted)
        self.doubleSpinBox_Cy.valueChanged.connect(self.undistorted)
        self.btn_save.clicked.connect(self.save)

    def undistorted(self):
        matrix = self.calculate()
        width = int(self.image.shape[1])
        height = int(self.image.shape[0])
        dim = (width, height)
        map1, map2 = cv2.fisheye.initUndistortRectifyMap(self.K, self.D, np.eye(3), matrix, (width, height),
                                                         cv2.CV_16SC2)
        undistorted_img = cv2.remap(self.image, map1, map2, interpolation=cv2.INTER_LINEAR,
                                    borderMode=cv2.BORDER_CONSTANT)
        # image = cv2.resize(undistorted_img, dim, interpolation=cv2.INTER_AREA)
        MoilUtils.showImageToLabel(self.lbl_result, undistorted_img, 500)
        self.put_text()

    def original_undistortion(self):
        width = int(self.image.shape[1])
        height = int(self.image.shape[0])
        map1, map2 = cv2.fisheye.initUndistortRectifyMap(self.K, self.D, np.eye(3), self.K, (width, height),
                                                         cv2.CV_16SC2)
        undistorted_img = cv2.remap(self.image, map1, map2, interpolation=cv2.INTER_LINEAR,
                                    borderMode=cv2.BORDER_CONSTANT)
        # image = cv2.resize(undistorted_img, dim, interpolation=cv2.INTER_AREA)
        cv2.imwrite("parameter/" + self.image_name + "_original.png", undistorted_img)
        MoilUtils.showImageToLabel(self.lbl_undis, undistorted_img, 500)

    def calculate(self):
        scale_x = self.doubleSpinBox_fx.value()
        Focal = self.camera_matrix[0, 0]
        distance = Focal - scale_x
        scale_y = self.doubleSpinBox_fy.value() - distance
        # self.doubleSpinBox_fy.setValue(scale_y)
        self.scale_xy = (scale_x, scale_y)

        shift_x = self.doubleSpinBox_Cx.value()
        shift_y = self.doubleSpinBox_Cy.value()
        self.shift_xy = (shift_x, shift_y)

        self.new_matrix = self.camera_matrix.copy()
        self.new_matrix[0, 0] = self.scale_xy[0]
        self.new_matrix[1, 1] = self.scale_xy[1]
        self.new_matrix[0, 2] = self.shift_xy[0]
        self.new_matrix[1, 2] = self.shift_xy[1]

        return self.new_matrix

    def put_text(self):
        self.label_o_fx_3.setText(str(round((self.camera_matrix[0, 0]), 4)))
        self.label_9.setText(str(self.camera_matrix[0, 1]))
        self.label_o_px_3.setText(str(round((self.camera_matrix[0, 2]), 4)))

        self.label_27.setText(str(self.camera_matrix[1, 0]))
        self.label_fy_3.setText(str(round((self.camera_matrix[1, 1]), 4)))
        self.label_py_3.setText(str(round((self.camera_matrix[1, 2]), 4)))

        self.label_32.setText(str(self.camera_matrix[2, 0]))
        self.label_28.setText(str(self.camera_matrix[2, 1]))
        self.label_29.setText(str(self.camera_matrix[2, 2]))
        # ------------------------------------------------------------

        self.label_o_fx_4.setText(str(round((self.new_matrix[0, 0]), 4)))
        self.label_12.setText(str(self.new_matrix[0, 1]))
        self.label_o_px_4.setText(str(round((self.new_matrix[0, 2]), 4 )))

        self.label_34.setText(str(self.new_matrix[1, 0]))
        self.label_fy_4.setText(str(round((self.new_matrix[1, 1]), 4)))
        self.label_py_4.setText(str(round((self.new_matrix[1, 2]), 4)))

        self.label_35.setText(str(self.new_matrix[2, 0]))
        self.label_36.setText(str(self.new_matrix[2, 1]))
        self.label_37.setText(str(self.new_matrix[2, 2]))

    def save(self):
        print("save")
        fs = cv2.FileStorage("parameter/" + self.image_name + ".yaml", cv2.FILE_STORAGE_WRITE)
        fs.write("camera_matrix", self.camera_matrix)
        fs.write("dist_coeffs", self.dist_coeffs)
        fs.write("resolution", self.resolution)
        fs.write("scale_xy", self.scale_xy)
        fs.write("shift_xy", self.shift_xy)
        fs.write("new_camera_matrix", self.new_matrix)
        fs.release()

    def reset(self):
        self.label_o_fx_4.setText(str(round((self.camera_matrix[0, 0]), 4)))
        self.label_12.setText(str(self.camera_matrix[0, 1]))
        self.label_o_px_4.setText(str(round((self.camera_matrix[0, 2]), 4)))

        self.label_34.setText(str(self.camera_matrix[1, 0]))
        self.label_fy_4.setText(str(round((self.camera_matrix[1, 1]), 4)))
        self.label_py_4.setText(str(round((self.camera_matrix[1, 2]), 4)))

        self.label_35.setText(str(self.camera_matrix[2, 0]))
        self.label_36.setText(str(self.camera_matrix[2, 1]))
        self.label_37.setText(str(self.camera_matrix[2, 2]))

        self.doubleSpinBox_fx.setValue(self.camera_matrix[0, 0])
        self.doubleSpinBox_fy.setValue(self.camera_matrix[1, 1])
        self.doubleSpinBox_Cx.setValue(self.camera_matrix[0, 2])
        self.doubleSpinBox_Cy.setValue(self.camera_matrix[1, 2])

        self.undistorted()

    def read_parameter(self):
        fs = cv2.FileStorage(self.parameters_path, cv2.FILE_STORAGE_READ)
        self.camera_matrix = fs.getNode("camera_matrix").mat()
        self.dist_coeffs = fs.getNode("dist_coeffs").mat()
        self.resolution = fs.getNode("resolution").mat().flatten()
        fs.release()
        self.K = np.array(self.camera_matrix)
        self.D = np.array(self.dist_coeffs)


def main():
    apps = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Controller(MainWindow)
    MainWindow.show()
    sys.exit(apps.exec_())


if __name__ == '__main__':
    main()