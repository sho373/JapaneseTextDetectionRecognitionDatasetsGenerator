import re
import numpy as np 
from numpy import savetxt
import random
import cv2
import numpy as np
import matplotlib as plt
from PIL import ImageFont, ImageDraw, Image
import os
from rotate_text import draw_rotated_text
import math
import config 
from mpmath import *

img_w = config.IMAGE_WIDTH
img_h = config.IMAGE_HIEGHT

def find_point(x, y) :
    x1 = 0
    y1 = 0
    x2 = img_w
    y2 = img_h

    if (x > x1 and x < x2 and 
        y > y1 and y < y2) : 
        return True
    else : 
        return False

def is_cor_inside_image(tl, tr, bl, br):
    if find_point(tl[0], tl[1]) and find_point(tr[0], tr[1]):
        if find_point(bl[0], bl[1]) and find_point(br[0],br[1]): 
            return True
    return False

def calRotatedPoints(_x1,_y1,cx,cy,angle):
    """
    Function calculate the cordinate (x1,y1) for rotaed points of box
    """
    # x′=xcosθ-ysinθ
    # y′=xsinθ+ycosθ
    
    tempX = fsub(_x1,cx)
    tempY = fsub(_y1,cy)
    rotatedX = fsub((fmul(tempX,cos(angle))), (fmul(tempY,sin(angle))))
    rotatedY = fadd((fmul(tempY,cos(angle))), (fmul(tempX,sin(angle))))
    x1 = fadd(rotatedX,cx)
    y1 = fadd(rotatedY,cy)
    
    return int(x1),int(y1)


def gen_random_par(words_list):
    words_index = random.randint(0,len(words_list) -1)
    font_scale = random.randint(config.FONT_SCALE_FROM, config.FONT_SCALE_TO)
    horizontal = random.randint(0,config.HORIZONTAL)
    angle = 0 
    words = words_list[words_index]
    words_len = len(words) - 1
    #For English words
    # if(len(words) % 2 == 0):
    #     words_len = (len(words) - 2)/2
    # else:
    #     words_len = (len(words) - 1)/2 - 0.5
    
    if words_len < 4:
        x_cor = random.randint(10,int(img_w/2))
    else :
        x_cor = random.randint(10,int(img_w/4))


    y_cor = random.randint(font_scale, int(img_h - font_scale))

    font = ImageFont.truetype(config.FONT_NAME, font_scale)
    
    tl = (int(x_cor), int(y_cor))
    tl_text_cor = tl
    tr = (int(x_cor + words_len*font_scale + font_scale), int(y_cor))
    br = (int(x_cor + words_len*font_scale + font_scale),int(y_cor + font_scale),)
    bl = (int(x_cor), int(y_cor + font_scale))

    if not horizontal:
        angle = random.randint(config.ANGLE_FROM, config.ANGLE_TO)               
        rotated_tr = calRotatedPoints(tr[0], tr[1], tl[0], tl[1], radians(-angle))
        rotated_br = calRotatedPoints(br[0], br[1], tl[0], tl[1], radians(-angle))
        rotated_bl = calRotatedPoints(bl[0], bl[1], tl[0], tl[1], radians(-angle))
        
        if(angle >= 0):
            tl = (tl[0], rotated_tr[1])
            br = (rotated_br[0], rotated_bl[1])
            tr = (rotated_br[0], rotated_tr[1])
            bl = (tl[0], rotated_bl[1])
        else:
            tl = (rotated_bl[0], tl[1])
            br = (rotated_tr[0], rotated_br[1])
            tr = (rotated_tr[0], tl[1])
            bl = (rotated_bl[0], rotated_br[1])

    return words, font, horizontal, font_scale, tl, tr, bl, br, angle, tl_text_cor

