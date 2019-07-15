import numpy as np
from cv2 import *
import math


# 两张图放到一横行
def twoinone(image1, image2):
    h1, w1, c1 = image1.shape
    h2, w2, c2 = image2.shape
    if c1 != c2:
        print("channels NOT match, cannot merge")
        return
    else:
        if h1 > h2:
            tmp = np.zeros([w2, h1 - h2, c1])
            image3 = np.hstack([image2, tmp])
            image3 = np.vstack([image1, image3])
        elif h1 == h2:
            image3 = np.hstack([image1, image2])
        else:
            tmp = np.zeros([w1, h2 - h1, c2])
            image3 = np.hstack([image1, tmp])
            image3 = np.vstack([image3, image2])

    h, w, c = image3.shape
    for i in range(0, h, 30):
        line(image3, (0, i), (w, i), (255, 255, 255), 1)
    return image3


# 从外旋欧拉角计算旋转矩阵R
def euler2R(roll, pitch, yaw):
    r11 = math.cos(yaw)*math.cos(pitch)
    r12 = -math.sin(yaw)*math.cos(roll)+math.cos(yaw)*math.sin(pitch)*math.sin(roll)
    r13 = math.cos(yaw)*math.sin(pitch)*math.cos(roll)+math.sin(yaw)*math.sin(roll)
    r21 = math.sin(yaw)*math.cos(pitch)
    r22 = -math.sin(yaw)*math.sin(pitch)*math.sin(roll)+math.cos(yaw)*math.cos(roll)
    r23 = math.cos(yaw)*math.sin(roll)+math.sin(yaw)*math.sin(pitch)*math.cos(roll)
    r31 = -math.sin(pitch)
    r32 = -math.cos(pitch)*math.sin(roll)
    r33 = math.cos(pitch)*math.cos(roll)
    return np.float32([[r11, r12, r13], [r21, r22, r23], [r31, r32, r33]])


# 成像平面旋转之后得到的图片
# 旋转矩阵R,相机内参K
def img_after_rotate_camera(Kl, Kr, R, img):
    invKr = np.linalg.inv(Kr)
    invKl = np.linalg.inv(Kl)
    h, w, c = img.shape
    newimg_r = np.zeros([h, w, c], dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            Pp = np.float32([i,j,1])    # 图像素坐标
            Pc = invKr.dot(Pp)           # 图像素坐标-->归一化坐标
            Pco = R.dot(Pc)             # 旋转之后的新点对应原图坐标系下的点的方向（未归一化）
            Pco /= Pco[2]               # 原图中的方向->原图中归一化坐标
            Ppo = Kr.dot(Pco)            # 原图中像素坐标

            uo = int(Ppo[0])
            vo = int(Ppo[1])

            if h-1 >= uo >= 0 and 0 <= vo <= w-1:
                newimg_r[i, j] = img[uo, vo]
    return newimg_r


# 调整焦距，使右图片中物体于左图大小近似
def adjust_focus(img_r, Kl, Kr):
    invKr = np.linalg.inv(Kr)
    invKl = np.linalg.inv(Kl)
    h, w, c = img_r.shape
    newimg_r = np.zeros([h, w, c], dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            Pp = np.float32([i,j,1])    # 图像素坐标
            Pc = invKl.dot(Pp)           # 图像素坐标-->等价左相机归一化坐标
            Ppo = Kr.dot(Pc)            # 原图中像素坐标

            uo = int(Ppo[0])
            vo = int(Ppo[1])

            if h-1 >= uo >= 0 and 0 <= vo <= w-1:
                newimg_r[i, j] = img_r[uo, vo]
    return newimg_r
