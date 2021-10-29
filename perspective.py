import cv2
import numpy as np
import surround_view.param_settings_2 as param

camera_name = "resize_moil_front"
img = cv2.imread("images/"+ camera_name +".png")
matrix = "yaml/"+ camera_name +".yaml"
# print(img.shape)
#
# src = [[231, 264], [537., 231],
#        [54., 387.], [862., 326.]]
#
# dst = [[420, 300], [700, 300],
#        [420, 460], [700, 460]]
#
# print(src)
projec_shapes = param.project_shapes[camera_name]

# src = np.float32(src)
# dst = np.float32(dst)
#
# perspective = cv2.getPerspectiveTransform(src, dst)
# print(perspective)
fs = cv2.FileStorage(matrix, cv2.FILE_STORAGE_READ)
perspective = fs.getNode("project_matrix").mat()
img_2 = cv2.warpPerspective(img, perspective, projec_shapes)
print(img.shape)
print(img_2.shape)


cv2.imshow("img", img)
cv2.imshow("img2", img_2)
cv2.waitKey()

# import necessary libraries
#
# import cv2
# import numpy as np
#
# # Turn on Laptop's webcam
# cap = cv2.VideoCapture(0)
#
# while True:
#
#        ret, frame = cap.read()
#        print(frame.shape)
#
#
#        # Locate points of the documents or object which you want to transform
#        pts1 = np.float32([[0, 0], [200, 0], [0, 300], [200, 300]])
#        pts2 = np.float32([[0, 0], [400, 0], [0, 640], [400, 640]])
#
#        # Apply Perspective Transform Algorithm
#        matrix = cv2.getPerspectiveTransform(pts1, pts2)
#        result = cv2.warpPerspective(frame, matrix, (480, 640))
#        # Wrap the transformed image
#
#        cv2.imshow('frame', frame)  # Inital Capture
#        cv2.imshow('frame1', result)  # Transformed Capture
#
#        if cv2.waitKey(24) == 27:
#               break
#
# cap.release()
# cv2.destroyAllWindows()