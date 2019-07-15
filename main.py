from functions import *
from cv2 import *
from math import *

K_l = np.float32([[615.80781, 0, 350.83844], [0, 625.32534, 235.12715], [0, 0, 1]])
K_r = np.float32([[612.40687, 0, 339.46954], [0, 621.75527, 234.54280], [0, 0, 1]])

theta_x1, theta_y1, theta_z1 = -pi*0.15810/180, pi*1.13860/180, -pi*0.07876/180
R1 = euler2R(theta_x1, theta_y1, theta_z1)

t_x, t_y, t_z = -35.05396, 0.20293, 0.80865
theta_x2, theta_y2, theta_z2 = 0, atan2(t_z, -t_x), atan2(t_y, sqrt(t_x*t_x+t_z*t_z))
R2 = euler2R(theta_x2, theta_y2, theta_z2)

left = imread('E:/epipolarLineRectification/left.png')
right = imread('E:/epipolarLineRectification/right.png')
imshow('l', left)
imshow('r', right)


img = twoinone(left, right)
imshow('ordinary', img)

left = img_after_rotate_camera(K_l, K_r, R2, left)
right = img_after_rotate_camera(K_l, K_r, R2.dot(R1), right)
right = adjust_focus(right, K_l, K_r)

test = twoinone(left, right)
imshow('test', test)





'''
pts0 = np.float32([p1[0:2],p2[0:2],p3[0:2],p4[0:2]])
pts1 = np.float32([pp5[0:2],pp6[0:2],pp7[0:2],pp8[0:2]])
M = getPerspectiveTransform(pts0, pts1)
dst = warpPerspective(left,M,(w,h))
# img = warpPerspective(left, m, (w,h))
imshow('test', dst)
'''
waitKey(0)
