import os
import pickle
import json
import cv2

from keras_yolov2.utils import draw_boxes

# Path to evaluation history
pickle_path = "/home/basile/Documents/projet_bees_detection_basile/bees_detection/src/data/pickles/histories/MobileNetV2-alpha=1.0_2023-03-23-11:54:53_0/bad_boxes_MobileNetV2-alpha=1.0_temp_csv_Andrena_hattorfiana.p"

# Open pickle
with open(pickle_path, 'rb') as fp:
    img_boxes = pickle.load(fp)


# Path to config filed use to evaluate
config_path = "/home/basile/Documents/projet_bees_detection_basile/bees_detection/src/config/bees_detection.json"

# Open config file as a dict
with open(config_path) as config_buffer:
    config = json.load(config_buffer)

# Make sure the output path exists
if not os.path.exists(config["data"]["base_path"] + '/badpreds/'):
    os.makedirs(config["data"]["base_path"] + '/badpreds/')

# Draw predicted boxes and save
for img in img_boxes:
    img_path = config["data"]["base_path"] + '/' + img
    frame = cv2.imread(img_path)
    frame = draw_boxes(frame, img_boxes[img], config['model']['labels'])
    cv2.imwrite(config["data"]["base_path"] + '/badpreds/' + str.replace(img, '/', '_'), frame)
