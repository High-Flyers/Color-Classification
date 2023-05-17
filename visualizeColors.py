import argparse
import ast
import math
import colorsys
import numpy as np
import cv2

ap = argparse.ArgumentParser()

ap.add_argument(
    "--input_file",
    type=str,
    default='inputColors.txt'
)

ap.add_argument(
    "--method",
    type=str,
    default="rgb"
)

ap.add_argument(
    "--max_dist",
    type=float,
    default=0.2
)

args = vars(ap.parse_args())

if args['method'] not in ['rgb', 'hsv']:
    print("Unidentified method!!")
    exit()

template_colors = {}

with open(args['input_file']) as f:
    for line in f.readlines():
        splitted = line.split(' ')
        if len(splitted) != 3:
            print("Wrong input file")
            exit()
        template_colors[splitted[0][:-1]] = ast.literal_eval(splitted[-1].split('=')[1])

print(template_colors)

max_dist = min(max(args['max_dist'], 0), 1)

W, H = 2480, 3508
image = np.zeros((H, W, 3), np.uint8)
points = [[0, 0, -1], [0, 0, 1], [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0]]
col_size = W // 6
row_size = H // len(template_colors)

for i, color in enumerate(template_colors):
    for j, dir in enumerate(points):
        if args['method'] == 'rgb':
            abs_max_dist = max_dist * 255
            r = min(max(template_colors[color][0] + dir[0] * abs_max_dist, 0), 255)
            g = min(max(template_colors[color][1] + dir[1] * abs_max_dist, 0), 255)
            b = min(max(template_colors[color][2] + dir[2] * abs_max_dist, 0), 255)
        elif args['method'] == 'hsv':
            abs_max_dist = max_dist * 1
            r, g, b = colorsys.hsv_to_rgb(
                min(max(template_colors[color][0] + dir[0] * abs_max_dist, 0), 1),
                min(max(template_colors[color][1] + dir[1] * abs_max_dist, 0), 1),
                min(max(template_colors[color][2] + dir[2] * abs_max_dist, 0), 1)
            )
            r, g, b = int(r * 255), int(g * 255), int(b * 255)

        cv2.rectangle(image, (j * col_size, i * row_size), ((j + 1) * col_size, (i + 1) * row_size), (b, g, r),
                      cv2.FILLED)

cv2.imwrite("visualizedColors.png", image)