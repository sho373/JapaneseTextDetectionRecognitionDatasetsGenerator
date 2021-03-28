from bing_image_downloader import downloader
import os
import shutil
import config

query = ["sky", "ocean"] #put words to search
output_dir = config.BING_OUT_DIR

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

for i in range(len(query)):
    downloader.download(query[i], limit=100, output_dir=output_dir, adult_filter_off=True,force_replace=False,timeout=60)

### merge image folders with search queary name into one image dir:"images" ###
 
target_dir = config.TARGET_DIR
if not os.path.exists(target_dir):
    os.mkdir(target_dir)

count = 0   
for dirname in os.listdir(output_dir):
    file_names = os.listdir(os.path.join(output_dir, dirname))
    for file_name in file_names:
        count+=1
        shutil.move(os.path.join(os.path.join(output_dir, dirname), file_name), target_dir)
        old_file = os.path.join(target_dir, file_name)
        new_file = os.path.join(target_dir, "img_{}.jpg".format(count))
        os.rename(old_file, new_file)
shutil.rmtree(output_dir)