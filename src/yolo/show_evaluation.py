import os
import pickle
import json
import cv2
import pandas as pd 

from keras_yolov2.utils import draw_boxes, draw_true_boxes,BoundBox

# Path to evaluation history (bad boxes)
pickle_path = "/home/basile/Documents/projet_bees_detection_basile/bees_detection/src/data/pickles/histories/ResNet50_2023-04-06-17:45:47_0/test/bad_boxes_ResNet50_test.p"

# Open pickle
with open(pickle_path, 'rb') as fp:
    img_boxes = pickle.load(fp)


# Path to config filed use to evaluate
config_path = "/home/basile/Documents/projet_bees_detection_basile/bees_detection/src/config/bees_detection_resnet.json"

# Open config file as a dict
with open(config_path) as config_buffer:
    config = json.load(config_buffer)

# Path to whole dataset
dataset_path = "/home/basile/Documents/projet_bees_detection_basile/bees_detection/src/data/inputs/bees_detection_dataset.csv"
df_dataset=pd.read_csv(dataset_path,names=['filepath','xmin','ymin','xmax','ymax','label','width','height'])

# Make sure the output path exists
if not os.path.exists(config["data"]["base_path"] + '/badpreds/'):
    os.makedirs(config["data"]["base_path"] + '/badpreds/')

# Draw predicted boxes and save
for img in img_boxes:
    # Load image
    img_path = os.path.join(config["data"]["base_path"],img)
    frame = cv2.imread(img_path)

    # Get the true boxes
    true_boxes = df_dataset[df_dataset['filepath'] == os.path.join('BD_71',img)]
    true_boxes = true_boxes[['xmin', 'ymin', 'xmax', 'ymax','label']].values
    # Convert to bbox format
    true_boxes=[BoundBox(true_boxes[i][0],true_boxes[i][1],true_boxes[i][2],true_boxes[i][3],true_boxes[i][4]) for i in range(len(true_boxes))]


    # Draw true boxes
    frame = draw_true_boxes(frame, true_boxes, config['model']['labels'])

   # Draw predicted boxes
    frame = draw_boxes(frame, img_boxes[img], config['model']['labels'])
    
    # Save image
    cv2.imwrite(config["data"]["base_path"] + '/badpreds/' + str.replace(img, '/', '_'), frame)
    