def boxes_intersection(bb1, bb2):
    """
    check two bounding boxes intersect.

    """
    assert bb1[0][0] < bb1[1][0]
    assert bb1[0][1] < bb1[1][1]
    assert bb2[0][0] < bb2[1][0]
    assert bb2[0][1] < bb2[1][1]

    # determine the coordinates of the intersection rectangle
    x_left = max(bb1[0][0], bb2[0][0])
    y_top = max(bb1[0][1], bb2[0][1])
    x_right = min(bb1[1][0], bb2[1][0])
    y_bottom = min(bb1[1][1], bb2[1][1])

    if x_right < x_left or y_bottom < y_top:
        return False
    return True


def main():
    results_dir = config.RESULT_DIR
    img_dir = config.TARGET_DIR
   
    results_img_dir = os.path.join(results_dir, img_dir)

    if not os.path.exists(results_dir):
        os.mkdir(results_dir)
    if not os.path.exists(results_img_dir):
        os.mkdir(results_img_dir)

    words_list = np.zeros(shape=(1, 1),dtype=object)

    with open('katakana_words.txt', 'r', encoding='utf-8') as f:
        for line in f:
            words_list = np.append(words_list, line.replace("\n",""))
    words_list = np.delete(words_list,0)
    
    text_color_list = [(0, 0, 255), (0,0,0), (15, 8, 44), (0,0,0), (255,250,250), (255,0,0), (255,250,250), (255,127,0)] 
    #blue, black, dark blue, black, red, white,orange
    count = 0

    for filename in os.listdir(img_dir):
        if filename.endswith(".jpg"):
            
            image = cv2.imread(os.path.join(img_dir,filename))
            count+=1
            words_num = random.randint(1,config.MAXIMUM_NUM_WORDS)
           
            cor_list = []

            if not image is None:
                image = cv2.resize(image, (img_w,img_h))
                
                for i in range(words_num):
                    is_cor_inside = False
                    is_box_intersect = False

                    if i == 0:
                        while not is_cor_inside:
                            words, font, horizontal, font_scale, tl, tr, bl, br, angle, tl_text_cor = gen_random_par(words_list)
                            if is_cor_inside_image(tl,tr,bl,br):
                                is_cor_inside = True
                        cor_list.append([tl, br])   
                    elif i == 1:
                        while not is_box_intersect:
                            while not is_cor_inside:
                                words, font, horizontal, font_scale, tl, tr, bl, br, angle, tl_text_cor = gen_random_par(words_list)
                                if is_cor_inside_image(tl,tr,bl,br):
                                    is_cor_inside = True
                            cor_list.append([tl, br])
                            check = boxes_intersection(cor_list[i-1], cor_list[i])
                            if check == False:
                                is_box_intersect = True
                            else:
                                cor_list.pop(-1)
                                is_cor_inside = False
                    elif i == 2:
                        while not is_box_intersect:
                            while not is_cor_inside:
                                words, font, horizontal, font_scale, tl, tr, bl, br, angle, tl_text_cor = gen_random_par(words_list)
                                if is_cor_inside_image(tl,tr,bl,br):
                                    is_cor_inside = True
                            cor_list.append([tl, br])        
                            check_2 = boxes_intersection(cor_list[0], cor_list[i])
                            check_3 = boxes_intersection(cor_list[1], cor_list[i])
                            if check_2 == False and check_3 == False:
                                is_box_intersect = True      
                            else:
                                cor_list.pop(-1)
                                is_cor_inside = False
 
                    image = Image.fromarray(image)
                    
                    draw_rotated_text(image, angle, ((int(tl_text_cor[0])), (int(tl_text_cor[1] - font_scale*0))), words, 
                                        random.choice(text_color_list), font=font)

                    image = np.array(image)

                    #uncomment if you wanna check coordinate of text
                    #cv2.rectangle(image, tl, br, (0, 255, 0), 2)

                    with open('{}/gt_img_{}.txt'.format(results_img_dir,count),'a',encoding='utf8') as f:
                        f.write("{},{},{},{},{},{},{},{},{}\n".format(tl[0],tl[1],tr[0],tr[1],br[0],br[1],bl[0],bl[1],words))
                 
                name = os.path.join(results_img_dir,"img_{}.jpg".format(count))
                cv2.imwrite(name, image)
                
                print(name)
               
if __name__ == "__main__":
    main()