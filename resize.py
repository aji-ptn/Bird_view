import cv2
import glob
i = 1

images = glob.glob('/home/aji/Documents/My/Github/surround-view-edit/images/moil_right.png')
for fname in images:

    img = cv2.imread(fname)

    print('Original Dimensions : ', img.shape)

    width = int(img.shape[1] / 3)
    height = int(img.shape[0] / 3)
    dim = (width, height)

    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    print('Resized Dimensions : ', resized.shape)
    # print(images)

    cv2.imshow("Resized image", resized)
    cv2.imwrite("/home/aji/Documents/My/Github/surround-view-edit/images/resize_moil_right.png", resized)
    print(i)
    i += 1
    cv2.waitKey(0)
    cv2.destroyAllWindows()