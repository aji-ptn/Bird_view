# Create by aji
# NFY

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import sys
import cv2
import numpy as np
from ui_omni import Ui_MainWindow
from utils import MoilUtils


class Controller(Ui_MainWindow):
    def __init__(self, MainWindow):
        super(Ui_MainWindow, self).__init__()
        self.parent = MainWindow
        self.setupUi(self.parent)
        self.K = None
        self.D = None
        self.resolution = None
        self.image = "/home/aji/Documents/My/Github/Bird_view/data/eleventh/original/front.png"
        self.image = cv2.imread(self.image)
        self.parameters_path = "calibration_omni.yaml"
        MoilUtils.showImageToLabel(self.lbl_ori, self.image, 500)
        self.camera_matrix = None
        self.resolution = None
        self.dist_coeffs = None
        self.read_parameter()
        self.undistorted()
        self.connect()

    def connect(self):
        print("sdasd")
        self.btn_save.clicked.connect(self.save)
        self.btn_start.clicked.connect(self.start)
        self.doubleSpinBox_fx.valueChanged.connect(self.undistorted)
        self.doubleSpinBox_fy.valueChanged.connect(self.undistorted)
        self.spinBox_px.valueChanged.connect(self.undistorted)
        self.spinBox_py.valueChanged.connect(self.undistorted)

    def undistorted(self):
        matrix = self.calculate()
        print(self.camera_matrix)
        print(self.new_matrix)
        width = int(self.image.shape[1])
        height = int(self.image.shape[0])
        dim = (width, height)
        print(dim)

        # map1, map2 = cv2.fisheye.initUndistortRectifyMap(self.K, self.D, np.eye(3), matrix, (width, height),
        #                                                  cv2.CV_16SC2)
        # undistorted_img = cv2.remap(self.image, map1, map2, interpolation=cv2.INTER_LINEAR,
        #                             borderMode=cv2.BORDER_CONSTANT)
        undistorted_img = cv2.omnidir.undistortImage(self.image, matrix, self.D, self.xil, (cv2.omnidir.RECTIFY_PERSPECTIVE))
        image = cv2.resize(undistorted_img, dim, interpolation=cv2.INTER_AREA)
        MoilUtils.showImageToLabel(self.lbl_result, image, 500)
        self.put_text()


    def calculate(self):
        scale_x = self.doubleSpinBox_fx.value()
        scale_y = self.doubleSpinBox_fy.value()
        self.scale_xy = (scale_x, scale_y)

        shift_x = self.spinBox_px.value()
        shift_y = self.spinBox_py.value()
        self.shift_xy = (shift_x, shift_y)

        self.new_matrix = self.camera_matrix.copy()
        self.new_matrix[0, 0] = self.scale_xy[0]
        self.new_matrix[1, 1] = self.scale_xy[1]
        self.new_matrix[0, 2] = self.shift_xy[0]
        self.new_matrix[1, 2] = self.shift_xy[1]

        return self.new_matrix

    def put_text(self):
        print(self.camera_matrix[0, 0])
        self.label_o_fx_3.setText(str(self.camera_matrix[0,0]))
        self.label_o_fx_4.setText(str(self.new_matrix[0, 0]))

    def save(self):
        print("hayy")

    def start(self):
        print("aji disini")
        print(type(self.doubleSpinBox_fx.value()))
        print(self.doubleSpinBox_fx.value())

    def read_parameter(self):
        fs = cv2.FileStorage(self.parameters_path, cv2.FILE_STORAGE_READ)
        self.camera_matrix = fs.getNode("camera_matrix").mat()
        dist_coeffs = fs.getNode("dist_coeffs").mat()
        self.resolution = fs.getNode("resolution").mat().flatten()
        self.xil = fs.getNode("xil").mat().flatten()
        print(self.xil)
        fs.release()
        self.K = np.array(self.camera_matrix)
        self.D = np.array(dist_coeffs)

def main():
    apps = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Controller(MainWindow)
    MainWindow.show()
    sys.exit(apps.exec_())

if __name__ == '__main__':
    main()