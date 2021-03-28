import os
import splitfolders
import shutil
import config

input_dir =  config.RESULT_DIR
out_dir = config.DATA_DIR
txt_dir = config.TEXT_RESULTS_DIR
train_dir = os.path.join(out_dir, "train")
val_dir = os.path.join(out_dir, "val")
text_results_dir = config.TEXT_RESULTS_DIR

if not os.path.exists(out_dir):
    os.mkdir(out_dir)
if not os.path.exists(train_dir):
    os.mkdir(train_dir)
if not os.path.exists(val_dir):
    os.mkdir(val_dir)
if not os.path.exists(text_results_dir):
    os.mkdir(text_results_dir)

for file_name in os.listdir(os.path.join(config.RESULT_DIR, config.IMG_DIR)):
    if file_name.endswith(".txt"):
        shutil.move(os.path.join( "results/images",file_name), text_results_dir)

splitfolders.ratio(input_dir, output=out_dir,ratio=(.8, 0.2),group_prefix=None)

train_img_names = os.listdir(os.path.join(train_dir, "images"))
val_img_names = os.listdir(os.path.join(val_dir, "images"))

for file_name in train_img_names:
    txt_name = 'gt_' + file_name.split('.')[0] + '.txt'
    shutil.move(os.path.join(txt_dir, txt_name), train_dir)
    shutil.move(os.path.join("data/train/images", file_name), os.path.join(out_dir, "train"))
   
shutil.rmtree("data/train/images")

for file_name in val_img_names:
    txt_name = 'gt_' + file_name.split('.')[0] + '.txt'
    shutil.move(os.path.join(txt_dir, txt_name),os.path.join(out_dir, "val"))
    shutil.move(os.path.join("data/val/images", file_name), os.path.join(out_dir, "val"))

shutil.rmtree("data/val/images")
