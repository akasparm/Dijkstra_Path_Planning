"""
ENPM661: PLANNING FOR AUTONOMOUS ROBOTS
PROJECT: 2
SUBMITTED BY: AKASHKUMAR PARMAR
UID: 118737430
"""

import numpy as np
import cv2 as cv


def draw_map():

    img = np.zeros((height_y, width_x))

    white = (255,255,255)
    black = (0, 0, 0)
    cv.rectangle(img, (100,0), (150,100), black, -1)
    cv.rectangle(img, (100,0), (150,105), white, 5)
    cv.rectangle(img, (100,150), (150,250), black, -1)
    cv.rectangle(img, (95,145), (155, 245), white, 5)
    cv.rectangle(img, (0,0), (600, 250), white, 5)

    hexagone = np.array([[235, 87.5], [235, 162.5], [300,200], [365,162.5], [365, 87.5], [300,50]], np.int32)
    hexagone = hexagone.reshape((-1,1,2))
    hex_border = np.array([[235, 87.5], [235, 162.5], [300,205], [370,162.5], [370, 87.5], [300,50]], np.int32)
    hex_border = hexagone.reshape((-1,1,2))
    cv.fillPoly(img,[hex_border], black)
    cv.polylines(img,[hex_border], True, white, thickness = 5)

    triangle = np.array([[460, 25], [460, 225], [510,125]])
    triangle = triangle.reshape((-1,1,2))
    tri_border = np.array([[455, 20], [455, 230], [515,125]])
    tri_border = tri_border.reshape((-1,1,2))
    cv.fillPoly(img,[triangle], black)
    cv.polylines(img,[tri_border], True, white, thickness = 5)

    return img

def move_up(current_coord):
    current_coord[1] += 1
    return current_coord

def move_down(current_coord):
    current_coord[1] -= 1
    return current_coord

def move_right(current_coord):
    current_coord[0] += 1
    return current_coord

def move_left(current_coord):
    current_coord[0] -= 1
    return current_coord

def move_upright(current_coord):
    current_coord[0] += 1
    current_coord[1] += 1
    return current_coord

def move_downright(current_coord):
    current_coord[0] += 1
    current_coord[1] -= 1
    return current_coord

def move_upleft(current_coord):
    current_coord[0] -= 1
    current_coord[1] += 1
    return current_coord

def move_downleft(current_coord):
    current_coord[0] -= 1
    current_coord[1] -= 1
    return current_coord


def y_conversion(old_y):
    converted_y = 249 - old_y
    return converted_y

def find_children(current_coord):

    possible_children = []
    possible_children.append(move_up(current_coord.copy()))
    possible_children.append(move_down(current_coord.copy()))
    possible_children.append(move_left(current_coord.copy()))
    possible_children.append(move_right(current_coord.copy()))
    possible_children.append(move_upright(current_coord.copy()))
    possible_children.append(move_downright(current_coord.copy()))
    possible_children.append(move_upleft(current_coord.copy()))
    possible_children.append(move_downleft(current_coord.copy()))

    children = []
    for id, child in enumerate(possible_children):
        if child[1]>=0 and child[1]<height_y and child[0]>=0 and child[0]<width_x:
            if canvas[y_conversion(child[1])][[child[0]]] == 0:
                child_cost = 1.4 if id>3 else 1
                children.append([child, child_cost])
    
    print(children)
    # return children



def main():

    global height_y, width_x, canvas

    
    height_y = 250
    width_x = 600
    canvas = draw_map()
    find_children([10, 10])


    cv.imshow("Dijkstra", canvas)
    cv.waitKey(0)

if __name__=="__main__":
    main()