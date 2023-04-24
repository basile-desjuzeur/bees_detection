import pandas as pd
from argparse import ArgumentParser
import json

from yolo.keras_yolov2.preprocessing import parse_annotation_csv

parser = ArgumentParser(description='Evaluate a detection ')

parser.add_argument(
    '-c',
    '--conf',
    default='/home/basile/Documents/projet_bees_detection_basile/bees_detection/src/yolo/config/bees_detection_mobilenet_retrain_find_lr_lr_scheduler.json',
    help='path to configuration file')

parser.add_argument(
    '-d',
    '--detection',
    default='',
    help='path to detection csv file, format: image_path, x1, y1, x2, y2, class, confidence')



def _main_(args):

    config_path = args.conf

    with open(config_path) as config_buffer:
        config = json.loads(config_buffer.read())

    validation_imgs, validation_labels = parse_annotation_csv(config['data']['valid_csv_file'],
                                                               config['model']['labels'],
                                                                config['data']['base_path'])
    
    gt_df = pd.read_csv(config['data']['valid_csv_file'], header=None)
    detection_df = pd.read_csv(args.detection, header=None)

    # Iterate over the gt images

    for i in range(len(validation_imgs)):

        img_path = validation_imgs.iloc[i, 0]
        x_min, y_min, x_max, y_max = validation_imgs.iloc[i, 1:5]


        # Get the detections for this image
        detections = detection_df[detection_df[0] == img_path]

        