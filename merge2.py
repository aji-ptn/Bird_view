import cv2
import numpy as np
import surround_view.param_settings_2 as settings
names = settings.camera_names
dimention_h = settings.total_h
dimention_w = settings.total_w
car_image = settings.car_image


def adjust_luminance(gray, factor):
    """
    Adjust the luminance of a grayscale image by a factor.
    """
    return np.minimum((gray * factor), 255).astype(np.uint8)


def white_balance_process(image):
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
    B = adjust_luminance(B, c1)
    G = adjust_luminance(G, c2)
    R = adjust_luminance(R, c3)
    return cv2.merge((B, G, R))

front = cv2.imread("/home/aji/Documents/My/Github/Bird_view_2.0/data/thirteen (copy)/cutting/front.png")
left = cv2.imread("/home/aji/Documents/My/Github/Bird_view_2.0/data/thirteen (copy)/cutting/left.png")
right = cv2.imread("/home/aji/Documents/My/Github/Bird_view_2.0/data/thirteen (copy)/cutting/right.png")
rear = cv2.imread("/home/aji/Documents/My/Github/Bird_view_2.0/data/thirteen (copy)/cutting/rear.png")

final_image = np.zeros([dimention_h, dimention_w, 3], dtype=np.uint8)
# final_image = np.zeros([4000, 4000, 3], dtype=np.uint8)
print("final image = ", final_image)
print("front", front.shape)
print("left", left.shape)
print("right", right.shape)
print("rear", rear.shape)
print(final_image.shape)

right_limit = final_image.shape[1]-right.shape[1]
rear_limit = final_image.shape[0]-rear.shape[0]
print(right_limit)

final_image[0:0 + left.shape[0], 0:0 + left.shape[1]] = left  # 0 is height
final_image[0:0 + right.shape[0], right_limit:right_limit + right.shape[1]] = right  # 0 is height
final_image[0:0 + front.shape[0], 0:0 + front.shape[1]] = front  # 0 is height 1 width
final_image[rear_limit:rear_limit + rear.shape[0], 0:0 + rear.shape[1]] = rear  # 0 is height
final_image[front.shape[0]:front.shape[0] + car_image.shape[0], right.shape[1]:right.shape[1] + car_image.shape[1]] = car_image  # 0 is height


width_final = int(final_image.shape[1] / 3)
height_final = int(final_image.shape[0] / 3)
dim2 = (width_final, height_final)

# final_image = cv2.resize(final_image, dim2, interpolation=cv2.INTER_AREA)
# print(resize_image.shape)
cv2.imshow("final_image", final_image)
cv2.imwrite("/home/aji/Documents/My/Github/Bird_view_2.0/data/thirteen (copy)/final.png", final_image)
final_image2 = white_balance_process(final_image)
cv2.imshow("final_image 2", final_image2)
cv2.waitKey()


