import os 
import cv2
from katakana_japanese import label_dic 
import numpy as np
import re
import config

img_dir = os.path.join(config.RESULT_DIR, config.IMG_DIR) # dir with img_x.jpg and gt_img_x.txt
char_dir = config.CHAE_DIR

if not os.path.exists(char_dir): 
    os.mkdir(char_dir)

## make every katakana char dir ##
label = label_dic.values()
for _value in label:
    path = os.path.join(char_dir, str(_value))
    if not os.path.exists(path):
        os.mkdir(path)

replacements = [
    ("ァ", "ア"),
    ("ィ", "イ"),
    ("ゥ", "ウ"),
    ("ェ", "エ"),
    ("ォ", "オ"),
    ("ャ", "ヤ"), 
    ("ュ", "ユ"),
    ("ョ", "ヨ"),
    ("ッ", "ツ"),]

count = 0
file_count = 0
for filename in os.listdir(img_dir):
        if filename.endswith(".jpg"):
            image = cv2.imread(os.path.join(img_dir,filename))
            if not image is None:
                file_count += 1
                txt_filename = "gt_" + filename.split(".jpg")[0]
                with open(os.path.join(img_dir,'{}.txt'.format(txt_filename)), 'r', encoding='utf-8') as f:
                    for line in f:
                        tl_x, tl_y, tr_x, tr_y, br_x, br_y, bl_x, bl_y, word = line.split(',')
                        #im[y1:y2, x1:x2] for (x1, y1):tl, (x2,y2):br
                        cropped_image = image[int(tl_y):int(br_y), int(tl_x):int(br_x)]
                        height, width, channels = cropped_image.shape
                        each_width = int(width / (len(word) - 1))
                        start = 0
                        end = each_width
                        img = cropped_image

                        for i in range(len(word) - 1):
                            if i == len(word) - 1:
                                end = width
                            char_img = img[0 : height, start : end]
                            start = end
                            end += each_width
                            char_img = cv2.resize(char_img, (48,48))

                            if word in "ァィゥェォャュョッ":
                                for pat,repl in replacements:
                                    word = re.sub(pat, repl, word)
                                    
                            katakana_dir = os.path.join(char_dir, str(label_dic.get(word[i])))
                            name = os.path.join(katakana_dir, "img_{}.jpg".format(count))
                            # cv2.imshow("text", char_img)
                            # cv2.waitKey(0)
                            cv2.imwrite(name, char_img)
                            count += 1
                            if (count % 500 == 0):
                                print("{} char pic are generated".format(count))
                        # name = os.path.join(char_dir,"img_{}.jpg".format(word))
                        # cv2.imwrite(name, out_img)

print("Toal:{} char pictures are generated".format(count))
print("Finished {} files".format(file_count))