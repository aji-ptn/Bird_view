# Experiment of bird view 
Name : Aji
#### How to use this code please refert to [This](How_to_Use_this_code.md)
### 1. Bird view Calibration
- **Outside Area** : the distance between the perspective area and the outer area that will be covered by the surrounding view​​
- **Perspective Area** : the area that gives the top-view image perspective
- **Inside area** : the distance between the car or box and the perspective area 
- **Car or Box** : to put the four cameras

![img.png](doc/second/img.png)

## 2. Calibration Size
### A. Measurement the area Calibration

![img_2.png](doc/second/img_2.png)

### B. Checkerboard size 
- Red Box
```
- Number of checkerboard is 7 x 7 (25 x 25 mm)

- Put on every corner of perspective area

- For Overlapping image (overlap image between two camera)
```
  - Blue Box
```
Number of checkerboard is 9 x 7 (25 X 25 mm)

Put on every front of camera (front, right, rear, left)

For Perspective image (for get perspective from above view)
```
![img_1.png](doc/second/img_1.png)

- **Note** : Each checkerboard must have the same width

## 3. Capture Image
- Image captured by Ethaniya Fisheye camera with FoV 220 degree
- Every camera will capture image at the same time

![img_5.png](doc/second/img_5.png)

## 4. Un-distortion Image
- Un-distortion image using anypoint mode 2
- Alpha = -65, Beta = 0, Zoom factor = 3.5

![img_6.png](doc/second/img_6.png)

## 4. Perspective Transform
- Perspective Image for front image

![img_7.png](doc/second/img_7.png)
- Change every image become above view

![img_8.png](doc/second/img_8.png)

## Final result

- On corner of perspective area still have distortion and fish eye camera had blind spot
![img_4.png](doc/second/img_4.png)


## Documentation and Reference
1. Documentation [link](https://mcut-my.sharepoint.com/:f:/g/personal/m07158031_o365_mcut_edu_tw/Enu7QLAPY15OkFzQuGQrBV4BK8BqS_Oq_2D-eVQ3WeZxSA?e=WiieP1)
2. PPT result [link](https://mcut-my.sharepoint.com/:p:/g/personal/m07158031_o365_mcut_edu_tw/EVBQWUR2BYFDlz0jHPW9KWUB9NKGR-VVz2c0rxeNMCr7Jg?e=0mGOy7)
3. Original Code from Zhao Liang [neozhaoliang GitHub](https://github.com/neozhaoliang/surround-view-system-introduction)