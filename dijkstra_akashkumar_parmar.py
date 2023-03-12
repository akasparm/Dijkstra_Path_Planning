"""
ENPM661: PLANNING FOR AUTONOMOUS ROBOTS
PROJECT: 2
SUBMITTED BY: AKASHKUMAR PARMAR
UID: 118737430
"""

# Importing required libraries
import numpy as np
from queue import PriorityQueue
import cv2 as cv
import time
import math as m

# Function to draw a map
def draw_map():

    img = np.zeros((height_y, width_x))
    # img = np.zeros((height_y, width_x), dtype=np.uint8)

    white = (255,255,255)
    black = (0, 0, 0)

    # Object Creation
    cv.rectangle(img, (100,0), (150,100), black, -1) 
    cv.rectangle(img, (95,0), (155,105), white, 5)
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

# Function to draw a map
def draw_visual_img():

    img = np.zeros((height_y, width_x, 3), dtype=np.uint8)

    white = (255,255,255)
    black = (0, 0, 0)

    # Object Creation
    cv.rectangle(img, (100,0), (150,100), black, -1) 
    cv.rectangle(img, (95,0), (155,105), white, 5)
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
# y conversion function
# As image origin and given visualization origin are different
# The function compensates for the shift and orientation of the origins
def y_conversion(old_y):
    converted_y = 249 - old_y
    return converted_y

# Checks for the validity of the user input
# Makes sure the coordinates do no intersect with walls or objects
def coord_validation(coord1, coord2):
    coord1[1] = y_conversion(coord1[1])
    coord2[1] = y_conversion(coord2[1])
             
    p = coord1[0]
    q = coord1[1]
    a = coord2[0]
    b = coord2[1]

    # Scrap image is generated for checking the validity of the coordinates
    scrap_img = np.zeros((height_y, width_x))

    # Make the objects white in binary scrap_img
    for i in range(height_y):
        for j in range(width_x):
            
            if(j>=95 and j<=155 and i>=0 and i<=105):
                scrap_img[i][j]=1

            if(j>=95 and j<=155 and i>=145 and i<250):
                scrap_img[i][j]=1
                
            if(j>=300-5-75*np.cos(np.deg2rad(30)) and j<=300+5+75*np.cos(np.deg2rad(30))):
                if(37.5*j + 64.95*i > 14498) and (-37.5*j + 64.95*i < 1742):
                    if(37.5*j + 64.95*i < 24240) and (37.5*j - 64.95*i < 8002.5):
                        scrap_img[i][j]=1

            if(j>=460):
                if(-100*j + 50*i > -44750) and (2*j + i < 1145):
                     scrap_img[i][j] = 1
                
            if(j>=0 and j<5) or (i>=0 and i<5) or (i>244 and i<250) or (j>594 and j<600):
                scrap_img[i][j]=1

    # check if the input coordinates have white pixel value or not
    if scrap_img[q][p]!=0 or scrap_img[b][a]!=0:
        return False

    return True

"""
node class generation.
Accomodation for the position, cost and parent attributes of the each object node.
"""
class Node:
    def __init__(self, position, cost, parent):
        self.position = position
        self.x = position[0]
        self.y = position[1]
        self.cost = cost
        self.parent = parent

# Action set move up
def move_up(current_coord):
    current_coord[1] += 1
    return current_coord

# Action set move down
def move_down(current_coord):
    current_coord[1] -= 1
    return current_coord

# Action set move right
def move_right(current_coord):
    current_coord[0] += 1
    return current_coord

# Action set move left
def move_left(current_coord):
    current_coord[0] -= 1
    return current_coord

# Action set move up-right
def move_upright(current_coord):
    current_coord[0] += 1
    current_coord[1] += 1
    return current_coord

# Action set move down-right
def move_downright(current_coord):
    current_coord[0] += 1
    current_coord[1] -= 1
    return current_coord

# Action set move up-left
def move_upleft(current_coord):
    current_coord[0] -= 1
    current_coord[1] += 1
    return current_coord

# Action set move down-left
def move_downleft(current_coord):
    current_coord[0] -= 1
    current_coord[1] -= 1
    return current_coord

