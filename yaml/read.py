import cv2


fs = cv2.FileStorage("back.yaml", cv2.FILE_STORAGE_READ)
camera_matrix = fs.getNode("camera_matrix").mat()
dist_coeffs = fs.getNode("dist_coeffs").mat()
resolution = fs.getNode("resolution").mat().flatten()


#load_camera_params()
print(camera_matrix)
