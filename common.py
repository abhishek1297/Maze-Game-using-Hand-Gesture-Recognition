import math
import numpy as np
import cv2 as cv
import arcade as arc

skin_l1 = np.array([0, 20, 40])
skin_u1 = np.array([40, 255, 255])

skin_l2 = np.array([0, 20, 70])
skin_u2 = np.array([20, 255, 255])

skin_l3 = np.array([2, 0, 0])
skin_u3 = np.array([20, 255, 255])

skin_l4 = np.array([0, 48, 80])
skin_u4 = np.array([20, 255, 255])

skin_l5 = np.array([0, 10, 60])
skin_u5 = np.array([20, 150, 255])

skin_l6 = np.array([19, 59, 255])
skin_u6 = np.array([9, 155, 186])

skin_l7 = np.array([6, 10, 100])
skin_u7 = np.array([26, 255, 255])

roi_1 = (100, 100)
roi_2 = (300, 300)
frame, binary = None, None
BOUND = [30, 20, 10]
STEP = [0.8, 0.3, 0.3]
WALL_SCALE = [0.85, 0.5, 0.3]
PLAYER_SCALE = [0.14, 0.05, 0.04]
centroid, normal, farthest, x, y, w, h = [0] * 7
HAND_DETECTED = False
CAMERA = None

WIDTH = 500
HEIGHT = 500
	