# Children geneation function
# Finds out the possible children
def find_children(node):
    i = node.x
    j = node.y

    current_coord = [i, j]
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

    # Iterate through possible children
    for id, child in enumerate(possible_children):
        if child[1]>=0 and child[1]<height_y and child[0]>=0 and child[0]<width_x:
            if canvas[y_conversion(child[1])][[child[0]]] == 0:
                child_cost = 1.4 if id>3 else 1 # Add cost to each child node
                children.append([child, child_cost])
    
    return children


# Main function
def main():

    # Global variables
    global q, height_y, width_x, canvas
    q = PriorityQueue()
    visited_list = set([])
    node_objects = {}
    height_y = 250
    width_x = 600
    initial_coord = [300, 125] # Initializations
    dest_coord = [300, 125] # initialization
    

    # Check the validity of coordinates
    is_valid = False
    while not is_valid:

        print("Invalid inputs. Initial or final coordinates are intersecting with obstacles.\nTry Again:")
        initial_coord[0] = int(input("Enter initial x coordinate: "))
        initial_coord[1] = int(input("Enter initial y coordinate: "))
        dest_coord[0] = int(input("Enter destination x coordinates: "))
        dest_coord[1] = int(input("Enter destination y coordinates: "))
        is_valid = coord_validation(initial_coord.copy(), dest_coord.copy())

    
    start_time = time.time() # start time for finding the path

    canvas = draw_map()

    cost_dict = {} # cost dictionary
    for i in range(height_y):
        for j in range(width_x):
            cost_dict[str([i, j])] = m.inf
    
    cost_dict[str(initial_coord)] = 0
    visited_list.add(str(initial_coord))
    node = Node(initial_coord, 0, None)
    node_objects[str(node.position)] = node
    q.put([node.cost, node.position])

    video_array = []

    # Generating the layers for color image
    # img_show = np.dstack([canvas.copy()*255, canvas.copy()*255, canvas.copy()*255])
    img_show = draw_visual_img()

    p = 0 # switch for showing the output at every 500th loop

    while not q.empty():

        # Get a node by greedy algorithm
        temp_node = q.get()
        node = node_objects[str(temp_node[1])]
        if temp_node[1][0] == dest_coord[0] and temp_node[1][1] == dest_coord[1]:
            node_objects[str(dest_coord)] = Node(dest_coord, temp_node[0], node)
            print("Solution Found!")
            break
        
        # Find children and iterate through them
        for child_node, cost in find_children(node):

            # if the node is visited
            if str(child_node) in visited_list:
                temp_cost = cost + cost_dict[str(node.position)]
                if temp_cost<cost_dict[str(child_node)]:
                    cost_dict[str(child_node)] = temp_cost
                    node_objects[str(child_node)].parent = node
                
            # if the node is not visited
            else:
                visited_list.add(str(child_node))
                img_show[y_conversion(child_node[1]), child_node[0], :] = np.array([0, 0, 255])
                if(p%500==0):
                    video_array.append(img_show.copy())
                    cv.imshow("Dijkstra", img_show)
                    cv.waitKey(1)
                abs_cost = cost + cost_dict[str(node.position)]
                cost_dict[str(child_node)] = abs_cost
                new_node = Node(child_node, abs_cost, node_objects[str(node.position)])
                q.put([abs_cost, new_node.position])
                node_objects[str(new_node.position)] = new_node

            p+=1

    # Backtracking algorithm
    dest_node = node_objects[str(dest_coord)]
    parent_node = dest_node.parent
    tempt_list = []
    while parent_node:
        tempt_list.append([y_conversion(parent_node.position[1]), parent_node.position[0]])
        parent_node = parent_node.parent

    # saving the backtrack and visualizing it
    tempt_list.reverse()
    for i in tempt_list:
        video_array.append(img_show.copy())
        cv.circle(img_show, (i[1], i[0]), 1, (0, 0, 0), -1)
        cv.imshow("Dijkstra", img_show)
        cv.waitKey(1)

    end_time = time.time()

    print("Path found in ", end_time - start_time, " seconds.")

    video = cv.VideoWriter('dijkstra_vid.mp4', cv.VideoWriter_fourcc(*'MP4V'), 30, (600, 250))

    for element in range(len(video_array)):
        frame = video_array[element]
        video.write(frame)
    video.release()


    cv.waitKey(0)

if __name__=="__main__":
    main()