import numpy as np
import cv2
from . import param_settings_2 as settings
from .param_settings_2 import xl, xr, yt, yb
# from . import utils


class BirdView():
    def __init__(self):
        self.frame = None
        self.image = np.zeros((settings.total_h, settings.total_w, 3), np.uint8)
        self.car_image = settings.car_image

    def update_frames(self, images):
        self.frames = images

    def get_weights_and_masks(self, images):
        front, back, left, right = images
        print("get_weights_and_masks - front left")
        G0, M0 = self.get_weight_mask_matrix(FI(front), LI(left))
        front_left, left_front = FI(front), LI(left)
        cv2.imshow("front_left", front_left)
        cv2.imshow("left_front", left_front)
        cv2.imshow("GO", G0)
        cv2.imshow("M0(mask)", M0)
        cv2.waitKey()
        print("original = ", front.shape, left.shape)
        # print(G0, M0)
        print("get_weights_and_masks - front right")
        G1, M1 = self.get_weight_mask_matrix(FII(front), RII(right))
        print("get_weights_and_masks - back left")
        G2, M2 = self.get_weight_mask_matrix(BIII(back), LIII(left))
        print("get_weights_and_masks - back right")
        G3, M3 = self.get_weight_mask_matrix(BIV(back), RIV(right))
        self.weights = [np.stack((G, G, G), axis=2) for G in (G0, G1, G2, G3)]
        self.masks = [(M / 255.0).astype(np.int) for M in (M0, M1, M2, M3)]
        return np.stack((G0, G1, G2, G3), axis=2), np.stack((M0, M1, M2, M3), axis=2)

    def get_weight_mask_matrix(self, imA, imB, dist_threshold=1):
        """
        Get the weight matrix G that combines two images imA, imB smoothly.

        imA = image overlapping A
        imB = image Overlapping B
        """

        overlapMask = self.get_overlap_region_mask(imA, imB)
        overlapMaskInv = cv2.bitwise_not(overlapMask)
        indices = np.where(overlapMask == 255)

        imA_diff = cv2.bitwise_and(imA, imA, mask=overlapMaskInv)
        imB_diff = cv2.bitwise_and(imB, imB, mask=overlapMaskInv)

        G = self.get_mask(imA).astype(np.float32) / 255.0

        polyA = self.get_outmost_polygon_boundary(imA_diff)
        polyB = self.get_outmost_polygon_boundary(imB_diff)

        for y, x in zip(*indices):
            distToB = cv2.pointPolygonTest(polyB, (x, y), True)
            if distToB < dist_threshold:
                distToA = cv2.pointPolygonTest(polyA, (x, y), True)
                distToB *= distToB
                distToA *= distToA
                G[y, x] = distToB / (distToA + distToB)
        cv2.imshow("overlapMaskInv", overlapMaskInv)

        return G, overlapMask

    def get_overlap_region_mask(self, imA, imB):
        """
        Given two images of the save size, get their overlapping region and
        convert this region to a mask array.
        """
        cv2.imshow("imA", imA)
        cv2.imshow("imB", imB)
        overlap = cv2.bitwise_and(imA, imB)
        mask = self.get_mask(overlap)
        mask = cv2.dilate(mask, np.ones((2, 2), np.uint8), iterations=2)
        cv2.imshow("overlap", overlap)
        return mask

    def get_mask(self, img):
        """
        Convert an image to a mask array.
        """
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
        return mask

    def get_outmost_polygon_boundary(self, img):
        """
        Given a mask image with the mask describes the overlapping region of
        two images, get the outmost contour of this region.
        """
        mask = self.get_mask(img)
        mask = cv2.dilate(mask, np.ones((2, 2), np.uint8), iterations=2)
        cnts, hierarchy = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2:]

        # get the contour with largest aera
        C = sorted(cnts, key=lambda x: cv2.contourArea(x), reverse=True)[0]

        # polygon approximation
        polygon = cv2.approxPolyDP(C, 0.009 * cv2.arcLength(C, True), True)

        return polygon

    def make_luminance_balance(self):

        def tune(x):
            if x >= 1:
                return x * np.exp((1 - x) * 0.5)
            else:
                return x * np.exp((1 - x) * 0.8)

        front, back, left, right = self.frames
        m1, m2, m3, m4 = self.masks
        Fb, Fg, Fr = cv2.split(front)
        Bb, Bg, Br = cv2.split(back)
        Lb, Lg, Lr = cv2.split(left)
        Rb, Rg, Rr = cv2.split(right)

        a1 = self.mean_luminance_ratio(RII(Rb), FII(Fb), m2)
        a2 = self.mean_luminance_ratio(RII(Rg), FII(Fg), m2)
        a3 = self.mean_luminance_ratio(RII(Rr), FII(Fr), m2)

        b1 = self.mean_luminance_ratio(BIV(Bb), RIV(Rb), m4)
        b2 = self.mean_luminance_ratio(BIV(Bg), RIV(Rg), m4)
        b3 = self.mean_luminance_ratio(BIV(Br), RIV(Rr), m4)

        c1 = self.mean_luminance_ratio(LIII(Lb), BIII(Bb), m3)
        c2 = self.mean_luminance_ratio(LIII(Lg), BIII(Bg), m3)
        c3 = self.mean_luminance_ratio(LIII(Lr), BIII(Br), m3)

        d1 = self.mean_luminance_ratio(FI(Fb), LI(Lb), m1)
        d2 = self.mean_luminance_ratio(FI(Fg), LI(Lg), m1)
        d3 = self.mean_luminance_ratio(FI(Fr), LI(Lr), m1)

        t1 = (a1 * b1 * c1 * d1)**0.25
        t2 = (a2 * b2 * c2 * d2)**0.25
        t3 = (a3 * b3 * c3 * d3)**0.25

        x1 = t1 / (d1 / a1)**0.5
        x2 = t2 / (d2 / a2)**0.5
        x3 = t3 / (d3 / a3)**0.5

        x1 = tune(x1)
        x2 = tune(x2)
        x3 = tune(x3)

        Fb = self.adjust_luminance(Fb, x1)
        Fg = self.adjust_luminance(Fg, x2)
        Fr = self.adjust_luminance(Fr, x3)

        y1 = t1 / (b1 / c1)**0.5
        y2 = t2 / (b2 / c2)**0.5
        y3 = t3 / (b3 / c3)**0.5

        y1 = tune(y1)
        y2 = tune(y2)
        y3 = tune(y3)

        Bb = self.adjust_luminance(Bb, y1)
        Bg = self.adjust_luminance(Bg, y2)
        Br = self.adjust_luminance(Br, y3)

        z1 = t1 / (c1 / d1)**0.5
        z2 = t2 / (c2 / d2)**0.5
        z3 = t3 / (c3 / d3)**0.5

        z1 = tune(z1)
        z2 = tune(z2)
        z3 = tune(z3)

        Lb = self.adjust_luminance(Lb, z1)
        Lg = self.adjust_luminance(Lg, z2)
        Lr = self.adjust_luminance(Lr, z3)

        w1 = t1 / (a1 / b1)**0.5
        w2 = t2 / (a2 / b2)**0.5
        w3 = t3 / (a3 / b3)**0.5

        w1 = tune(w1)
        w2 = tune(w2)
        w3 = tune(w3)

        Rb = self.adjust_luminance(Rb, w1)
        Rg = self.adjust_luminance(Rg, w2)
        Rr = self.adjust_luminance(Rr, w3)

        self.frames = [cv2.merge((Fb, Fg, Fr)),
                       cv2.merge((Bb, Bg, Br)),
                       cv2.merge((Lb, Lg, Lr)),
                       cv2.merge((Rb, Rg, Rr))]
        return self

    def adjust_luminance(self, gray, factor):
        """
        Adjust the luminance of a grayscale image by a factor.
        """
        return np.minimum((gray * factor), 255).astype(np.uint8)

    def mean_luminance_ratio(self, grayA, grayB, mask):
        return self.get_mean_statistisc(grayA, mask) / self.get_mean_statistisc(grayB, mask)

    def get_mean_statistisc(self, gray, mask):
        """
        Get the total values of a gray image in a region defined by a mask matrix.
        The mask matrix must have values either 0 or 1.
        """
        return np.sum(gray * mask)

    def stitch_all_parts(self):
        front, back, left, right = self.frames
        np.copyto(self.F, FM(front))
        np.copyto(self.B, BM(back))
        np.copyto(self.L, LM(left))
        np.copyto(self.R, RM(right))
        np.copyto(self.FL, self.merge(FI(front), LI(left), 0))
        np.copyto(self.FR, self.merge(FII(front), RII(right), 1))
        np.copyto(self.BL, self.merge(BIII(back), LIII(left), 2))
        np.copyto(self.BR, self.merge(BIV(back), RIV(right), 3))

    def make_white_balance(self):
        self.image = self.white_balance_process(self.image)

    def white_balance_process(self, image):
        """
        Adjust white balance of an image base on the means of its channels.
        """
        B, G, R = cv2.split(image)
        m1 = np.mean(B)
        m2 = np.mean(G)
        m3 = np.mean(R)
        K = (m1 + m2 + m3) / 3
        c1 = K / m1
        c2 = K / m2
        c3 = K / m3
        B = self.adjust_luminance(B, c1)
        G = self.adjust_luminance(G, c2)
        R = self.adjust_luminance(R, c3)
        return cv2.merge((B, G, R))

    def copy_car_image(self):
        np.copyto(self.C, self.car_image)

    def merge(self, imA, imB, k):
        G = self.weights[k]
        return (imA * G + imB * (1 - G)).astype(np.uint8)

    @property
    def FL(self):  # front left
        return self.image[:yt, :xl]

    @property
    def F(self):  # front
        return self.image[:yt, xl:xr]

    @property
    def FR(self):  # front right
        return self.image[:yt, xr:]

    @property
    def BL(self):  # bellow left
        return self.image[yb:, :xl]

    @property
    def B(self):  # bellow
        return self.image[yb:, xl:xr]

    @property
    def BR(self):  # bellow right
        return self.image[yb:, xr:]

    @property
    def L(self):  # left
        return self.image[yt:yb, :xl]

    @property
    def R(self):  # right
        return self.image[yt:yb, xr:]

    @property
    def C(self):  # center
        return self.image[yt:yb, xl:xr]


def FI(front_image):
    value = front_image[:, :xl]
    # print(value)
    # cv2.imshow("hay", value)
    # cv2.waitKey()
    return value


def FII(front_image):
    return front_image[:, xr:]


def FM(front_image):
    return front_image[:, xl:xr]


def BIII(back_image):
    return back_image[:, :xl]


def BIV(back_image):
    return back_image[:, xr:]


def BM(back_image):
    return back_image[:, xl:xr]


def LI(left_image):
    value = left_image[:yt, :]
    return value


def LIII(left_image):
    return left_image[yb:, :]


def LM(left_image):
    return left_image[yt:yb, :]


def RII(right_image):
    return right_image[:yt, :]


def RIV(right_image):
    return right_image[yb:, :]


def RM(right_image):
    return right_image[yt:yb, :]



